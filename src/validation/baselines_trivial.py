"""
Phase 8.1.5 — Trivial baselines for attractor↔cohort agreement.

For each cohort we report the balanced accuracy of two trivial classifiers:

  - all-1: predict every node as active (sens = 1, spec = 0).
  - all-0: predict every node as inactive (sens = 0, spec = 1).

Together with the per-attractor balanced accuracy from
``sensitivity_specificity_auroc.csv``, this lets the reader verify that the
IFN-stim attractor genuinely outperforms a base-rate guess.

Output:
    results/phase8/baselines_trivial.csv
"""

from __future__ import annotations

import csv
import pathlib
from collections import defaultdict

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
HGNC_CSV = pathlib.Path("data/processed/hgnc_to_bnet.csv")
OUT_CSV  = pathlib.Path("results/phase8/baselines_trivial.csv")

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


def main() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    hgnc_map = load_hgnc_mapping()
    rows: list[dict] = []
    for cohort, path in OVERLAYS.items():
        deg = load_overlay(path)
        pairs: list[tuple[str, int]] = []
        for sym, direction in deg.items():
            node = best_node(hgnc_map.get(sym, []))
            if node is None:
                continue
            pairs.append((node, direction))
        n = len(pairs)
        n_up = sum(1 for _, d in pairs if d == +1)
        n_dn = n - n_up
        if n == 0:
            continue

        # all-1: predict 1 for every pair
        tp_all1 = n_up
        fp_all1 = n_dn
        tn_all1 = 0
        fn_all1 = 0
        # all-0: predict 0 for every pair
        tp_all0 = 0
        fp_all0 = 0
        tn_all0 = n_dn
        fn_all0 = n_up

        for label, (tp, tn, fp, fn) in [
            ("all-1", (tp_all1, tn_all1, fp_all1, fn_all1)),
            ("all-0", (tp_all0, tn_all0, fp_all0, fn_all0)),
        ]:
            sens = tp / max(1, tp + fn)
            spec = tn / max(1, tn + fp)
            ppv  = tp / max(1, tp + fp)
            npv  = tn / max(1, tn + fn)
            rows.append({
                "cohort":       cohort,
                "baseline":     label,
                "n_pairs":      n,
                "n_up":         n_up,
                "n_down":       n_dn,
                "tp": tp, "tn": tn, "fp": fp, "fn": fn,
                "sensitivity":  round(sens, 3),
                "specificity":  round(spec, 3),
                "ppv":          round(ppv, 3),
                "npv":          round(npv, 3),
                "balanced_acc": round(0.5 * (sens + spec), 3),
                "up_down_ratio": round(n_up / max(1, n_dn), 2),
            })

    fieldnames = list(rows[0].keys())
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"Saved: {OUT_CSV}  ({len(rows)} rows)")


if __name__ == "__main__":
    main()
