"""
Phase 4 — Control analysis: single-node perturbation screen.

For each non-input node in the network (Naive condition, 79 dynamic),
tests inhibition (force=0) and activation (force=1).
Scores each perturbation by:
  - Whether the disease attractor (FP1, 7 active phenotypes) is eliminated.
  - Reduction in active phenotypes across all remaining fixed points.

Also cross-references with SjD clinical trial drug targets.

Outputs:
  results/phase4/perturbation_screen.csv
  results/phase4/druggable_targets.csv
  results/phase4/control_report.md

Usage:
    python src/validation/control_analysis.py
"""

from __future__ import annotations

import csv
import pathlib

import mpbn

BNET     = pathlib.Path("models/sbmlqual/v1/sjd_map_reduced_clean.bnet")
DRUG_CSV = pathlib.Path(
    "data/raw/zenodo_17585308/TheSjDMap/TheSjDMap/"
    "Statistics_Overlays/Open_Targets/Clinical_trials_drugs/Sjogren_drugs.csv"
)
OUT_DIR  = pathlib.Path("results/phase4")

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

# Phenotypes active in the reference disease attractor (Naive FP1)
DISEASE_PHENOS = {
    "B_Cell_Activation_Survival_phenotype",
    "Cell_Proliferation_Survival_phenotype",
    "Chemotaxis_Infiltration_phenotype",
    "Inflammation_phenotype",
    "MHC_Class_2_Activation_phenotype",
    "Regulated_Necrosis_phenotype",
    "T_Cell_Activation_Differentiation_phenotype",
}


def build_base_network(input_values: dict[str, int]) -> tuple[mpbn.MPBooleanNetwork, dict[str, int], list[str]]:
    """Return (reduced_bn, fixed_constants, dynamic_node_list) for given input state."""
    bn = mpbn.MPBooleanNetwork(str(BNET))
    inputs = [n for n, r in bn.items() if str(r) == n]
    for inp in inputs:
        bn[inp] = input_values.get(inp, 0)
    bn.propagate_constants()
    fixed    = {n: int(str(r)) for n, r in bn.items() if str(r) in ("0", "1")}
    non_triv = [n for n, r in bn.items() if str(r) not in ("0", "1")]
    return bn, fixed, non_triv


def get_fps(bn: mpbn.MPBooleanNetwork, fixed: dict[str, int]) -> list[dict[str, int]]:
    """Compute fixed points of bn; merge with fixed constants."""
    fps = list(bn.fixedpoints())
    result = []
    for fp in fps:
        full = dict(fixed)
        full.update(fp)
        result.append({n: int(v) for n, v in full.items()})
    return result


def score_fps(fps: list[dict[str, int]]) -> dict:
    """
    Summarise attractor landscape for a given perturbation.

    Returns a dict with:
      n_fp          : number of fixed points
      disease_present: whether any FP has DISEASE_PHENOS pattern (≥6 active)
      min_active_pheno: minimum # active phenotypes over all FPs
      max_active_pheno: maximum
      best_pheno_str  : phenotypes active in the "healthiest" FP
    """
    if not fps:
        return {
            "n_fp": 0,
            "disease_present": False,
            "min_active_pheno": 0,
            "max_active_pheno": 0,
            "best_pheno_str": "",
        }

    pheno_counts = []
    for fp in fps:
        active = [p for p in PHENOTYPES if fp.get(p, 0) == 1]
        pheno_counts.append(active)

    disease_present = any(
        len(set(a) & DISEASE_PHENOS) >= 6 for a in pheno_counts
    )
    counts = [len(a) for a in pheno_counts]
    best_idx = counts.index(min(counts))

    return {
        "n_fp": len(fps),
        "disease_present": disease_present,
        "min_active_pheno": min(counts),
        "max_active_pheno": max(counts),
        "best_pheno_str": "|".join(sorted(pheno_counts[best_idx])),
    }


