"""
Phase 7.1.1 — Build v2 Boolean network with IFN-I cascade unblocked.

The v1 BNET contains two rules that block the canonical IFN-I → ISGF3 → ISG
cascade when input nodes are at their default 0 state:

  - `STAT1 = HDAC3` (HDAC3 input = 0 → STAT1 protein never expressed)
  - `STAT1_STAT2_IRF9_complex_nucleus = ... & KPNB1`
    (KPNB1/importin-β input = 0 → ISGF3 never reaches the nucleus)

Both HDAC3 and KPNB1 are constitutively active in immune cells (HDAC3 is a
ubiquitous nuclear deacetylase; KPNB1 is the canonical importin-β1). The
CaSQ encoding inherits them as input nodes from the SjD Map's CellDesigner
representation but their biological default is 1, not 0.

This script produces a v2 BNET that overrides these two rules to constants
(`HDAC3 = 1`, `KPNB1 = 1`). All other rules are preserved verbatim.

The list of changes is logged to `models/sbmlqual/v2/changes.csv`.

Usage:
    python3 src/conversion/build_v2_model.py
"""

from __future__ import annotations

import csv
import pathlib

V1   = pathlib.Path("models/sbmlqual/v1/sjd_map_reduced_clean.bnet")
V2   = pathlib.Path("models/sbmlqual/v2/sjd_map_v2.bnet")
LOG  = pathlib.Path("models/sbmlqual/v2/changes.csv")

CONSTITUTIVE_INPUTS = {
    "HDAC3": "1",
    "KPNB1": "1",
}


def main() -> None:
    if not V1.exists():
        raise SystemExit(f"v1 BNET not found: {V1}")

    V2.parent.mkdir(parents=True, exist_ok=True)

    changes: list[dict[str, str]] = []
    out_lines: list[str] = []
    out_lines.append("# v2: HDAC3 and KPNB1 set to 1 (constitutive in immune cells)\n")
    out_lines.append("# See docs/audit_logique_v2.md for rationale.\n")

    with open(V1) as f:
        for line in f:
            stripped = line.rstrip("\n")
            if not stripped.strip() or stripped.startswith("#"):
                out_lines.append(stripped + "\n")
                continue
            if stripped == "targets, factors":
                out_lines.append(stripped + "\n")
                continue
            idx = stripped.find(", ")
            if idx == -1:
                out_lines.append(stripped + "\n")
                continue
            target  = stripped[:idx]
            formula = stripped[idx + 2:]
            if target in CONSTITUTIVE_INPUTS:
                new_formula = CONSTITUTIVE_INPUTS[target]
                changes.append({
                    "target": target,
                    "v1_formula": formula,
                    "v2_formula": new_formula,
                    "rationale": "constitutively active in immune cells",
                })
                out_lines.append(f"{target}, {new_formula}\n")
            else:
                out_lines.append(stripped + "\n")

    V2.write_text("".join(out_lines))
    print(f"Wrote: {V2}")

    with open(LOG, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["target", "v1_formula", "v2_formula", "rationale"])
        w.writeheader()
        w.writerows(changes)
    print(f"Wrote: {LOG}")
    print(f"Rules changed: {len(changes)}")
    for c in changes:
        print(f"  {c['target']}: {c['v1_formula']} -> {c['v2_formula']}")


if __name__ == "__main__":
    main()
