"""
Phase 7.3.4 — Sensitivity of the AP1/p38 hit to the disease-attractor threshold (R4.5).

The Phase 4 screen labelled a perturbation as "eliminating the disease
attractor" iff no remaining FP had ≥ 6 disease phenotypes. R4.5 asks
whether the AP1/p38 hits remain stable when this threshold is varied
(5 / 6 / 7 phenotypes). This script re-runs the mono-node screen of
Phase 4 (on v2) for thresholds ∈ {5, 6, 7} and reports per-threshold hit
lists.

Outputs:
    results/phase7/threshold_sensitivity.csv
"""

from __future__ import annotations

import csv
import pathlib

import mpbn

BNET_V2 = pathlib.Path("models/sbmlqual/v2/sjd_map_v2.bnet")
OUT_CSV = pathlib.Path("results/phase7/threshold_sensitivity.csv")

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
DISEASE_PHENOS = {
    "B_Cell_Activation_Survival_phenotype",
    "Cell_Proliferation_Survival_phenotype",
    "Chemotaxis_Infiltration_phenotype",
    "Inflammation_phenotype",
    "MHC_Class_2_Activation_phenotype",
    "Regulated_Necrosis_phenotype",
    "T_Cell_Activation_Differentiation_phenotype",
}
THRESHOLDS = (5, 6, 7)
MODULE_NODES = {
    "EIF2AK2_homodimer",
    "MAP2K6_phosphorylated",
    "MAPK11_12_13_14_phosphorylated",
    "FOS_phosphorylated",
    "JUN_phosphorylated",
    "AP1_complex",
}


def baseline_dynamic_nodes() -> list[str]:
    bn = mpbn.MPBooleanNetwork(str(BNET_V2))
    inputs = [n for n, r in bn.items() if str(r) == n]
    for n in inputs:
        bn[n] = 0
    bn.propagate_constants()
    return [n for n, r in bn.items() if str(r) not in ("0", "1")]


def run_perturbation(node: str, value: int) -> int:
    bn = mpbn.MPBooleanNetwork(str(BNET_V2))
    inputs = [n for n, r in bn.items() if str(r) == n]
    for n in inputs:
        bn[n] = 0
    bn[node] = value
    bn.propagate_constants()
    fps = list(bn.fixedpoints())
    if not fps:
        return -1  # no FP — treat as "all eliminated" but flag separately
    return max(sum(1 for p in DISEASE_PHENOS if fp.get(p, 0) == 1) for fp in fps)


def main() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    nodes = baseline_dynamic_nodes()
    print(f"Dynamic nodes (Naive): {len(nodes)}")

    rows: list[dict] = []
    for node in nodes:
        for value in (0, 1):
            max_disease = run_perturbation(node, value)
            row: dict = {
                "node":          node,
                "value":         value,
                "max_disease":   max_disease,
                "in_ap1_p38":    int(node in MODULE_NODES),
            }
            for thr in THRESHOLDS:
                # "eliminates" = no FP retained ≥ thr disease phenotypes
                row[f"eliminates_thr{thr}"] = int(max_disease < thr) if max_disease >= 0 else 1
            rows.append(row)

    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Saved: {OUT_CSV}  ({len(rows)} rows)")

    # Summary per threshold
    print("\nHits per threshold:")
    for thr in THRESHOLDS:
        hits = [r for r in rows if r[f"eliminates_thr{thr}"] == 1]
        ap1_hits = [r for r in hits if r["in_ap1_p38"] == 1]
        print(f"  thr={thr}: {len(hits)} total hits, "
              f"{len(ap1_hits)} from AP1/p38 module")
        for r in ap1_hits:
            print(f"    [AP1/p38] {r['node']} (value={r['value']})")


if __name__ == "__main__":
    main()
