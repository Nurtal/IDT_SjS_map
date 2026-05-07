"""
Phase 7.3.2 — Combinatorial (pairwise) perturbation screen on v2.

Reviewers R1.3, R2.3 and R4.1 ask whether the manuscript's claim of "JAK +
p38 synergy" is supported by simulation. The Phase 4 mono-node screen
cannot answer this — only pairs can. We run a *targeted* pair screen
(rather than the full ~3000-pair grid) over biologically motivated drug
combinations, augmented with the 7 Phase-4 hits crossed with each other.

For each (cond, pair) we report:
    - n FPs after dual perturbation
    - max_phenos_active across remaining FPs
    - is_synergy: TRUE iff (a) the pair eliminates FP1 (max_phenos < 6) AND
      (b) neither single-node perturbation does so.

Outputs:
    results/phase7/combinatorial_perturbations.csv
    figures/phase7/combinatorial_heatmap.png
"""

from __future__ import annotations

import csv
import itertools
import pathlib
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import mpbn  # noqa: E402
import numpy as np  # noqa: E402

BNET_V2 = pathlib.Path("models/sbmlqual/v2/sjd_map_v2.bnet")
OUT_CSV = pathlib.Path("results/phase7/combinatorial_perturbations.csv")
OUT_PNG = pathlib.Path("figures/phase7/combinatorial_heatmap.png")

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

# Drug-target nodes of interest (R2.3, R4.1).  These are SJD clinical trial
# targets; the goal is to test whether *combinations* eliminate the disease
# attractor when the single-target perturbations do not.
DRUG_TARGETS = [
    "JAK1_phosphorylated",         # filgotinib, baricitinib, tofacitinib
    "JAK2_phosphorylated",         # baricitinib
    "JAK3_phosphorylated",         # tofacitinib
    "TYK2_phosphorylated",         # deucravacitinib
    "STAT2_phosphorylated",
    "BTK_phosphorylated",          # tirabrutinib
    "SYK_phosphorylated",          # fostamatinib
    "TNFRSF13C",                   # ianalumab (BAFF-R)
    "MAPK11_12_13_14_phosphorylated",  # losmapimod, doramapimod (p38)
    "AP1_complex",
    "FOS_phosphorylated",
    "JUN_phosphorylated",
    "EIF2AK2_homodimer",           # PKR
    "MAP2K6_phosphorylated",
]

# Specific pairs called out by the reviewers
EXPLICIT_PAIRS = [
    ("JAK1_phosphorylated", "MAPK11_12_13_14_phosphorylated"),  # JAK + p38 (R2.3)
    ("JAK1_phosphorylated", "AP1_complex"),
    ("BTK_phosphorylated",  "MAPK11_12_13_14_phosphorylated"),  # BCR/lymphoma + p38
    ("BTK_phosphorylated",  "AP1_complex"),
    ("SYK_phosphorylated",  "MAPK11_12_13_14_phosphorylated"),
    ("TYK2_phosphorylated", "MAPK11_12_13_14_phosphorylated"),
    ("STAT2_phosphorylated", "AP1_complex"),
]


def build_pair_pool() -> list[tuple[str, str]]:
    """Return EXPLICIT_PAIRS plus all 2-combinations of DRUG_TARGETS."""
    pool: set[tuple[str, str]] = set()
    for a, b in itertools.combinations(DRUG_TARGETS, 2):
        pool.add((a, b) if a < b else (b, a))
    for a, b in EXPLICIT_PAIRS:
        pool.add((a, b) if a < b else (b, a))
    return sorted(pool)


def run_perturbation(cond_name: str, overrides: dict[str, int],
                     fixes: dict[str, int]) -> tuple[int, int, list[int]]:
    """Run mpbn fixed-point enumeration after applying fixes.

    Returns (n_fps, max_n_disease_phenos, n_phenos_per_fp).
    """
    bn = mpbn.MPBooleanNetwork(str(BNET_V2))
    inputs = [n for n, r in bn.items() if str(r) == n]
    for n in inputs:
        bn[n] = overrides.get(n, 0)
    for node, val in fixes.items():
        if node in bn:
            bn[node] = val
    bn.propagate_constants()

    fps = list(bn.fixedpoints())
    n_phenos = []
    max_disease = 0
    for fp in fps:
        active = sum(1 for p in PHENOTYPES if fp.get(p, 0) == 1)
        n_phenos.append(active)
        active_disease = sum(1 for p in DISEASE_PHENOS if fp.get(p, 0) == 1)
        max_disease = max(max_disease, active_disease)
    return len(fps), max_disease, n_phenos


