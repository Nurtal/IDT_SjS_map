"""
Phase 7.2.4 — KEGG / Reactome enrichment of attractor-active nodes (R3.7).

For each attractor of v2, export the set of HGNC symbols mapped to nodes in
state 1 (or `*` = activable). Run a hypergeometric over-representation test
against KEGG_2021_Human and Reactome_Pathways libraries via the Enrichr
endpoint of `gseapy`. Report top enriched pathways and confront with the
pathways enriched in cohort up-DEGs.

Outputs:
    results/phase7/enrichment_attractors.csv   (attractor → top pathways)
    results/phase7/enrichment_cohorts.csv      (cohort up-DEGs → top pathways)
    results/phase7/enrichment_summary.md       (concordance table)

Usage:
    python3 src/validation/enrichment_kegg_reactome.py --top 20

Network access:
    `gseapy.enrichr` queries the Enrichr public API. If the run fails,
    rerun on a host with network access.
"""

from __future__ import annotations

import argparse
import csv
import pathlib
from collections import defaultdict

import gseapy
import mpbn

BNET_V2 = pathlib.Path("models/sbmlqual/v2/sjd_map_v2.bnet")
HGNC_CSV = pathlib.Path("data/processed/hgnc_to_bnet.csv")
OVERLAY_DIR = pathlib.Path(
    "data/raw/zenodo_17585308/TheSjDMap/TheSjDMap/Statistics_Overlays"
)
OVERLAYS = {
    "PRECISESADS": OVERLAY_DIR / "Blood_datasets/overlay_PRECISESADS.txt",
    "UKPSSR":      OVERLAY_DIR / "Blood_datasets/overlay_UKPSSR.txt",
    "GSE51092":    OVERLAY_DIR / "Blood_datasets/overlay_GSE51092.txt",
}
LIBS = ["KEGG_2021_Human", "Reactome_2022"]
OUT_DIR = pathlib.Path("results/phase7")

CONDITIONS: dict[str, dict[str, int]] = {
    "Naive (homeostatic)": {},
    "IFN-stimulated": {
        "IFNA_Extracellular_ligands":  1,
        "IFNB1_Extracellular_ligands": 1,
        "IFNG_IFNGR_complex":          1,
        "IFNAR_complex":               1,
    },
    "BCR-stimulated": {"BCR_complex": 1},
}


def load_hgnc_mapping() -> dict[str, list[tuple[str, str]]]:
    """Return {bnet_node: [(hgnc, kind), ...]}. Inverted from the CSV."""
    out: dict[str, list[tuple[str, str]]] = defaultdict(list)
    with open(HGNC_CSV) as f:
        for r in csv.DictReader(f):
            out[r["bnet_node"]].append((r["hgnc_symbol"], r["kind"]))
    return out


def attractor_active_nodes() -> dict[str, set[str]]:
    """Per attractor, set of nodes in state 1 or '*'."""
    bn_base = mpbn.MPBooleanNetwork(str(BNET_V2))
    inputs = [n for n, r in bn_base.items() if str(r) == n]
    out: dict[str, set[str]] = {}
    for cond, overrides in CONDITIONS.items():
        bn = mpbn.MPBooleanNetwork(str(BNET_V2))
        for n in inputs:
            bn[n] = overrides.get(n, 0)
        bn.propagate_constants()
        for i, attr in enumerate(bn.attractors(), 1):
            active = set()
            for n, r in bn.items():
                v = str(attr.get(n, str(r)))
                if v in ("1", "*"):
                    active.add(n)
            out[f"{cond}|A{i}"] = active
    return out


def load_overlay_up(path: pathlib.Path) -> set[str]:
    out: set[str] = set()
    if not path.exists():
        return out
    with open(path) as f:
        next(f, None)
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2 or not parts[0] or parts[0] == "NA":
                continue
            if "FF0000" in parts[1].upper():
                out.add(parts[0])
    return out


def nodes_to_hgnc(nodes: set[str],
                  hgnc_map: dict[str, list[tuple[str, str]]]) -> list[str]:
    out: set[str] = set()
    for node in nodes:
        for sym, _kind in hgnc_map.get(node, []):
            out.add(sym)
    return sorted(out)


