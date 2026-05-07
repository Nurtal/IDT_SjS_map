"""
Phase 9.1.4 — Reformat KEGG/Reactome enrichment as top-5 pathways per
attractor for the SI table.

Output:
    results/phase9/enrichment_top5_per_attractor.csv
"""

from __future__ import annotations

import csv
import pathlib
from collections import defaultdict

ENR_CSV = pathlib.Path("results/phase7/enrichment_attractors.csv")
OUT_CSV = pathlib.Path("results/phase9/enrichment_top5_per_attractor.csv")


def main() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    by_attractor: dict[tuple[str, str], list[dict]] = defaultdict(list)
    with open(ENR_CSV) as f:
        for r in csv.DictReader(f):
            key = (r["condition"], r["attractor"])
            by_attractor[key].append(r)

    rows_out: list[dict] = []
    for (cond, attr), rs in sorted(by_attractor.items()):
        # Sort by adjusted p-value
        rs_sorted = sorted(rs, key=lambda r: float(r.get("adj_p_value", 1.0)
                                                   if r.get("adj_p_value") not in ("", "nan")
                                                   else 1.0))
        for rank, r in enumerate(rs_sorted[:5], 1):
            rows_out.append({
                "condition":  cond,
                "attractor":  attr,
                "rank":       rank,
                "library":    r["library"],
                "term":       r["term"],
                "p_value":    r["p_value"],
                "adj_p_value": r["adj_p_value"],
                "overlap":    r["overlap"],
            })

    fieldnames = list(rows_out[0].keys())
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows_out)
    print(f"Saved: {OUT_CSV}  ({len(rows_out)} rows = "
          f"{len(by_attractor)} attractors × 5)")


if __name__ == "__main__":
    main()