def perturbation_screen(
    base_bn: mpbn.MPBooleanNetwork,
    base_fixed: dict[str, int],
    dynamic_nodes: list[str],
) -> list[dict]:
    """
    For each dynamic node, test force=0 and force=1.
    Returns list of result dicts.
    """
    results = []

    # Baseline
    bn_base = mpbn.MPBooleanNetwork()
    for node in dynamic_nodes:
        bn_base[node] = base_bn[node]
    base_fps = get_fps(bn_base, base_fixed)
    base_score = score_fps(base_fps)

    for node in dynamic_nodes:
        for forced_val in (0, 1):
            bn_p = base_bn.copy()
            bn_p[node] = forced_val
            bn_p.propagate_constants()
            fixed_p = {n: int(str(r)) for n, r in bn_p.items() if str(r) in ("0", "1")}
            non_triv_p = {n: r for n, r in bn_p.items() if str(r) not in ("0", "1")}

            bn_red = mpbn.MPBooleanNetwork()
            for n, r in non_triv_p.items():
                bn_red[n] = r
            fps_p = get_fps(bn_red, fixed_p)
            score = score_fps(fps_p)

            delta_min = base_score["min_active_pheno"] - score["min_active_pheno"]
            delta_max = base_score["max_active_pheno"] - score["max_active_pheno"]
            disease_eliminated = base_score["disease_present"] and not score["disease_present"]

            results.append({
                "node": node,
                "perturbation": f"force={forced_val}",
                "n_fp": score["n_fp"],
                "disease_present": score["disease_present"],
                "min_active_pheno": score["min_active_pheno"],
                "max_active_pheno": score["max_active_pheno"],
                "delta_min_pheno": delta_min,
                "delta_max_pheno": delta_max,
                "disease_eliminated": disease_eliminated,
                "best_pheno_str": score["best_pheno_str"],
            })

    return results


def load_drug_targets() -> list[dict]:
    rows = []
    with open(DRUG_CSV) as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def cross_drug_targets(
    screen_results: list[dict],
    drug_rows: list[dict],
    all_nodes: list[str],
) -> list[dict]:
    """
    For each drug target gene, find matching BNET nodes and their perturbation scores.
    """
    target_genes = {}
    for r in drug_rows:
        g = r["target_approvedSymbol"]
        if g not in target_genes:
            target_genes[g] = {
                "gene": g,
                "target_name": r["target_approvedName"],
                "drugs": set(),
                "max_phase": 0,
            }
        target_genes[g]["drugs"].add(r["drug_name"])
        try:
            phase = int(r["phase"])
        except (ValueError, TypeError):
            phase = 0
        target_genes[g]["max_phase"] = max(target_genes[g]["max_phase"], phase)

    score_by_node = {(r["node"], r["perturbation"]): r for r in screen_results}

    drug_results = []
    for gene, info in sorted(target_genes.items(), key=lambda x: -x[1]["max_phase"]):
        # Find matching BNET nodes
        matched = [n for n in all_nodes if gene.lower() in n.lower().replace("_", " ")]
        if not matched:
            drug_results.append({
                "gene": gene,
                "max_phase": info["max_phase"],
                "drugs": "|".join(sorted(info["drugs"])),
                "target_name": info["target_name"],
                "bnet_nodes": "",
                "inhibition_disease_elim": False,
                "inhibition_delta_min": None,
                "activation_disease_elim": False,
                "activation_delta_min": None,
                "note": "No BNET node found",
            })
            continue

        for node in matched:
            inh = score_by_node.get((node, "force=0"), {})
            act = score_by_node.get((node, "force=1"), {})
            drug_results.append({
                "gene": gene,
                "max_phase": info["max_phase"],
                "drugs": "|".join(sorted(info["drugs"])),
                "target_name": info["target_name"],
                "bnet_nodes": node,
                "inhibition_disease_elim": inh.get("disease_eliminated", False),
                "inhibition_delta_min": inh.get("delta_min_pheno", None),
                "activation_disease_elim": act.get("disease_eliminated", False),
                "activation_delta_min": act.get("delta_min_pheno", None),
                "note": "",
            })

    return drug_results


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Building baseline Naive network (all inputs=0)...")
    base_bn, base_fixed, dynamic_nodes = build_base_network({})
    print(f"  Dynamic nodes: {len(dynamic_nodes)}")

    print("Running single-node perturbation screen...")
    results = perturbation_screen(base_bn, base_fixed, dynamic_nodes)
    print(f"  {len(results)} perturbations tested")

    # Top hits: disease eliminated
    eliminated = [r for r in results if r["disease_eliminated"]]
    print(f"  Perturbations eliminating disease attractor: {len(eliminated)}")

    # Top hits: most phenotype reduction
    top_delta = sorted(results, key=lambda r: -r["delta_min_pheno"])[:20]

    # Save screen results
    screen_path = OUT_DIR / "perturbation_screen.csv"
    with open(screen_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=results[0].keys())
        w.writeheader(); w.writerows(results)
    print(f"  Saved: {screen_path}")

    # Drug target cross-reference
    print("Cross-referencing with SjD drug targets...")
    drug_rows = load_drug_targets()
    all_nodes = list(base_bn.keys())
    drug_results = cross_drug_targets(results, drug_rows, all_nodes)
    drug_path = OUT_DIR / "druggable_targets.csv"
    with open(drug_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=drug_results[0].keys())
        w.writeheader(); w.writerows(drug_results)
    print(f"  Saved: {drug_path}")

    # Report
    report = _build_report(results, eliminated, top_delta, drug_results)
    report_path = OUT_DIR / "control_report.md"
    report_path.write_text(report)
    print(f"  Saved: {report_path}")
    print("\nPhase 4 complete.")