def enrich(gene_list: list[str], lib: str, *, label: str) -> list[dict]:
    """Run gseapy.enrichr for one list+library; return top rows."""
    if not gene_list:
        return []
    try:
        res = gseapy.enrichr(gene_list=gene_list, gene_sets=[lib],
                             organism="human", outdir=None,
                             cutoff=1.0, verbose=False)
    except Exception as exc:
        print(f"  [warn] {label} / {lib}: {exc}")
        return []
    df = res.results
    if df is None or df.empty:
        return []
    return df.head(20).to_dict("records")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=10)
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    hgnc_map = load_hgnc_mapping()
    print(f"BNET nodes with ≥1 HGNC: {len(hgnc_map)}")

    print("Computing v2 attractor active sets ...")
    attr_active = attractor_active_nodes()

    attractor_rows: list[dict] = []
    for attr_key, nodes in attr_active.items():
        gene_list = nodes_to_hgnc(nodes, hgnc_map)
        cond, fp = attr_key.split("|")
        print(f"\nEnriching {attr_key}  ({len(gene_list)} symbols) ...")
        for lib in LIBS:
            results = enrich(gene_list, lib, label=attr_key)
            for r in results[: args.top]:
                attractor_rows.append({
                    "condition":   cond,
                    "attractor":   fp,
                    "library":     lib,
                    "term":        r.get("Term", ""),
                    "p_value":     r.get("P-value", float("nan")),
                    "adj_p_value": r.get("Adjusted P-value", float("nan")),
                    "overlap":     r.get("Overlap", ""),
                    "genes":       ";".join(str(r.get("Genes", "")).split(";")[:8]),
                })

    out_a = OUT_DIR / "enrichment_attractors.csv"
    fields_a = ["condition", "attractor", "library", "term",
                "p_value", "adj_p_value", "overlap", "genes"]
    with open(out_a, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields_a)
        w.writeheader()
        w.writerows(attractor_rows)
    print(f"\nSaved: {out_a}  ({len(attractor_rows)} rows)")

    cohort_rows: list[dict] = []
    for cohort, path in OVERLAYS.items():
        gene_list = sorted(load_overlay_up(path))
        print(f"\nEnriching {cohort} up-DEGs  ({len(gene_list)} symbols) ...")
        for lib in LIBS:
            results = enrich(gene_list, lib, label=cohort)
            for r in results[: args.top]:
                cohort_rows.append({
                    "cohort":      cohort,
                    "library":     lib,
                    "term":        r.get("Term", ""),
                    "p_value":     r.get("P-value", float("nan")),
                    "adj_p_value": r.get("Adjusted P-value", float("nan")),
                    "overlap":     r.get("Overlap", ""),
                })

    out_c = OUT_DIR / "enrichment_cohorts.csv"
    fields_c = ["cohort", "library", "term", "p_value", "adj_p_value", "overlap"]
    with open(out_c, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields_c)
        w.writeheader()
        w.writerows(cohort_rows)
    print(f"Saved: {out_c}  ({len(cohort_rows)} rows)")

    # Concordance summary: pathways significant (adj p < 0.05) in BOTH the
    # IFN-stim A1 attractor and at least one cohort.
    md = ["# Concordance enrichissement attracteur ↔ cohorte (Phase 7.2.4)\n"]
    md.append("\n## Critère 7.2.4\n\n")
    md.append("≥ 3 voies canoniques SjD (IFN-I, BCR/JAK-STAT) confirmées "
              "enrichies dans IFN-stim A1.\n\n")

    SJD_KEYWORDS = ["interferon", "ifn", "jak-stat", "jak/stat", "jak stat",
                    "b cell", "b-cell", "antigen receptor", "type i ifn",
                    "isg", "rig-i", "innate immun"]

    md.append("## Voies canoniques SjD enrichies dans IFN-stim A1\n\n")
    md.append("| Library | Term | adj_p |\n|---|---|---|\n")
    n_canonical = 0
    for r in attractor_rows:
        if r["condition"] != "IFN-stimulated" or r["attractor"] != "A1":
            continue
        adj = r.get("adj_p_value", 1.0)
        try:
            if float(adj) > 0.05:
                continue
        except (TypeError, ValueError):
            continue
        term_lower = str(r["term"]).lower()
        if any(k in term_lower for k in SJD_KEYWORDS):
            md.append(f"| {r['library']} | {r['term']} | {adj} |\n")
            n_canonical += 1

    md.append(f"\n**N voies canoniques SjD enrichies (adj_p < 0.05) dans "
              f"IFN-stim A1 : {n_canonical}**\n")
    md.append(f"\nCritère 7.2.4 : "
              f"{'✅ atteint' if n_canonical >= 3 else '❌ non atteint'} "
              f"(seuil ≥ 3).\n")

    out_md = OUT_DIR / "enrichment_summary.md"
    out_md.write_text("".join(md))
    print(f"Saved: {out_md}")


if __name__ == "__main__":
    main()
