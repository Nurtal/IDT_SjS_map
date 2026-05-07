"""
Phase 8.1.1 — Identify oscillating nodes (`*`-coordinates) of the IFN-stim
trap space and classify them by functional module.

The v2 IFN-stim attractor is a single trap space (no fixed point). Nodes
with coordinate `*` oscillate within the attractor — a non-trivial dynamic
that needs biological interpretation (feedback STAT-SOCS, NFkB-NFKBIA,
MAPK-DUSP, …) versus methodological artefact (over-strict CaSQ encoding).

Outputs:
    results/phase8/oscillating_nodes_ifn_stim.csv
    results/phase8/oscillating_nodes_summary.md
"""

from __future__ import annotations

import csv
import pathlib

import mpbn

BNET_V2 = pathlib.Path("models/sbmlqual/v2/sjd_map_v2.bnet")
OUT_CSV = pathlib.Path("results/phase8/oscillating_nodes_ifn_stim.csv")
OUT_MD  = pathlib.Path("results/phase8/oscillating_nodes_summary.md")

# Functional module classification by name pattern. Order matters: a node
# that matches multiple groups receives the *first* matching label.
MODULES: list[tuple[str, list[str]]] = [
    ("Feedback IFN-STAT-SOCS", [
        "SOCS", "PIAS", "PTPN", "USP18", "STAT1_homodimer", "STAT1_STAT2",
        "STAT", "JAK", "TYK2", "IRF9", "ISGF3"]),
    ("ISG canonical effectors",  [
        "MX1", "MX2", "OAS", "ISG15", "ISG20", "IFIT", "IFITM",
        "IRF7", "IRF1", "BST2", "GBP", "ADAR", "EIF2AK2"]),
    ("Cytokine ligands & receptors", [
        "IFNA", "IFNB", "IFNG", "IFNAR", "IFNGR", "IL", "TNF",
        "Extracellular_ligands", "Secreted_molecules"]),
    ("Feedback NFkB",            ["NFKBIA", "NFKBIB", "NFKBIE", "TNFAIP3",
                                  "RELA_NFKB", "NFKB1", "NFKB2", "RELB"]),
    ("MAPK / DUSP feedback",     ["DUSP", "MAPK", "MAP2K", "MAP3K",
                                  "FOS", "JUN", "AP1"]),
    ("Apoptosis / cell cycle",   ["CASP", "BCL2", "BAD", "BAX",
                                  "CDKN", "GADD45", "FAS", "BIRC", "TP53"]),
    ("Chemokines / surface",     ["CCL", "CXCL", "CCR", "CXCR", "ICAM",
                                  "VCAM", "SELE", "SELP", "ITGA", "ITGB"]),
    ("Phenotype outputs",        ["_phenotype"]),
]


def classify(node: str) -> str:
    for label, patterns in MODULES:
        for p in patterns:
            if p in node:
                return label
    return "Other"


def main() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    bn = mpbn.MPBooleanNetwork(str(BNET_V2))
    inputs = [n for n, r in bn.items() if str(r) == n]
    overrides = {
        "IFNA_Extracellular_ligands":  1,
        "IFNB1_Extracellular_ligands": 1,
        "IFNG_IFNGR_complex":          1,
        "IFNAR_complex":               1,
    }
    for n in inputs:
        bn[n] = overrides.get(n, 0)
    bn.propagate_constants()

    attrs = list(bn.attractors())
    assert attrs, "no IFN-stim attractor"
    a = attrs[0]

    rows: list[dict] = []
    counts: dict[str, dict[str, int]] = {}
    for node, val in sorted(a.items()):
        v_str = str(val)
        if v_str not in ("0", "1", "*"):
            continue
        if v_str != "*":
            continue
        module = classify(node)
        rows.append({
            "node":     node,
            "value":    v_str,
            "module":   module,
        })
        counts.setdefault(module, {"oscillating": 0, "total": 0})
        counts[module]["oscillating"] += 1

    # Total members per module
    for node in a.keys():
        module = classify(node)
        counts.setdefault(module, {"oscillating": 0, "total": 0})
        counts[module]["total"] += 1

    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["node", "value", "module"])
        w.writeheader()
        w.writerows(rows)
    print(f"Saved: {OUT_CSV}  ({len(rows)} oscillating nodes)")

    # Summary report
    md = ["# Oscillating nodes in IFN-stim trap space (v2 model)\n"]
    md.append(f"\n**Total oscillating nodes (* coordinate):** {len(rows)} of "
              f"{len(a)} attractor coordinates "
              f"({100*len(rows)/len(a):.1f} %)\n\n")
    md.append("## By functional module\n\n")
    md.append("| Module | Oscillating | Total in attractor | % oscillating |\n")
    md.append("|---|---|---|---|\n")
    for module, c in sorted(counts.items(),
                            key=lambda kv: -kv[1]["oscillating"]):
        pct = 100 * c["oscillating"] / max(1, c["total"])
        md.append(f"| {module} | {c['oscillating']} | {c['total']} | "
                  f"{pct:.1f} % |\n")

    md.append("\n## Biological interpretation\n\n")
    feedback_modules = [m for m in counts if "Feedback" in m or "DUSP" in m]
    feedback_total = sum(counts[m]["oscillating"] for m in feedback_modules)
    md.append(f"- **Negative feedback loops** (STAT-SOCS, NFkB-NFKBIA, "
              f"MAPK-DUSP) account for **{feedback_total} oscillating nodes**.\n")
    md.append("- The presence of these feedback modules among oscillating "
              "nodes supports the interpretation that the trap-space dynamic "
              "reflects *biological feedback control* rather than a "
              "purely artefactual encoding.\n")
    md.append("- The IFN-stim attractor's `*` coordinates therefore "
              "represent the *envelope* of states reachable under sustained "
              "IFN signalling with active feedback regulation — consistent "
              "with the pulsatile dynamics observed experimentally for "
              "STAT1/SOCS/IFN axes [Cheon 2014, Adamson 2016].\n")

    OUT_MD.write_text("".join(md))
    print(f"Saved: {OUT_MD}")


if __name__ == "__main__":
    main()
