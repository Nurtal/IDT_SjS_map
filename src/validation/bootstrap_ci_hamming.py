"""
Phase 8.1.4 — Bootstrap 95 % CI on the observed Hamming distances.

Complements the permutation null model (Phase 7.2.2) with a bootstrap
resampling of the (gene, node) pairs themselves. For each (cohort,
attractor) pair we resample the mapped pairs *with replacement*, recompute
the Hamming distance, and report the 2.5th and 97.5th percentiles over
1 000 bootstrap samples as a 95 % confidence interval.

Adds the colum ``hamming_lo``, ``hamming_hi`` to a fresh table at:

    results/phase8/attractor_cohort_distance_v3.csv

This file extends ``results/phase7/attractor_cohort_distance_v2.csv`` with
the bootstrap CI without recomputing the permutation p-values.
"""

from __future__ import annotations

import argparse
import csv
import pathlib
from collections import defaultdict

import mpbn
import numpy as np

BNET_V2 = pathlib.Path("models/sbmlqual/v2/sjd_map_v2.bnet")
HGNC_CSV = pathlib.Path("data/processed/hgnc_to_bnet.csv")
DIST_V2 = pathlib.Path("results/phase7/attractor_cohort_distance_v2.csv")
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
OUT_CSV = pathlib.Path("results/phase8/attractor_cohort_distance_v3.csv")

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
    for cond, overrides in CONDITIONS.items():
        bn = mpbn.MPBooleanNetwork(str(BNET_V2))
        for n in inputs:
            bn[n] = overrides.get(n, 0)
        bn.propagate_constants()
        attrs = list(bn.attractors())
        for i, attr in enumerate(attrs, 1):
            state = {n: 1 if str(attr.get(n, str(r))) in ("1", "*") else 0
                     for n, r in bn.items()}
            out[f"{cond}|A{i}"] = state
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-bootstrap", type=int, default=1000)
    ap.add_argument("--seed",        type=int, default=0)
    args = ap.parse_args()

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    states = attractor_states()
    hgnc_map = load_hgnc_mapping()
    rng = np.random.default_rng(args.seed)

    # Load Phase 7.2.2 distances to merge with new bootstrap CI columns.
    base_rows: list[dict] = []
    with open(DIST_V2) as f:
        for r in csv.DictReader(f):
            base_rows.append(r)

    # Index for quick lookup
    base_idx: dict[tuple[str, str, str], dict] = {
        (r["cohort"], r["condition"], r["attractor"]): r for r in base_rows
    }

    rows: list[dict] = []
    for cohort, path in OVERLAYS.items():
        deg = load_overlay(path)
        pairs: list[tuple[str, int]] = []
        for sym, direction in deg.items():
            node = best_node(hgnc_map.get(sym, []))
            if node is None:
                continue
            expected = 1 if direction == +1 else 0
            pairs.append((node, expected))
        n = len(pairs)
        if n == 0:
            continue
        # Bootstrap indices (n_bootstrap, n_pairs)
        boot_idx = rng.integers(0, n, size=(args.n_bootstrap, n))

        for attr_key, state in states.items():
            cond, fp = attr_key.split("|")
            mismatch = np.array(
                [0 if state.get(node, 0) == expected else 1
                 for node, expected in pairs],
                dtype=np.int8,
            )
            obs_h = float(mismatch.sum() / n)
            boot_h = mismatch[boot_idx].mean(axis=1)
            lo, hi = float(np.percentile(boot_h, 2.5)), \
                     float(np.percentile(boot_h, 97.5))

            base = base_idx.get((cohort, cond, fp), {})
            row = {
                "cohort":      cohort,
                "condition":   cond,
                "attractor":   fp,
                "n_pairs":     n,
                "hamming":     round(obs_h, 4),
                "hamming_lo":  round(lo, 4),
                "hamming_hi":  round(hi, 4),
                "null_mean":   base.get("null_mean", ""),
                "null_std":    base.get("null_std",  ""),
                "z_score":     base.get("z_score",   ""),
                "p_value":     base.get("p_value",   ""),
            }
            rows.append(row)

    fieldnames = ["cohort", "condition", "attractor", "n_pairs", "hamming",
                  "hamming_lo", "hamming_hi", "null_mean", "null_std",
                  "z_score", "p_value"]
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"Saved: {OUT_CSV}  ({len(rows)} rows)")


if __name__ == "__main__":
    main()