def main() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)

    pool = build_pair_pool()
    print(f"Pair pool: {len(pool)} unique pairs across {len(DRUG_TARGETS)} targets "
          f"+ {len(EXPLICIT_PAIRS)} explicit pairs")

    rows: list[dict] = []
    for cond_name, overrides in CONDITIONS.items():
        # Baseline (no perturbation)
        n_fp_b, max_b, _ = run_perturbation(cond_name, overrides, {})
        # Mono-node baselines for each target — needed to detect synergy.
        mono = {}
        for t in DRUG_TARGETS:
            mono[t] = run_perturbation(cond_name, overrides, {t: 0})

        print(f"\nCondition: {cond_name}  baseline: {n_fp_b} FPs, "
              f"max disease phenos = {max_b}")

        for a, b in pool:
            n_fp, max_disease, _ = run_perturbation(cond_name, overrides,
                                                    {a: 0, b: 0})
            mono_a = mono.get(a)
            mono_b = mono.get(b)
            mono_a_max = mono_a[1] if mono_a else max_b
            mono_b_max = mono_b[1] if mono_b else max_b
            single_eliminates = (mono_a_max < 6) or (mono_b_max < 6)
            pair_eliminates = max_disease < 6
            synergy = pair_eliminates and not single_eliminates
            rows.append({
                "condition":          cond_name,
                "node_a":             a,
                "node_b":             b,
                "baseline_max_disease": max_b,
                "mono_a_max_disease": mono_a_max,
                "mono_b_max_disease": mono_b_max,
                "pair_n_fp":          n_fp,
                "pair_max_disease":   max_disease,
                "pair_eliminates":    int(pair_eliminates),
                "synergy":            int(synergy),
            })

    fieldnames = list(rows[0].keys())
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"\nSaved: {OUT_CSV}  ({len(rows)} rows)")

    # ── Heatmap of pair_max_disease for "Naive" condition ───────────────────
    naive_rows = [r for r in rows if r["condition"] == "Naive (homeostatic)"]
    nodes_in_pool = sorted({r["node_a"] for r in naive_rows} |
                           {r["node_b"] for r in naive_rows})
    idx = {n: i for i, n in enumerate(nodes_in_pool)}
    M = np.full((len(nodes_in_pool), len(nodes_in_pool)), np.nan)
    for r in naive_rows:
        i, j = idx[r["node_a"]], idx[r["node_b"]]
        M[i, j] = r["pair_max_disease"]
        M[j, i] = r["pair_max_disease"]
    fig, ax = plt.subplots(figsize=(10, 8.5))
    im = ax.imshow(M, cmap="RdYlGn_r", vmin=0, vmax=7)
    ax.set_xticks(range(len(nodes_in_pool)))
    ax.set_yticks(range(len(nodes_in_pool)))
    ax.set_xticklabels(nodes_in_pool, rotation=70, ha="right", fontsize=7)
    ax.set_yticklabels(nodes_in_pool, fontsize=7)
    plt.colorbar(im, ax=ax, label="max disease phenotypes after pair KO")
    ax.set_title("Pairwise perturbations — Naive condition\n"
                 "(green = pair eliminates disease attractor)")
    plt.tight_layout()
    fig.savefig(OUT_PNG, dpi=130)
    print(f"Saved: {OUT_PNG}")

    # ── Summary stats ───────────────────────────────────────────────────────
    by_cond = defaultdict(lambda: {"n_total": 0, "n_eliminates": 0,
                                   "n_synergy": 0})
    synergy_pairs: list[dict] = []
    for r in rows:
        c = r["condition"]
        by_cond[c]["n_total"] += 1
        by_cond[c]["n_eliminates"] += r["pair_eliminates"]
        by_cond[c]["n_synergy"] += r["synergy"]
        if r["synergy"]:
            synergy_pairs.append(r)

    print("\n=== Summary ===")
    for c, s in by_cond.items():
        print(f"  {c}: {s['n_total']} pairs, "
              f"{s['n_eliminates']} eliminate FP1, {s['n_synergy']} synergistic")
    print(f"\nSynergistic pairs (eliminate disease attractor while neither "
          f"single-node KO does so):")
    for r in synergy_pairs[:20]:
        print(f"  [{r['condition']}] {r['node_a']} + {r['node_b']}")


if __name__ == "__main__":
    main()
