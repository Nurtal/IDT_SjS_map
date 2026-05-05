"""
Phase 3 — Biological annotation of Boolean attractors.

For each attractor (from results/phase2/attractor_catalog.csv), computes:
1. Pathway activity profiles (JAK-STAT, NF-kB, IFN, BCR, TLR, BAFF).
2. DEG-attractor distance (Hamming) against 3 blood transcriptomic cohorts.
3. Best-matching attractor per cohort.

Outputs:
  results/phase3/pathway_profiles.csv
  results/phase3/deg_mapping.csv
  results/phase3/attractor_cohort_distance.csv
  results/phase3/annotation_report.md

Usage:
    python src/validation/annotate_attractors.py
"""

from __future__ import annotations

import csv
import pathlib
import re
from collections import defaultdict

import mpbn

# ── Paths ────────────────────────────────────────────────────────────────────
BNET         = pathlib.Path("models/sbmlqual/v1/sjd_map_reduced_clean.bnet")
CATALOG      = pathlib.Path("results/phase2/attractor_catalog.csv")
OVERLAY_DIR  = pathlib.Path("data/raw/zenodo_17585308/TheSjDMap/TheSjDMap/Statistics_Overlays/Blood_datasets")
OUT_DIR      = pathlib.Path("results/phase3")

OVERLAYS = {
    "PRECISESADS": OVERLAY_DIR / "overlay_PRECISESADS.txt",
    "UKPSSR":      OVERLAY_DIR / "overlay_UKPSSR.txt",
    "GSE51092":    OVERLAY_DIR / "overlay_GSE51092.txt",
}

# ── Pathway node patterns ────────────────────────────────────────────────────
PATHWAYS = {
    "JAK-STAT":  ["STAT1", "STAT2", "STAT3", "STAT4", "STAT5", "STAT6", "JAK1", "JAK2", "TYK2"],
    "NF-kB":     ["RELA", "NFKB1", "NFKB2", "RELB", "REL", "NFKBIA", "TNFAIP3"],
    "IFN-I":     ["IFNAR", "IFNA", "IFNB", "IRF3", "IRF7", "IRF9", "MX1", "OAS", "ISG15"],
    "IFN-II":    ["IFNG", "IFNGR", "IRF1"],
    "BCR":       ["BCR", "BTK", "SYK", "BLNK", "PI3K", "AKT", "PLCG"],
    "TLR":       ["TLR", "MYD88", "TRIF", "IRAK", "TRAF6"],
    "BAFF":      ["TNFSF13", "BAFF", "TACI", "BAFFR", "BCMA", "TNFRSF13"],
    "Complement":["C3a", "C5a", "C3AR", "C5AR"],
    "Apoptosis": ["CASP3", "CASP7", "BCL2", "BAD", "BAX", "LMNB1"],
}


def load_bn_and_catalog() -> tuple[mpbn.MPBooleanNetwork, list[dict]]:
    bn = mpbn.MPBooleanNetwork(str(BNET))
    rows = []
    with open(CATALOG) as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return bn, rows


def get_attractor_states(bn: mpbn.MPBooleanNetwork, catalog: list[dict]) -> dict[str, dict[str, int]]:
    """
    Recompute per-node states for each attractor by re-running fixed-point computation.
    Returns {attractor_key: {node: 0/1}}.
    """
    inputs = [n for n, r in bn.items() if str(r) == n]

    CONDITIONS = {
        "Naive (homeostatic)": {},
        "IFN-stimulated": {
            "IFNA_Extracellular_ligands": 1,
            "IFNB1_Extracellular_ligands": 1,
            "IFNG_IFNGR_complex": 1,
            "IFNAR_complex": 1,
        },
        "BCR-stimulated": {"BCR_complex": 1},
    }

    states: dict[str, dict[str, int]] = {}
    for cond_name, cond_vals in CONDITIONS.items():
        bn_c = bn.copy()
        for inp in inputs:
            bn_c[inp] = cond_vals.get(inp, 0)
        bn_c.propagate_constants()
        fixed = {n: int(str(r)) for n, r in bn_c.items() if str(r) in ("0", "1")}
        non_trivial = {n: r for n, r in bn_c.items() if str(r) not in ("0", "1")}
        bn_red = mpbn.MPBooleanNetwork()
        for node, rule in non_trivial.items():
            bn_red[node] = rule
        fps = list(bn_red.fixedpoints())
        for i, fp in enumerate(fps):
            full = dict(fixed)
            full.update(fp)
            key = f"{cond_name}|FP{i+1}"
            states[key] = {n: int(v) for n, v in full.items()}
    return states


