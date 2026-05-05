"""
Phase 2 — Boolean attractor computation.

Loads the sanitized BNET model, sets input nodes per condition, propagates
constants, and identifies all fixed points with mpbn.

Outputs:
  results/phase2/attractor_catalog.csv  — per-attractor phenotype profiles

Usage:
    python src/analysis/compute_attractors.py
"""

from __future__ import annotations

import csv
import pathlib

import mpbn

BNET    = pathlib.Path("models/sbmlqual/v1/sjd_map_reduced_clean.bnet")
OUT_DIR = pathlib.Path("results/phase2")

PHENOTYPES = [
    "Angiogenesis_phenotype",
    "Apoptosis_phenotype",
    "B_Cell_Activation_Survival_phenotype",
    "Cell_Proliferation_Survival_phenotype",
    "Chemotaxis_Infiltration_phenotype",
    "Fibrosis_phenotype",
    "Inflammation_phenotype",
    "Lymphoid_organ_development_phenotype",
    "MHC_Class_1_Activation_phenotype",
    "MHC_Class_2_Activation_phenotype",
    "Matrix_degradation_phenotype",
    "Phagocytosis_phenotype",
    "Regulated_Necrosis_phenotype",
    "T_Cell_Activation_Differentiation_phenotype",
]

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


def compute(bnet_path: pathlib.Path = BNET) -> list[dict]:
    bn_base = mpbn.MPBooleanNetwork(str(bnet_path))
    inputs  = {n for n, r in bn_base.items() if str(r) == n}
    rows: list[dict] = []

    for cond_name, overrides in CONDITIONS.items():
        bn = mpbn.MPBooleanNetwork(str(bnet_path))
        for node, val in overrides.items():
            if node in bn:
                bn[node] = val
        bn.propagate_constants()

        fps = list(bn.fixedpoints())
        for i, fp in enumerate(fps, 1):
            active = [p.replace("_phenotype", "").replace("_", " ")
                      for p in PHENOTYPES if fp.get(p, 0) == 1]
            row: dict = {
                "condition": cond_name,
                "attractor": f"FP{i}",
                "active_phenotypes": "|".join(active),
                "n_active": len(active),
            }
            for p in PHENOTYPES:
                row[p] = fp.get(p, 0)
            rows.append(row)
        print(f"  {cond_name}: {len(fps)} fixed points")

    return rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Computing attractors...")
    rows = compute()

    fieldnames = ["condition", "attractor", "active_phenotypes", "n_active"] + PHENOTYPES
    with open(OUT_DIR / "attractor_catalog.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print(f"Saved: {OUT_DIR}/attractor_catalog.csv ({len(rows)} attractors)")


if __name__ == "__main__":
    main()
