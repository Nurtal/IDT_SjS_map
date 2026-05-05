"""
Phase 0.4 — Reproduction des statistiques topologiques publiées.

Charge le SBML/SBGN-PD (ou le SBML-qual produit par CaSQ) et compare
les métriques aux valeurs publiées dans Silva-Saffar et al. 2026 :
  - Carte complète : 829 nœuds, 598 interactions
  - Carte réduite  : 412 nœuds, 692 arêtes

Identifie également les 5 hubs topologiques attendus :
  STAT1, STAT1/STAT2/IRF9, RELA/NFKB1, Inflammation, Chemotaxis/Infiltration

Usage :
    python src/validation/topological_stats.py --sbml data/raw/<fichier>.xml \
        [--expected-nodes 412] [--expected-edges 692] [--out docs/audit_topologique.md]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import NamedTuple

import networkx as nx


EXPECTED_HUBS = [
    "Inflammation",
    "STAT1 homodimer",
    "STAT1/STAT2/IRF9",
    "RELA/NFKB1",
    "Chemotaxis/Infiltration",
]

TERMINAL_PHENOTYPES = [
    "MHC Class I Activation",
    "MHC Class II Activation",
    "T Cell Activation/Differentiation",
    "B Cell Activation/Survival",
    "Cell Proliferation/Survival",
    "Inflammation",
    "Chemotaxis/Infiltration",
    "Angiogenesis",
    "Lymphoid Organ Development",
    "Apoptosis",
    "Regulated Necrosis",
    "Matrix Degradation",
    "Fibrosis",
    "Phagocytosis",
]


class TopologyReport(NamedTuple):
    n_nodes: int
    n_edges: int
    top10_hubs_degree: list[tuple[str, int]]
    hub_presence: dict[str, bool]
    phenotype_presence: dict[str, bool]


def load_sbml_as_graph(sbml_path: Path) -> nx.DiGraph:
    """Parse un fichier SBML ou SBML-qual et retourne un DiGraph NetworkX."""
    try:
        import libsbml
    except ImportError:
        sys.exit("Erreur : python-libsbml non installé. Voir docs/setup.md.")

    reader = libsbml.SBMLReader()
    doc = reader.readSBMLFromFile(str(sbml_path))

    if doc.getNumErrors(libsbml.LIBSBML_SEV_ERROR) > 0:
        for i in range(doc.getNumErrors()):
            e = doc.getError(i)
            if e.getSeverity() >= libsbml.LIBSBML_SEV_ERROR:
                print(f"SBML error : {e.getMessage()}", file=sys.stderr)
        sys.exit("Fichier SBML invalide.")

    G = nx.DiGraph()
    model = doc.getModel()

    if model is None:
        sys.exit("Aucun modèle trouvé dans le SBML.")

    # SBML classique : species = nœuds, reactions = arêtes
    for i in range(model.getNumSpecies()):
        sp = model.getSpecies(i)
        name = sp.getName() or sp.getId()
        G.add_node(name, id=sp.getId())

    for i in range(model.getNumReactions()):
        rxn = model.getReaction(i)
        for j in range(rxn.getNumReactants()):
            src = model.getSpecies(rxn.getReactant(j).getSpecies())
            src_name = src.getName() or src.getId()
            for k in range(rxn.getNumProducts()):
                tgt = model.getSpecies(rxn.getProduct(k).getSpecies())
                tgt_name = tgt.getName() or tgt.getId()
                G.add_edge(src_name, tgt_name)

    return G


def analyze(G: nx.DiGraph) -> TopologyReport:
    deg = dict(G.degree())
    top10 = sorted(deg.items(), key=lambda x: x[1], reverse=True)[:10]
    node_names = set(G.nodes())
    hub_presence = {h: h in node_names for h in EXPECTED_HUBS}
    phenotype_presence = {p: p in node_names for p in TERMINAL_PHENOTYPES}
    return TopologyReport(
        n_nodes=G.number_of_nodes(),
        n_edges=G.number_of_edges(),
        top10_hubs_degree=top10,
        hub_presence=hub_presence,
        phenotype_presence=phenotype_presence,
    )


def write_report(
    report: TopologyReport,
    expected_nodes: int,
    expected_edges: int,
    out_path: Path,
) -> None:
    delta_n = report.n_nodes - expected_nodes
    delta_e = report.n_edges - expected_edges
    pct_n = abs(delta_n) / expected_nodes * 100
    pct_e = abs(delta_e) / expected_edges * 100

    lines = [
        "# Audit topologique — SjD Map",
        "",
        "## Statistiques globales",
        "",
        f"| Métrique | Observé | Attendu | Écart |",
        f"|---|---|---|---|",
        f"| Nœuds | {report.n_nodes} | {expected_nodes} | {delta_n:+d} ({pct_n:.1f} %) |",
        f"| Arêtes | {report.n_edges} | {expected_edges} | {delta_e:+d} ({pct_e:.1f} %) |",
        "",
    ]

    status_n = "✓ OK" if pct_n <= 1.0 else f"⚠ Écart > 1 % ({pct_n:.1f} %)"
    status_e = "✓ OK" if pct_e <= 1.0 else f"⚠ Écart > 1 % ({pct_e:.1f} %)"
    lines += [f"Nœuds : {status_n}", f"Arêtes : {status_e}", ""]

    lines += [
        "## Top-10 nœuds par degré total",
        "",
        "| Rang | Nœud | Degré |",
        "|---|---|---|",
    ]
    for rank, (name, d) in enumerate(report.top10_hubs_degree, 1):
        marker = " ★" if name in EXPECTED_HUBS else ""
        lines.append(f"| {rank} | {name}{marker} | {d} |")
    lines.append("")

    lines += ["## Présence des hubs topologiques attendus", ""]
    for hub, present in report.hub_presence.items():
        status = "✓ présent" if present else "✗ ABSENT"
        lines.append(f"- **{hub}** : {status}")
    lines.append("")

    lines += ["## Présence des 14 phénotypes terminaux", ""]
    for phen, present in report.phenotype_presence.items():
        status = "✓ présent" if present else "✗ ABSENT"
        lines.append(f"- {phen} : {status}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")
    print(f"Rapport écrit dans {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit topologique SjD Map")
    parser.add_argument("--sbml", required=True, type=Path, help="Fichier SBML/SBGN-PD en entrée")
    parser.add_argument("--expected-nodes", type=int, default=412)
    parser.add_argument("--expected-edges", type=int, default=692)
    parser.add_argument("--out", type=Path, default=Path("docs/audit_topologique.md"))
    args = parser.parse_args()

    if not args.sbml.exists():
        sys.exit(f"Fichier introuvable : {args.sbml}")

    print(f"Chargement du SBML : {args.sbml}")
    G = load_sbml_as_graph(args.sbml)
    report = analyze(G)

    print(f"  Nœuds : {report.n_nodes}  (attendu : {args.expected_nodes})")
    print(f"  Arêtes : {report.n_edges}  (attendu : {args.expected_edges})")
    print(f"  Top hub : {report.top10_hubs_degree[0]}")

    write_report(report, args.expected_nodes, args.expected_edges, args.out)


if __name__ == "__main__":
    main()
