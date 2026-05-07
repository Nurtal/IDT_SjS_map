"""
Phase 7.1.2 — Topological audit of the AP1/p38 control module.

Reviewers R1, R2, R4 raised the concern that the seven monogenic perturbations
that eliminate the SjD attractor in Phase 4 are concentrated on a single
linear chain (EIF2AK2 → MAP2K6 → MAPK11-14 → FOS/JUN → AP1) — possibly an
artefact of CaSQ encoding rather than a biological hierarchy of control.

This script tests three things:

    (1) For every node of the AP1/p38 chain and for a control set of comparable
        nodes (other phosphorylation cascades, hubs, output phenotypes), report
        in-degree, out-degree, betweenness and reachable-component sizes.

    (2) Walk upstream from MAPK11_12_13_14_phosphorylated up to depth 3 and list
        every regulator. Highlight whether the canonical TAK1 (MAP3K7) branch is
        present and whether it carries any biological input under default
        conditions.

    (3) Count parallel paths from each "module entry point" (TLR/RLR/IFN/BCR
        ligand inputs) to MAPK11-14 and to AP1_complex. Few parallel paths =
        the module is a bottleneck (R1 hypothesis confirmed); many parallel
        paths = the module aggregates several signals (biological hub).

Outputs:
    results/phase7/topology_ap1_p38.csv   per-node centrality table
    results/phase7/ap1_p38_upstream.csv   walk upstream from MAPK11-14
    docs/audit_ap1_p38.md                 narrative report
"""

from __future__ import annotations

import csv
import pathlib
import re

import networkx as nx

BNET    = pathlib.Path("models/sbmlqual/v1/sjd_map_reduced_clean.bnet")
OUT_DIR = pathlib.Path("results/phase7")
DOC     = pathlib.Path("docs/audit_ap1_p38.md")

MODULE_NODES = [
    "EIF2AK2_homodimer",
    "MAP2K6_phosphorylated",
    "MAPK11_12_13_14_phosphorylated",
    "FOS_phosphorylated",
    "JUN_phosphorylated",
    "AP1_complex",
]

# Comparable "control" nodes for centrality benchmarking
CONTROL_NODES = [
    # JAK/STAT cascade nodes
    "JAK1_phosphorylated",
    "STAT1_phosphorylated",
    "STAT1_STAT2_IRF9_complex_nucleus",
    # BCR cascade
    "BTK_phosphorylated",
    "SYK_phosphorylated",
    # NFkB
    "RELA_NFKB1_complex",
    # Other MAPKs (non-p38)
    "MAPK3_phosphorylated",
    "MAPK8_9_10_phosphorylated",
    # Output phenotypes (sinks)
    "Inflammation_phenotype",
    "B_Cell_Activation_Survival_phenotype",
    "T_Cell_Activation_Differentiation_phenotype",
]


def parse_bnet(path: pathlib.Path) -> dict[str, str]:
    rules: dict[str, str] = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line == "targets, factors":
                continue
            idx = line.find(", ")
            if idx == -1:
                continue
            rules[line[:idx]] = line[idx + 2:]
    return rules


def regulators(formula: str, all_nodes: set[str]) -> set[str]:
    """Tokenise a Boolean formula and return the set of recognised node names.

    Tokens that do not appear in `all_nodes` are dropped (they are typically
    constants 0/1 or names rewritten by deduplication).
    """
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", formula)
    return {t for t in tokens if t in all_nodes}


def build_graph(rules: dict[str, str]) -> nx.DiGraph:
    g = nx.DiGraph()
    g.add_nodes_from(rules.keys())
    nodes = set(rules.keys())
    for tgt, formula in rules.items():
        for src in regulators(formula, nodes):
            g.add_edge(src, tgt)
    return g


def upstream_walk(g: nx.DiGraph, start: str, depth: int = 3) -> list[dict]:
    """Return rows describing every ancestor of `start` up to `depth`."""
    rows: list[dict] = []
    visited = {start}
    frontier: dict[str, int] = {start: 0}
    while frontier:
        next_frontier: dict[str, int] = {}
        for node, d in frontier.items():
            if d >= depth:
                continue
            for parent in g.predecessors(node):
                if parent not in visited:
                    visited.add(parent)
                    next_frontier[parent] = d + 1
                    rows.append({
                        "ancestor":   parent,
                        "depth":      d + 1,
                        "child":      node,
                        "in_degree":  g.in_degree(parent),
                        "out_degree": g.out_degree(parent),
                    })
        frontier = next_frontier
    return rows