def pathway_activity(states: dict[str, dict[str, int]]) -> list[dict]:
    """Fraction of pathway members that are active in each attractor."""
    rows = []
    for attr_key, node_states in states.items():
        cond, fp = attr_key.split("|")
        row: dict = {"condition": cond, "attractor": fp}
        for pw_name, keywords in PATHWAYS.items():
            members = [n for n in node_states if any(kw.lower() in n.lower() for kw in keywords)]
            if members:
                active = sum(node_states[n] for n in members)
                row[pw_name] = round(active / len(members), 3)
            else:
                row[pw_name] = None
        rows.append(row)
    return rows


def load_overlay(path: pathlib.Path) -> dict[str, int]:
    """Return {gene_name: +1/-1} from Cytoscape overlay txt."""
    deg: dict[str, int] = {}
    with open(path) as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue
            gene, color = parts[0], parts[1]
            if "#FF0000" in color:
                deg[gene] = 1   # upregulated
            elif "#0000FF" in color:
                deg[gene] = -1  # downregulated
    return deg


def map_genes_to_nodes(
    deg: dict[str, int],
    node_names: list[str],
) -> dict[str, tuple[str, int]]:
    """
    Map gene symbols to BNET node names using substring matching.
    Returns {node_name: (gene_symbol, direction)}.
    A gene maps to a node if the gene symbol appears as a word boundary in the
    node name (case-insensitive, ignoring underscores → spaces).
    """
    mapped: dict[str, tuple[str, int]] = {}
    for gene, direction in deg.items():
        gene_pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(gene) + r"(?![A-Za-z0-9])", re.IGNORECASE)
        for node in node_names:
            node_norm = node.replace("_", " ")
            if gene_pat.search(node_norm) and node not in mapped:
                mapped[node] = (gene, direction)
    return mapped


def hamming_distance(
    attractor_state: dict[str, int],
    mapped: dict[str, tuple[str, int]],
) -> tuple[float, int]:
    """
    Hamming distance (fraction of mismatches) between attractor node states
    and DEG directions for mapped nodes only.

    Returns (hamming_fraction, n_matched_nodes).
    """
    mismatches = 0
    total = 0
    for node, (gene, direction) in mapped.items():
        if node not in attractor_state:
            continue
        predicted = attractor_state[node]
        # direction: +1 = up (expected active=1), -1 = down (expected active=0)
        expected = 1 if direction == 1 else 0
        if predicted != expected:
            mismatches += 1
        total += 1
    if total == 0:
        return float("nan"), 0
    return round(mismatches / total, 4), total


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading Boolean network...")
    bn, catalog = load_bn_and_catalog()
    all_nodes = list(bn.keys())
    print(f"  {len(all_nodes)} nodes, {len(catalog)} attractor records")

    print("Computing full node states for all attractors...")
    states = get_attractor_states(bn, catalog)
    print(f"  {len(states)} attractors")

    # ── 1. Pathway activity profiles ────────────────────────────────────────
    print("Computing pathway activity profiles...")
    pw_rows = pathway_activity(states)
    pw_path = OUT_DIR / "pathway_profiles.csv"
    with open(pw_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=pw_rows[0].keys())
        w.writeheader(); w.writerows(pw_rows)
    print(f"  Saved: {pw_path}")

    # ── 2. DEG overlay loading and gene→node mapping ────────────────────────
    print("Loading DEG overlays and mapping genes to nodes...")
    cohort_maps: dict[str, dict[str, tuple[str, int]]] = {}
    mapping_rows = []
    for cohort, ov_path in OVERLAYS.items():
        deg = load_overlay(ov_path)
        mapped = map_genes_to_nodes(deg, all_nodes)
        cohort_maps[cohort] = mapped
        n_up = sum(1 for _, d in mapped.values() if d == 1)
        n_dn = sum(1 for _, d in mapped.values() if d == -1)
        print(f"  {cohort}: {len(deg)} DEGs → {len(mapped)} BNET nodes ({n_up} up, {n_dn} down)")
        for node, (gene, direction) in sorted(mapped.items()):
            mapping_rows.append({"cohort": cohort, "gene": gene,
                                  "direction": direction, "bnet_node": node})

    mapping_path = OUT_DIR / "deg_mapping.csv"
    if mapping_rows:
        with open(mapping_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["cohort", "gene", "direction", "bnet_node"])
            w.writeheader(); w.writerows(mapping_rows)
        print(f"  Saved: {mapping_path}")

    # ── 3. Hamming distances ─────────────────────────────────────────────────
    print("Computing attractor–cohort Hamming distances...")
    dist_rows = []
    for attr_key, node_states in states.items():
        cond, fp = attr_key.split("|")
        row: dict = {"condition": cond, "attractor": fp}
        for cohort, mapped in cohort_maps.items():
            dist, n = hamming_distance(node_states, mapped)
            row[f"{cohort}_hamming"] = dist
            row[f"{cohort}_n"] = n
        dist_rows.append(row)

    dist_path = OUT_DIR / "attractor_cohort_distance.csv"
    with open(dist_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=dist_rows[0].keys())
        w.writeheader(); w.writerows(dist_rows)
    print(f"  Saved: {dist_path}")

    # ── 4. Report ────────────────────────────────────────────────────────────
    report = _build_report(pw_rows, dist_rows, cohort_maps, states)
    report_path = OUT_DIR / "annotation_report.md"
    report_path.write_text(report)
    print(f"  Saved: {report_path}")
    print("\nPhase 3 annotation complete.")


