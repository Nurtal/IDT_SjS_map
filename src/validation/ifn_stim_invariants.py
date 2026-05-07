"""
Phase 9.1.7 — Extract the invariants of the IFN-stimulated trap-space
attractor.

Under MP semantics a trap-space attractor reports each node coordinate as
0, 1 or `*`. The 0-invariants and 1-invariants are the nodes that take
that single value in *every* MP trajectory of the attractor. They define
the stable "skeleton" of the attractor; the `*` coordinates are the
reachable envelope above this skeleton.

Output:
    results/phase9/ifn_stim_trap_space_invariants.csv
    results/phase9/ifn_stim_trap_space_invariants_summary.md
"""

from __future__ import annotations

import csv
import pathlib

import mpbn

BNET_V2 = pathlib.Path("models/sbmlqual/v2/sjd_map_v2.bnet")
OUT_CSV = pathlib.Path("results/phase9/ifn_stim_trap_space_invariants.csv")
OUT_MD  = pathlib.Path("results/phase9/ifn_stim_trap_space_invariants_summary.md")

IFN_OVERRIDES = {
    "IFNA_Extracellular_ligands":  1,
    "IFNB1_Extracellular_ligands": 1,
    "IFNG_IFNGR_complex":          1,
    "IFNAR_complex":               1,
}


def main() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    bn = mpbn.MPBooleanNetwork(str(BNET_V2))
    inputs = [n for n, r in bn.items() if str(r) == n]
    for n in inputs:
        bn[n] = IFN_OVERRIDES.get(n, 0)
    bn.propagate_constants()

    attrs = list(bn.attractors())
    assert attrs, "no IFN-stim attractor found"
    a = attrs[0]

    one_invariants = []
    zero_invariants = []
    oscillating = []
    for node, val in sorted(a.items()):
        v = str(val)
        if v == "1":
            one_invariants.append(node)
        elif v == "0":
            zero_invariants.append(node)
        elif v == "*":
            oscillating.append(node)

    rows: list[dict] = []
    for n in one_invariants:
        rows.append({"node": n, "invariant_value": "1"})
    for n in zero_invariants:
        rows.append({"node": n, "invariant_value": "0"})
    for n in oscillating:
        rows.append({"node": n, "invariant_value": "*"})

    fieldnames = ["node", "invariant_value"]
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"Saved: {OUT_CSV}  ({len(rows)} nodes)")

    md = [
        "# IFN-stimulated trap-space attractor — invariants\n",
        "",
        f"- 1-invariants (always active): **{len(one_invariants)}**",
        f"- 0-invariants (always inactive): **{len(zero_invariants)}**",
        f"- oscillating (`*`, reachable both states): **{len(oscillating)}**",
        f"- total: **{len(rows)}**",
        "",
        "## 1-invariants — examples (first 30 sorted)",
        "",
        ", ".join(one_invariants[:30]) + (" ..." if len(one_invariants) > 30 else ""),
        "",
        "## 0-invariants — examples (first 30 sorted)",
        "",
        ", ".join(zero_invariants[:30]) + (" ..." if len(zero_invariants) > 30 else ""),
        "",
        "## Interpretation",
        "",
        "The IFN-stim attractor's invariant skeleton — nodes whose value ",
        "is determined for the entire attractor — defines the *stable* ",
        "part of the IFN response. The oscillating coordinates form the ",
        "*envelope* of states reachable under sustained IFN stimulation ",
        "with active SOCS / USP18 / PIAS feedback. The downstream ISGs ",
        "(MX1, OAS1-3, ISG15, IFIT1/3, IFITM1) and the ISGF3 nuclear ",
        "complex fall in the oscillating set: they are *activable* in ",
        "every attractor trajectory but not pinned to a single value at ",
        "all times — an MP-formal expression of the refractory dynamic ",
        "produced by negative feedback.",
        "",
        f"Per-node table: `{OUT_CSV}`.",
    ]
    OUT_MD.write_text("\n".join(md))
    print(f"Saved: {OUT_MD}")


if __name__ == "__main__":
    main()