def _build_report(
    results: list[dict],
    eliminated: list[dict],
    top_delta: list[dict],
    drug_results: list[dict],
) -> str:
    lines = [
        "# Rapport d'analyse de contrôle — Phase 4",
        "",
        "**Date :** 2026-05-05  ",
        "**Méthode :** Crible de perturbations mono-nœud (inhibition/activation)  ",
        "**Réseau :** Condition Naive (79 nœuds dynamiques)  ",
        "**Attracteur cible à éliminer :** FP1 (7 phénotypes actifs = état SjD)",
        "",
        "## 1. Résumé du crible",
        "",
        f"- Perturbations testées : {len(results)} ({len(results)//2} nœuds × 2 valeurs)",
        f"- Perturbations éliminant l'attracteur maladif : **{len(eliminated)}**",
        "",
        "## 2. Perturbations éliminant l'attracteur SjD",
        "",
        "| Nœud | Perturbation | FPs restants | Phénotypes min actifs | Meilleurs phénotypes |",
        "|---|---|---|---|---|",
    ]
    for r in sorted(eliminated, key=lambda x: x["min_active_pheno"]):
        phenos = r["best_pheno_str"].replace("|", " · ").replace("_phenotype", "").replace("_", " ") or "—"
        lines.append(
            f"| {r['node']} | {r['perturbation']} | {r['n_fp']} "
            f"| {r['min_active_pheno']} | {phenos} |"
        )

    lines += [
        "",
        "## 3. Top 20 perturbations par réduction de phénotypes",
        "",
        "| Nœud | Perturbation | Δ phénotypes min | Maladie éliminée |",
        "|---|---|---|---|",
    ]
    for r in top_delta:
        lines.append(
            f"| {r['node']} | {r['perturbation']} | {r['delta_min_pheno']:+d} "
            f"| {'✓' if r['disease_eliminated'] else '○'} |"
        )

    lines += [
        "",
        "## 4. Cibles thérapeutiques SjD — confrontation au crible",
        "",
        "Phase max = phase d'essai clinique maximum atteinte. ✓ = perturbation élimine l'attracteur SjD.",
        "",
        "| Gène | Phase max | Médicaments | Nœud BNET | Inhib. Δmin | Activ. Δmin |",
        "|---|---|---|---|---|---|",
    ]
    seen_genes = set()
    for r in sorted(drug_results, key=lambda x: (-x["max_phase"], x["gene"])):
        gene = r["gene"]
        if not r["bnet_nodes"]:
            if gene not in seen_genes:
                lines.append(f"| {gene} | {r['max_phase']} | {r['drugs'][:30]} | — (absent BNET) | — | — |")
                seen_genes.add(gene)
            continue
        inh = ("✓ " if r["inhibition_disease_elim"] else "") + (
            f"{r['inhibition_delta_min']:+d}" if r["inhibition_delta_min"] is not None else "—"
        )
        act = ("✓ " if r["activation_disease_elim"] else "") + (
            f"{r['activation_delta_min']:+d}" if r["activation_delta_min"] is not None else "—"
        )
        lines.append(
            f"| {gene} | {r['max_phase']} | {r['drugs'][:30]} "
            f"| {r['bnet_nodes'][:40]} | {inh} | {act} |"
        )
        seen_genes.add(gene)

    lines += [""]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