def parallel_paths(g: nx.DiGraph, source: str, target: str, cap: int = 50) -> int:
    """Count node-disjoint paths from source to target, up to `cap`.

    Uses NetworkX's max-flow on a unit-capacity vertex-split graph — for small
    `cap` this is fast even on 500-node graphs.
    """
    if source not in g or target not in g:
        return 0
    try:
        return min(nx.node_disjoint_paths(g, source, target, cutoff=cap).__length_hint__(), cap)
    except (nx.NetworkXNoPath, nx.NodeNotFound, AttributeError):
        try:
            paths = list(nx.node_disjoint_paths(g, source, target, cutoff=cap))
            return len(paths)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return 0


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DOC.parent.mkdir(parents=True, exist_ok=True)

    rules = parse_bnet(BNET)
    g = build_graph(rules)
    print(f"Graph: {g.number_of_nodes()} nodes, {g.number_of_edges()} edges")

    # ── (1) Centrality table ────────────────────────────────────────────────
    print("Computing betweenness ...")
    btw = nx.betweenness_centrality(g, k=min(150, g.number_of_nodes()), seed=0)

    rows: list[dict] = []
    for kind, group in [("ap1_p38", MODULE_NODES), ("control", CONTROL_NODES)]:
        for node in group:
            if node not in g:
                rows.append({"node": node, "kind": kind, "in_degree": -1,
                             "out_degree": -1, "betweenness": -1.0,
                             "ancestors": -1, "descendants": -1, "in_module": ""})
                continue
            rows.append({
                "node":         node,
                "kind":         kind,
                "in_degree":    g.in_degree(node),
                "out_degree":   g.out_degree(node),
                "betweenness":  round(btw.get(node, 0.0), 6),
                "ancestors":    len(nx.ancestors(g, node)),
                "descendants":  len(nx.descendants(g, node)),
                "in_module":    "1" if node in MODULE_NODES else "0",
            })

    centrality_csv = OUT_DIR / "topology_ap1_p38.csv"
    with open(centrality_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Saved: {centrality_csv}")

    # ── (2) Upstream walk from MAPK11-14 ────────────────────────────────────
    upstream_csv = OUT_DIR / "ap1_p38_upstream.csv"
    upstream = upstream_walk(g, "MAPK11_12_13_14_phosphorylated", depth=3)
    with open(upstream_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ancestor", "depth", "child",
                                          "in_degree", "out_degree"])
        w.writeheader()
        w.writerows(upstream)
    print(f"Saved: {upstream_csv}  ({len(upstream)} ancestors up to depth 3)")

    has_tak1 = any(r["ancestor"] == "MAP3K7_phosphorylated" for r in upstream)
    has_ask1 = any(r["ancestor"] == "MAP3K5_phosphorylated" for r in upstream)

    # ── (3) Parallel paths from input ligands to MAPK11-14 / AP1 ─────────────
    INPUT_LIGANDS = [
        "IFNA_Extracellular_ligands",
        "IFNB1_Extracellular_ligands",
        "IFNG_IFNGR_complex",
        "BCR_complex",
        "CpG_DNA_TLR9_complex",
        "LPS_CD14_TL4_LY96_complex",
    ]
    pp_rows: list[dict] = []
    for src in INPUT_LIGANDS:
        for tgt in ("MAPK11_12_13_14_phosphorylated", "AP1_complex",
                    "STAT1_phosphorylated"):
            if src in g and tgt in g:
                try:
                    paths = list(nx.node_disjoint_paths(g, src, tgt))
                    n_paths = len(paths)
                except (nx.NetworkXNoPath, nx.NodeNotFound):
                    n_paths = 0
            else:
                n_paths = 0
            pp_rows.append({"source": src, "target": tgt, "node_disjoint_paths": n_paths})

    pp_csv = OUT_DIR / "ap1_p38_parallel_paths.csv"
    with open(pp_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["source", "target", "node_disjoint_paths"])
        w.writeheader()
        w.writerows(pp_rows)
    print(f"Saved: {pp_csv}")

    # ── Narrative report ────────────────────────────────────────────────────
    module_rows = [r for r in rows if r["kind"] == "ap1_p38"]
    control_rows = [r for r in rows if r["kind"] == "control"]

    def _avg(rs: list[dict], k: str) -> float:
        vals = [r[k] for r in rs if r[k] != -1]
        return sum(vals) / len(vals) if vals else 0.0

    md = []
    md.append("# Audit topologique du module AP1/p38 (Phase 7.1.2)\n")
    md.append(f"\n**Réseau analysé :** `{BNET}` ({g.number_of_nodes()} nœuds, "
              f"{g.number_of_edges()} arêtes orientées)\n")
    md.append("\n## 1. Centralités\n")
    md.append("\n| Groupe | in-degree (moy) | out-degree (moy) | "
              "betweenness (moy) | ancestors (moy) | descendants (moy) |\n")
    md.append("|---|---|---|---|---|---|\n")
    md.append(f"| AP1/p38 ({len(module_rows)} nœuds) | "
              f"{_avg(module_rows, 'in_degree'):.1f} | "
              f"{_avg(module_rows, 'out_degree'):.1f} | "
              f"{_avg(module_rows, 'betweenness'):.4f} | "
              f"{_avg(module_rows, 'ancestors'):.1f} | "
              f"{_avg(module_rows, 'descendants'):.1f} |\n")
    md.append(f"| Contrôle ({len(control_rows)} nœuds) | "
              f"{_avg(control_rows, 'in_degree'):.1f} | "
              f"{_avg(control_rows, 'out_degree'):.1f} | "
              f"{_avg(control_rows, 'betweenness'):.4f} | "
              f"{_avg(control_rows, 'ancestors'):.1f} | "
              f"{_avg(control_rows, 'descendants'):.1f} |\n")

    md.append("\nDétails complets : `results/phase7/topology_ap1_p38.csv`.\n")

    md.append("\n## 2. Voie TAK1/MAP3K7 → p38\n")
    md.append(f"- MAP3K7_phosphorylated présent comme ancêtre de "
              f"MAPK11-14 (depth ≤ 3) : **{'OUI' if has_tak1 else 'NON'}**\n")
    md.append(f"- MAP3K5 (ASK1) présent : **{'OUI' if has_ask1 else 'NON'}**\n")
    md.append("\nLa voie canonique TLR/IL-1 → TRAF6 → TAK1 → MKK6 → p38 est "
              "donc " + ("intacte topologiquement" if has_tak1 else
              "absente — à reconstruire dans la v2") + ".\n")
    md.append(f"\nListe complète des ancêtres de MAPK11-14 (depth ≤ 3) : "
              f"`results/phase7/ap1_p38_upstream.csv` "
              f"({len(upstream)} entrées).\n")

    md.append("\n## 3. Chemins parallèles ligands → module\n")
    md.append("\nNombre de chemins nœud-disjoints depuis chaque ligand :\n\n")
    md.append("| Ligand | → MAPK11-14 | → AP1_complex | → STAT1-P (référence) |\n")
    md.append("|---|---|---|---|\n")
    for src in INPUT_LIGANDS:
        sub = {r["target"]: r["node_disjoint_paths"] for r in pp_rows if r["source"] == src}
        md.append(f"| {src} | {sub.get('MAPK11_12_13_14_phosphorylated', 0)} | "
                  f"{sub.get('AP1_complex', 0)} | "
                  f"{sub.get('STAT1_phosphorylated', 0)} |\n")

    md.append("\n## 4. Interprétation\n")
    md.append("\nLe module AP1/p38 est jugé **topologiquement central** si :\n"
              "1. la betweenness moyenne de ses 6 nœuds est ≥ celle du groupe "
              "de contrôle ; **et**\n"
              "2. au moins un ligand a > 1 chemins nœud-disjoints vers "
              "MAPK11-14 et > 1 vers AP1_complex (redondance).\n\n"
              "Sinon il est jugé **bottleneck linéaire** (artefact possible "
              "d'encodage CaSQ).\n")

    DOC.write_text("".join(md))
    print(f"Saved: {DOC}")


if __name__ == "__main__":
    main()
