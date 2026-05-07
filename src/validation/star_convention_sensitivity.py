"""
Phase 8.1.7 — Sensitivity of phenotype/ISG counts to the trap-space `*`
convention.

The Phase 7 catalogue counts a phenotype as active if its trap-space
coordinate is `1` *or* `*` (oscillating, *activable* in some MP trajectory).
This script rebuilds the same catalogue under the alternative convention
`* = 0` (oscillating, *not guaranteed* to be active) and reports the
phenotype count delta per attractor.

Output:
    results/phase8/star_convention_sensitivity.csv
"""

from __future__ import annotations

import csv
import pathlib

import mpbn

BNET_V2 = pathlib.Path("models/sbmlqual/v2/sjd_map_v2.bnet")
OUT_CSV = pathlib.Path("results/phase8/star_convention_sensitivity.csv")

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

ISG_NODES = ["MX1", "MX2", "OAS1", "OAS2", "OAS3", "OASL",
             "ISG15_Cell", "ISG20",
             "IFIT1_rna", "IFIT2_rna", "IFIT3_rna", "IFIT5_rna",
             "IFITM1_rna", "IFITM2_rna", "IFITM3_rna",
             "IRF7_Cell", "IRF9"]


def main() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    bn_base = mpbn.MPBooleanNetwork(str(BNET_V2))
    inputs = [n for n, r in bn_base.items() if str(r) == n]

    rows: list[dict] = []
    for cond, overrides in CONDITIONS.items():
        bn = mpbn.MPBooleanNetwork(str(BNET_V2))
        for n in inputs:
            bn[n] = overrides.get(n, 0)
        bn.propagate_constants()

        attrs = list(bn.attractors())
        for i, attr in enumerate(attrs, 1):
            n_phen_inclusive = 0   # * → 1
            n_phen_exclusive = 0   # * → 0
            n_phen_star = 0        # only the * coord
            for p in PHENOTYPES:
                v = str(attr.get(p, 0))
                if v == "1":
                    n_phen_inclusive += 1
                    n_phen_exclusive += 1
                elif v == "*":
                    n_phen_inclusive += 1
                    n_phen_star += 1

            n_isg_inclusive = 0
            n_isg_exclusive = 0
            n_isg_star = 0
            for g in ISG_NODES:
                v = str(attr.get(g, 0))
                if v == "1":
                    n_isg_inclusive += 1
                    n_isg_exclusive += 1
                elif v == "*":
                    n_isg_inclusive += 1
                    n_isg_star += 1

            kind = "fixed_point" if all(
                str(attr.get(k, 0)) in ("0", "1") for k in attr
            ) else "trap_space"
            rows.append({
                "condition": cond,
                "attractor": f"A{i}",
                "kind":      kind,
                "phenotypes_inclusive_star1": n_phen_inclusive,
                "phenotypes_exclusive_star0": n_phen_exclusive,
                "phenotypes_star_count":      n_phen_star,
                "phenotypes_delta":           n_phen_inclusive - n_phen_exclusive,
                "isgs_inclusive_star1":       n_isg_inclusive,
                "isgs_exclusive_star0":       n_isg_exclusive,
                "isgs_star_count":            n_isg_star,
                "isgs_delta":                 n_isg_inclusive - n_isg_exclusive,
            })

    fieldnames = list(rows[0].keys())
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"Saved: {OUT_CSV}  ({len(rows)} rows)")


if __name__ == "__main__":
    main()
