"""
Sanitize a CaSQ-generated BNET file so node names are pyboolnet-compatible.

pyboolnet requires node names matching [A-Za-z_][A-Za-z0-9_]* — no spaces,
slashes, commas, parentheses, dots, etc.

Strategy:
1. Parse all (target, formula) pairs, collecting raw node names.
2. Build a collision-free mapping: raw_name -> sanitized_name.
3. Re-write every formula by replacing tokens (longest match first to avoid
   partial replacements like 'STAT1' matching inside 'STAT1/STAT2').
4. Deduplicate rules, keeping the longer formula when the same sanitized name
   appears twice (artifact of CaSQ comma-names like 'CD80,86').

Usage:
    python src/conversion/sanitize_bnet.py \
        --input  models/sbmlqual/v1/sjd_map_reduced.bnet \
        --output models/sbmlqual/v1/sjd_map_reduced_clean.bnet \
        --map    data/processed/bnet_name_map.csv
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


def sanitize(name: str) -> str:
    n = re.sub(r"[^A-Za-z0-9_]", "_", name)
    n = re.sub(r"_+", "_", n)
    n = n.strip("_")
    if n and n[0].isdigit():
        n = "n" + n
    return n or "unnamed"


def parse_bnet(path: Path) -> list[tuple[str, str]]:
    """Return list of (target, formula) pairs, skipping header/comments."""
    rules: list[tuple[str, str]] = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line == "targets, factors":
                continue
            idx = line.find(", ")
            if idx == -1:
                continue
            target = line[:idx]
            formula = line[idx + 2:]
            rules.append((target, formula))
    return rules


def build_name_map(raw_names: list[str]) -> dict[str, str]:
    """Build raw→sanitized map, resolving collisions by appending a counter."""
    seen: dict[str, int] = {}
    mapping: dict[str, str] = {}
    for raw in raw_names:
        s = sanitize(raw)
        if s in seen:
            seen[s] += 1
            s = f"{s}_{seen[s]}"
        else:
            seen[s] = 0
        mapping[raw] = s
    return mapping


def replace_tokens(formula: str, mapping: dict[str, str]) -> str:
    """
    Replace raw node names with sanitized names in a formula string.

    Sort by length descending so that 'STAT1/STAT2/IRF9' is replaced before
    the partial match 'STAT1/STAT2' or 'STAT1'.
    """
    for raw in sorted(mapping, key=len, reverse=True):
        new = mapping[raw]
        if raw == new:
            continue
        pattern = r"(?<![A-Za-z0-9_])" + re.escape(raw) + r"(?![A-Za-z0-9_])"
        formula = re.sub(pattern, new, formula)
    return formula


def main() -> None:
    parser = argparse.ArgumentParser(description="Sanitize CaSQ BNET for pyboolnet")
    parser.add_argument("--input",  type=Path, default=Path("models/sbmlqual/v1/sjd_map_reduced.bnet"))
    parser.add_argument("--output", type=Path, default=Path("models/sbmlqual/v1/sjd_map_reduced_clean.bnet"))
    parser.add_argument("--map",    type=Path, default=Path("data/processed/bnet_name_map.csv"))
    parser.add_argument("--collisions", type=Path, default=Path("data/processed/sanitize_collisions.csv"),
                        help="CSV listing raw_target collisions resolved by deduplication "
                             "(audit for Phase 7.1.3 / R1.5)")
    args = parser.parse_args()

    if not args.input.exists():
        sys.exit(f"Input not found: {args.input}")

    rules = parse_bnet(args.input)
    raw_targets = [t for t, _ in rules]

    # Collect all raw node names appearing in targets and formulas
    all_raw: set[str] = set(raw_targets)
    for _, formula in rules:
        # Tokenize formula: extract identifiers (may contain illegal chars)
        # We use a broad pattern matching runs of non-operator characters
        for tok in re.findall(r"[^\s&|!()\[\]]+", formula):
            all_raw.add(tok)

    # Build name map
    name_map = build_name_map(sorted(all_raw))

    # Deduplicate: keep one rule per sanitized target (prefer longer formula).
    # Track every collision so the audit report can quantify how many raw rules
    # were dropped by sanitisation (R1.5).
    deduped: dict[str, str] = {}
    raw_targets_per_san: dict[str, list[str]] = {}
    formulas_per_san: dict[str, list[tuple[str, str]]] = {}
    for raw_target, raw_formula in rules:
        san_target = name_map[raw_target]
        san_formula = replace_tokens(raw_formula, name_map)
        raw_targets_per_san.setdefault(san_target, []).append(raw_target)
        formulas_per_san.setdefault(san_target, []).append((raw_target, san_formula))
        if san_target not in deduped or len(san_formula) > len(deduped[san_target]):
            deduped[san_target] = san_formula

    collisions_rows: list[dict[str, str]] = []
    for san_target, entries in formulas_per_san.items():
        if len(entries) <= 1:
            continue
        kept_formula = deduped[san_target]
        for raw_target, san_formula in entries:
            collisions_rows.append({
                "sanitized_target": san_target,
                "raw_target":       raw_target,
                "formula":          san_formula,
                "kept":             "1" if san_formula == kept_formula else "0",
                "n_raw_targets":    str(len(entries)),
            })

    # Write output
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        f.write("targets, factors\n")
        for target in sorted(deduped):
            f.write(f"{target}, {deduped[target]}\n")

    # Write name map CSV
    args.map.parent.mkdir(parents=True, exist_ok=True)
    with open(args.map, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["raw_name", "sanitized_name"])
        for raw, san in sorted(name_map.items()):
            w.writerow([raw, san])

    # Write collisions CSV
    args.collisions.parent.mkdir(parents=True, exist_ok=True)
    with open(args.collisions, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["sanitized_target", "raw_target",
                                          "formula", "kept", "n_raw_targets"])
        w.writeheader()
        w.writerows(collisions_rows)

    # Summary
    phenotypes = [t for t in deduped if "phenotype" in t.lower()]
    collisions = sum(1 for r, s in name_map.items() if r != s)
    n_dropped = sum(1 for r in collisions_rows if r["kept"] == "0")
    n_collided = len({r["sanitized_target"] for r in collisions_rows})
    print(f"Rules:        {len(deduped)}")
    print(f"Name maps:    {len(name_map)}  ({collisions} renamed)")
    print(f"Phenotypes:   {len(phenotypes)}")
    print(f"Collisions:   {n_collided} sanitized targets received >1 raw rule")
    print(f"Rules lost:   {n_dropped} raw rules discarded by deduplication")
    print(f"Audit CSV:    {args.collisions}")
    for p in sorted(phenotypes):
        print(f"  {p}")


if __name__ == "__main__":
    main()
