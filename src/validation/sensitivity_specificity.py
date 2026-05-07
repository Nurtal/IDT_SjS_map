"""
Phase 7.2.3 — Decompose attractor↔cohort agreement into TP/TN/FP/FN
and compute sensitivity, specificity and AUROC.

Per attractor × cohort:
  TP = DEG up   AND node = 1     (correctly predicts up-regulation)
  TN = DEG down AND node = 0     (correctly predicts down-regulation)
  FP = DEG down AND node = 1
  FN = DEG up   AND node = 0

Sensitivity = TP / (TP + FN)
Specificity = TN / (TN + FP)
AUROC is computed on the cross-attractor ranking of nodes by their
*activation frequency* across the 5 v2 attractors. Under H1 (model
captures cohort biology), nodes mapped to up DEGs should have higher
mean activation across attractors than nodes mapped to down DEGs.

Outputs:
    results/phase7/sensitivity_specificity_auroc.csv
"""

from __future__ import annotations

import csv
import pathlib
from collections import defaultdict

import numpy as np
from sklearn.metrics import roc_auc_score

import mpbn

BNET_V2  = pathlib.Path("models/sbmlqual/v2/sjd_map_v2.bnet")
HGNC_CSV = pathlib.Path("data/processed/hgnc_to_bnet.csv")
OVERLAY_DIR = pathlib.Path(
    "data/raw/zenodo_17585308/TheSjDMap/TheSjDMap/Statistics_Overlays"
)
OVERLAYS = {
    "PRECISESADS": OVERLAY_DIR / "Blood_datasets/overlay_PRECISESADS.txt",
    "UKPSSR":      OVERLAY_DIR / "Blood_datasets/overlay_UKPSSR.txt",
    "GSE51092":    OVERLAY_DIR / "Blood_datasets/overlay_GSE51092.txt",
    "ASSESS":      OVERLAY_DIR / "ASSESS/ASSESS_lymphoma.txt",
    "GSE23117":    OVERLAY_DIR / "GSE23117/overlay_GSE23117.txt",
}
OUT_CSV = pathlib.Path("results/phase7/sensitivity_specificity_auroc.csv")
CONDITIONS: dict[str, dict[str, int]] = {
    "Naive (homeostatic)": {},
    "IFN-stimulated": {
        "IFNA_Extracellular_ligands":  1,
        "IFNB1_Extracellular_ligands": 1,
        "IFNG_IFNGR_complex":          1,
        "IFNAR_complex":               1,
    },
    "BCR-stimulated": {"BCR_complex": 1},
}

RNA_PREF_ORDER = ["rna", "protein", "complex_member", "secreted",
                  "secreted_ligand", "cell_localised", "active",
                  "phosphorylated", "homodimer", "nucleus", "empty",
                  "small_molecule", "cell_surface_receptor"]


def load_overlay(path: pathlib.Path) -> dict[str, int]:
    out: dict[str, int] = {}
    if not path.exists():
        return out
    with open(path) as f:
        next(f, None)
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2 or not parts[0] or parts[0] == "NA":
                continue
            sym, color = parts[0], parts[1]
            if "FF0000" in color.upper():
                out[sym] = +1
            elif "0000FF" in color.upper():
                out[sym] = -1
    return out


def load_hgnc_mapping() -> dict[str, list[tuple[str, str]]]:
    out: dict[str, list[tuple[str, str]]] = defaultdict(list)
    with open(HGNC_CSV) as f:
        for r in csv.DictReader(f):
            out[r["hgnc_symbol"]].append((r["bnet_node"], r["kind"]))
    return out


def best_node(nodes: list[tuple[str, str]]) -> str | None:
    if not nodes:
        return None
    by_kind: dict[str, str] = {}
    for node, kind in nodes:
        by_kind.setdefault(kind, node)
    for kind in RNA_PREF_ORDER:
        if kind in by_kind:
            return by_kind[kind]
    return nodes[0][0]


def attractor_states() -> dict[str, dict[str, int]]:
    bn_base = mpbn.MPBooleanNetwork(str(BNET_V2))
    inputs = [n for n, r in bn_base.items() if str(r) == n]
    out: dict[str, dict[str, int]] = {}
    for cond_name, overrides in CONDITIONS.items():
        bn = mpbn.MPBooleanNetwork(str(BNET_V2))
        for n in inputs:
            bn[n] = overrides.get(n, 0)
        bn.propagate_constants()
        attrs = list(bn.attractors())
        for i, attr in enumerate(attrs, 1):
            state = {n: 1 if str(attr.get(n, str(r))) in ("1", "*") else 0
                     for n, r in bn.items()}
            out[f"{cond_name}|A{i}"] = state
    return out


def main() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    states = attractor_states()
    print(f"v2 attractors: {len(states)}")

    hgnc_map = load_hgnc_mapping()

    # Cross-attractor activation frequency — used as the AUROC score.
    # For each node, fraction of attractors where the node is active.
    n_attr = len(states)
    activation_freq: dict[str, float] = defaultdict(float)
    for attr_state in states.values():
        for n, v in attr_state.items():
            activation_freq[n] += v / n_attr

    rows: list[dict] = []
    for cohort, path in OVERLAYS.items():
        deg = load_overlay(path)
        # Build the (node, direction) list deduplicating by best_node.
        pairs: list[tuple[str, int]] = []
        for sym, direction in deg.items():
            node = best_node(hgnc_map.get(sym, []))
            if node is None:
                continue
            pairs.append((node, direction))
        if not pairs:
            continue

        # AUROC on activation frequency
        scores = np.array([activation_freq.get(n, 0.0) for n, _ in pairs])
        labels = np.array([1 if d == +1 else 0 for _, d in pairs])
        if len(set(labels)) < 2:
            auroc = float("nan")
        else:
            auroc = float(roc_auc_score(labels, scores))

        # Per-attractor sensitivity / specificity
        for attr_key, attr_state in states.items():
            cond, fp = attr_key.split("|")
            tp = tn = fp_ = fn = 0
            for node, direction in pairs:
                pred = attr_state.get(node, 0)
                if direction == +1 and pred == 1:
                    tp += 1
                elif direction == -1 and pred == 0:
                    tn += 1
                elif direction == -1 and pred == 1:
                    fp_ += 1
                elif direction == +1 and pred == 0:
                    fn += 1
            sens = tp / max(1, tp + fn)
            spec = tn / max(1, tn + fp_)
            ppv = tp / max(1, tp + fp_)
            npv = tn / max(1, tn + fn)
            rows.append({
                "cohort":       cohort,
                "condition":    cond,
                "attractor":    fp,
                "n_pairs":      len(pairs),
                "tp":           tp,
                "tn":           tn,
                "fp":           fp_,
                "fn":           fn,
                "sensitivity":  round(sens, 3),
                "specificity":  round(spec, 3),
                "ppv":          round(ppv, 3),
                "npv":          round(npv, 3),
                "balanced_acc": round(0.5 * (sens + spec), 3),
                "auroc":        round(auroc, 3),
            })

    fieldnames = list(rows[0].keys())
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"Saved: {OUT_CSV}  ({len(rows)} rows)")


if __name__ == "__main__":
    main()
