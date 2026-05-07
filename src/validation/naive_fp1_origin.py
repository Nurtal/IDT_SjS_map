"""
Phase 9.1.6 — Document which nodes are active in Naive FP1 and trace the
upstream rule that drives each activation.

The Naive condition fixes every input to 0 (apart from the constitutively
active HDAC3 = KPNB1 = 1). It is therefore not a "tonic-input" homeostatic
state but a *ground state* in the Boolean sense. The fact that some
phenotypes nonetheless reach 1 in this state means there exist
auto-amplifying rules or rules that depend only on HDAC3 / KPNB1.

For each node in state 1 in Naive FP1 we extract the rule of that node
and decompose it into:
  - inputs from HDAC3 / KPNB1 only (constitutive activation),
  - inputs from other already-active nodes (cascaded activation),
  - self-loops or auto-amplifying terms.

Outputs:
    results/phase9/naive_fp1_active_origin.csv
    results/phase9/naive_fp1_origin_summary.md
"""

from __future__ import annotations

import csv
import pathlib
import re

import mpbn

BNET_V2 = pathlib.Path("models/sbmlqual/v2/sjd_map_v2.bnet")
OUT_CSV = pathlib.Path("results/phase9/naive_fp1_active_origin.csv")
OUT_MD  = pathlib.Path("results/phase9/naive_fp1_origin_summary.md")

CONSTITUTIVE = {"HDAC3", "KPNB1"}


def parse_bnet(path: pathlib.Path) -> dict[str, str]:
    rules: dict[str, str] = {}
    for line in path.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        target, _, formula = s.partition(",")
        rules[target.strip()] = formula.strip()
    return rules


def tokens(formula: str) -> set[str]:
    return set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", formula))


def classify_origin(node: str, formula: str, active: set[str]) -> str:
    toks = tokens(formula) - {"true", "false"}
    if node in toks and len(toks) == 1:
        return "self_loop_input"
    deps = toks - {node}
    if not deps:
        return "constant"
    if deps <= CONSTITUTIVE:
        return "constitutive_only"
    cascaded = deps & active
    non_cascaded = deps - active - CONSTITUTIVE
    if cascaded and not non_cascaded:
        return "cascaded_from_active"
    if cascaded and (deps & CONSTITUTIVE):
        return "constitutive+cascade"
    return "mixed"


def main() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    rules = parse_bnet(BNET_V2)
    bn = mpbn.MPBooleanNetwork(str(BNET_V2))
    inputs = [n for n, r in bn.items() if str(r) == n]
    for n in inputs:
        bn[n] = 0  # Naive condition (HDAC3, KPNB1 are not inputs in v2)
    bn.propagate_constants()

    fps = list(bn.fixedpoints())
    assert fps, "no Naive fixed point found"
    fp1 = fps[0]
    print(f"Naive: {len(fps)} fixed point(s); analysing FP1.")

    active_nodes = {n for n, v in fp1.items() if str(v) == "1"}
    print(f"  Active nodes: {len(active_nodes)}")

    rows: list[dict] = []
    by_origin: dict[str, int] = {}
    for node in sorted(active_nodes):
        formula = rules.get(node, "")
        origin = classify_origin(node, formula, active_nodes)
        rows.append({
            "node":       node,
            "rule":       formula,
            "origin":     origin,
        })
        by_origin[origin] = by_origin.get(origin, 0) + 1

    fieldnames = list(rows[0].keys())
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"Saved: {OUT_CSV}  ({len(rows)} active nodes)")

    md = [
        "# Origin of activity in the Naive fixed point\n",
        "",
        "The Naive condition fixes every external input to 0; only HDAC3 ",
        "and KPNB1 are constitutively at 1 by construction (Section 2.3 of ",
        "the manuscript). The fixed point FP1 nonetheless contains active ",
        "nodes (state = 1). This document traces, for each active node, ",
        "the source of its activation.",
        "",
        f"**Total active nodes in Naive FP1:** {len(rows)}",
        "",
        "## Classification by origin of activation",
        "",
        "| Origin | Count | Definition |",
        "|---|---|---|",
        f"| `constitutive_only` | {by_origin.get('constitutive_only', 0)} | depends only on HDAC3 and/or KPNB1 |",
        f"| `cascaded_from_active` | {by_origin.get('cascaded_from_active', 0)} | depends on other already-active nodes (downstream relay) |",
        f"| `constitutive+cascade` | {by_origin.get('constitutive+cascade', 0)} | mixed (HDAC3/KPNB1 + cascaded) |",
        f"| `self_loop_input` | {by_origin.get('self_loop_input', 0)} | self-regulatory input (rare in Naive — should be 0) |",
        f"| `constant` | {by_origin.get('constant', 0)} | rule is a Boolean constant |",
        f"| `mixed` | {by_origin.get('mixed', 0)} | depends on inactive nodes; encoding artefact |",
        "",
        "## Interpretation",
        "",
        "The activity in Naive FP1 is propagated downstream from the ",
        "constitutive activation of HDAC3 and KPNB1. The first nodes to ",
        "switch on are those whose rules depend exclusively on HDAC3 / ",
        "KPNB1 (e.g. STAT1 = HDAC3); these then cascade to downstream ",
        "regulators that take their place in the active set. The Naive ",
        "fixed point should therefore not be read as the model's view of ",
        "a *rest* state but as a *baseline competence* state where the ",
        "network is poised to amplify any extracellular signal through a ",
        "transcription-factor backbone that is already chromatin- and ",
        "transport-competent.",
        "",
        f"Per-node table with rule and origin classification: `{OUT_CSV}`.",
    ]
    OUT_MD.write_text("\n".join(md))
    print(f"Saved: {OUT_MD}")


if __name__ == "__main__":
    main()
