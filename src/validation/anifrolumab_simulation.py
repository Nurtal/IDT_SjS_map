"""
Phase 8.1.6 — Anifrolumab in silico simulation.

Anifrolumab targets IFNAR1; in the network this corresponds to forcing
``IFNAR_complex = 0``. We simulate this perturbation under the three
conditions (Naive, IFN-stimulated, BCR-stimulated) and report the
attractor outcome per condition.

Output:
    results/phase8/drug_simulation_anifrolumab.csv
"""

from __future__ import annotations

import csv
import pathlib

import mpbn

BNET_V2 = pathlib.Path("models/sbmlqual/v2/sjd_map_v2.bnet")
OUT_CSV = pathlib.Path("results/phase8/drug_simulation_anifrolumab.csv")

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
TARGET = "IFNAR_complex"

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
ISG_NODES = ["MX1", "OAS1", "OAS2", "ISG15_Cell", "IRF7_Cell",
             "IFIT1_rna", "IFIT3_rna", "IFITM1_rna"]


def simulate(perturb: bool, cond: str, overrides: dict[str, int]) -> dict:
    bn = mpbn.MPBooleanNetwork(str(BNET_V2))
    inputs = [n for n, r in bn.items() if str(r) == n]
    eff_overrides = dict(overrides)
    if perturb:
        eff_overrides[TARGET] = 0
    for n in inputs:
        bn[n] = eff_overrides.get(n, 0)
    bn.propagate_constants()

    attrs = list(bn.attractors())
    fps = sum(1 for a in attrs
              if all(str(a.get(k, 0)) in ("0", "1") for k in a))
    n_phen = []
    n_isg = []
    for a in attrs:
        n_phen.append(sum(1 for p in PHENOTYPES
                          if str(a.get(p, 0)) in ("1", "*")))
        n_isg.append(sum(1 for g in ISG_NODES
                         if str(a.get(g, 0)) in ("1", "*")))
    return {
        "n_attractors": len(attrs),
        "n_fixed_points": fps,
        "max_phenotypes": max(n_phen, default=0),
        "min_phenotypes": min(n_phen, default=0),
        "max_isgs":       max(n_isg, default=0),
        "min_isgs":       min(n_isg, default=0),
    }


def main() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for cond, overrides in CONDITIONS.items():
        baseline = simulate(False, cond, overrides)
        treated  = simulate(True,  cond, overrides)

        rows.append({
            "drug":       "anifrolumab",
            "target":     TARGET,
            "condition":  cond,
            "baseline_n_attractors":   baseline["n_attractors"],
            "baseline_n_fixed_points": baseline["n_fixed_points"],
            "baseline_max_phenotypes": baseline["max_phenotypes"],
            "baseline_max_isgs":       baseline["max_isgs"],
            "treated_n_attractors":    treated["n_attractors"],
            "treated_n_fixed_points":  treated["n_fixed_points"],
            "treated_max_phenotypes":  treated["max_phenotypes"],
            "treated_max_isgs":        treated["max_isgs"],
            "delta_phenotypes":        baseline["max_phenotypes"]
                                       - treated["max_phenotypes"],
            "delta_isgs":              baseline["max_isgs"]
                                       - treated["max_isgs"],
        })

    fieldnames = list(rows[0].keys())
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"Saved: {OUT_CSV}  ({len(rows)} rows)")


if __name__ == "__main__":
    main()