def _build_report(
    pw_rows: list[dict],
    dist_rows: list[dict],
    cohort_maps: dict,
    states: dict,
) -> str:
    lines = [
        "# Rapport d'annotation biologique — Phase 3",
        "",
        "**Date :** 2026-05-05  ",
        "**Attracteurs :** 6 points fixes (3 conditions × 2 FP)  ",
        "**Cohortes DEG :** PRECISESADS, UKPSSR, GSE51092",
        "",
        "## 1. Activité des voies de signalisation",
        "",
        "Fraction de nœuds actifs parmi les membres de chaque voie :",
        "",
        "| Condition | Attracteur | " + " | ".join(PATHWAYS.keys()) + " |",
        "|---|---|" + "---|" * len(PATHWAYS),
    ]
    for r in pw_rows:
        vals = " | ".join(
            ("—" if r[pw] is None else f"{r[pw]:.2f}") for pw in PATHWAYS
        )
        lines.append(f"| {r['condition']} | {r['attractor']} | {vals} |")

    lines += [
        "",
        "## 2. Couverture DEG → nœuds BNET",
        "",
        "| Cohorte | DEGs total | Nœuds BNET mappés | Up mappés | Down mappés |",
        "|---|---|---|---|---|",
    ]
    for cohort, mapped in cohort_maps.items():
        n_up = sum(1 for _, d in mapped.values() if d == 1)
        n_dn = sum(1 for _, d in mapped.values() if d == -1)
        lines.append(f"| {cohort} | — | {len(mapped)} | {n_up} | {n_dn} |")

    lines += [
        "",
        "## 3. Distance de Hamming attracteur–cohorte",
        "",
        "Distance = fraction de nœuds mappés dont l'état prédit ≠ signe DEG.",
        "**Plus la distance est faible, meilleure est la correspondance.**",
        "",
        "| Condition | Attracteur | PRECISESADS | UKPSSR | GSE51092 |",
        "|---|---|---|---|---|",
    ]
    best: dict[str, tuple[str, str, float]] = {}  # cohort → (cond, fp, dist)
    for r in dist_rows:
        ps  = r.get("PRECISESADS_hamming", float("nan"))
        uk  = r.get("UKPSSR_hamming", float("nan"))
        gse = r.get("GSE51092_hamming", float("nan"))
        fmt = lambda x: f"{x:.3f}" if x == x else "—"
        cond, fp = r["condition"], r["attractor"]
        lines.append(f"| {cond} | {fp} | {fmt(ps)} | {fmt(uk)} | {fmt(gse)} |")
        for cohort, val in [("PRECISESADS", ps), ("UKPSSR", uk), ("GSE51092", gse)]:
            if val == val and (cohort not in best or val < best[cohort][2]):
                best[cohort] = (cond, fp, val)

    lines += [
        "",
        "### Attracteur le mieux corrélé par cohorte",
        "",
        "| Cohorte | Meilleur attracteur | Distance Hamming |",
        "|---|---|---|",
    ]
    for cohort, (cond, fp, dist) in best.items():
        lines.append(f"| {cohort} | {cond} — {fp} | {dist:.3f} |")

    # IFN signature test
    lines += [
        "",
        "## 4. Test hypothèse H2 — Signature IFN-high",
        "",
        "Vérification : le FP2 IFN-stimulé (sans Cell_Proliferation) correspond-il",
        "à la signature IFN-high de PRECISESADS ?",
        "",
    ]
    ifn_fp2_key = "IFN-stimulated|FP2"
    if ifn_fp2_key in states:
        ifn_nodes = {n: v for n, v in states[ifn_fp2_key].items()
                     if any(k in n for k in ["IFNA", "IFNB", "IFNG", "IFNAR", "IRF", "STAT1", "STAT2", "MX", "OAS", "ISG"])}
        lines += [
            "Nœuds IFN actifs dans IFN-stimulé FP2 :",
            "",
            "| Nœud | État |",
            "|---|---|",
        ]
        for node, val in sorted(ifn_nodes.items()):
            lines.append(f"| {node} | {'✓ Actif' if val else '○ Inactif'} |")

    lines += [""]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
