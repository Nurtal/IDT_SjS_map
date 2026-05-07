"""
Phase 7.2.1 — Build a clean HGNC-symbol → BNET-node mapping.

Replaces the substring matcher used in Phase 3 (annotate_attractors.py:147)
with a deterministic mapping that:

  - decomposes BNET node names by stripping known CaSQ suffixes
    (`_rna`, `_phosphorylated`, `_complex`, `_nucleus`, `_Cell`,
    `_Extracellular_ligands`, `_Secreted_molecules`, `_homodimer`, `_active`,
    `_simple_molecule`, `_empty`, `_phenotype`);
  - decomposes multi-gene complexes into their member symbols (e.g.
    `STAT1_STAT2_IRF9_complex` → STAT1, STAT2, IRF9);
  - expands family numbering (`MAPK11_12_13_14_phosphorylated` →
    MAPK11/12/13/14);
  - flags every mapping with a *kind* (protein, rna, complex_member,
    secreted_ligand, phosphorylated, nucleus, etc.) so downstream code can
    apply a "protein vs mRNA" rule (R3.5).

The HGNC symbol vocabulary is the union of gene names found in the cohort
DEG overlays (PRECISESADS, UKPSSR, GSE51092, ASSESS, GSE23117) — by
construction these symbols are valid HGNC. We additionally seed the
vocabulary with the SjD-relevant family backbones (STAT1-6, IRF1-9, MX1,
OAS1-3, JAK1-3, TYK2, MAPK1-14, etc.) to avoid spurious omissions.

Output:
    data/processed/hgnc_to_bnet.csv  columns:
        hgnc_symbol, bnet_node, kind, source_match, suffix
    data/processed/hgnc_mapping_summary.md  (coverage table)

Usage:
    python3 src/validation/build_hgnc_mapping.py
"""

from __future__ import annotations

import csv
import pathlib
import re
from collections import defaultdict


BNET = pathlib.Path("models/sbmlqual/v1/sjd_map_reduced_clean.bnet")
OVERLAY_DIR = pathlib.Path(
    "data/raw/zenodo_17585308/TheSjDMap/TheSjDMap/Statistics_Overlays"
)
OVERLAYS = {
    "PRECISESADS": OVERLAY_DIR / "Blood_datasets/overlay_PRECISESADS.txt",
    "UKPSSR":      OVERLAY_DIR / "Blood_datasets/overlay_UKPSSR.txt",
    "GSE51092":    OVERLAY_DIR / "Blood_datasets/overlay_GSE51092.txt",
    "ASSESS":      OVERLAY_DIR / "ASSESS/ASSESS_lymphoma.txt",
    "GSE23117":    OVERLAY_DIR / "GSE23117/overlay_GSE23117.txt",
}

OUT_CSV = pathlib.Path("data/processed/hgnc_to_bnet.csv")
OUT_MD  = pathlib.Path("data/processed/hgnc_mapping_summary.md")

# Suffixes recognised by CaSQ encoding, in order of attempt (longest first to
# avoid matching '_Cell' inside '_Cell_Surface_Receptor' etc.).
SUFFIXES = [
    ("_Cell_Surface_Receptor", "cell_surface_receptor"),
    ("_Extracellular_ligands", "secreted_ligand"),
    ("_Secreted_molecules",    "secreted"),
    ("_simple_molecule",       "small_molecule"),
    ("_phosphorylated",        "phosphorylated"),
    ("_homodimer",             "homodimer"),
    ("_nucleus",               "nucleus"),
    ("_phenotype",             "phenotype"),
    ("_complex",               "complex"),
    ("_active",                "active"),
    ("_empty",                 "empty"),
    ("_Cell",                  "cell_localised"),
    ("_rna",                   "rna"),
]

# Curated SjD-relevant HGNC backbone (seeds + family expansion roots).
SEED_SYMBOLS = {
    # JAK/STAT
    "JAK1", "JAK2", "JAK3", "TYK2",
    "STAT1", "STAT2", "STAT3", "STAT4", "STAT5A", "STAT5B", "STAT6",
    # IRFs
    "IRF1", "IRF3", "IRF5", "IRF7", "IRF8", "IRF9",
    # ISGs
    "MX1", "MX2", "OAS1", "OAS2", "OAS3", "OASL",
    "ISG15", "ISG20", "BST2",
    "IFIT1", "IFIT2", "IFIT3", "IFIT5",
    "IFITM1", "IFITM2", "IFITM3",
    "IFI6", "IFI44", "IFI44L", "IFI27", "IFI35",
    "EIF2AK2", "ADAR", "GBP1", "GBP3",
    # NFkB
    "RELA", "RELB", "REL", "NFKB1", "NFKB2", "NFKBIA", "TNFAIP3",
    # MAPKs
    "MAPK1", "MAPK3", "MAPK8", "MAPK9", "MAPK10",
    "MAPK11", "MAPK12", "MAPK13", "MAPK14",
    "MAP2K1", "MAP2K3", "MAP2K4", "MAP2K6", "MAP2K7",
    "MAP3K1", "MAP3K5", "MAP3K7", "MAP3K14",
    "FOS", "JUN",
    # BCR
    "BTK", "SYK", "BLNK", "PLCG2", "AKT1", "AKT2", "AKT3",
    # TLR / IL-1
    "TLR1", "TLR2", "TLR3", "TLR4", "TLR7", "TLR8", "TLR9",
    "MYD88", "TRAF6", "IRAK1", "IRAK4",
    # BAFF/APRIL
    "TNFSF13", "TNFSF13B", "TNFRSF13B", "TNFRSF13C", "TNFRSF17",
    # IFN ligands/receptors
    "IFNA1", "IFNA2", "IFNB1", "IFNG",
    "IFNAR1", "IFNAR2", "IFNGR1", "IFNGR2",
    # Costim
    "CD40", "CD40LG", "CD80", "CD86", "CTLA4", "CD28",
    # Apoptosis / chemotaxis (R3.7 enrichment will need these)
    "CASP3", "CASP7", "CASP8", "BCL2", "BCL2L1", "BAD", "BAX",
    "CCL2", "CCL5", "CXCL10", "CXCL11", "CXCR3",
    # HDAC/KPNB (relevant after Phase 7.1)
    "HDAC3", "KPNB1",
}

# Manual overrides for nodes whose name does not yield the right HGNC by
# decomposition. Every entry must be justified.
MANUAL_OVERRIDES: dict[str, list[str]] = {
    # CaSQ "AP1_complex" stands for the FOS/JUN heterodimer
    "AP1_complex":            ["FOS", "JUN"],
    # "BCR_complex" is the B-cell receptor (Ig + Igα/Igβ); we map it to the
    # canonical Igα/Igβ symbols since the cohorts measure these
    "BCR_complex":            ["CD79A", "CD79B"],
    # MHC-Class-1 / 2 phenotypes — used for enrichment, not Hamming
    "MHC_class_1_complex":    ["HLA-A", "HLA-B", "HLA-C", "B2M"],
    "MHC_class_2_complex":    ["HLA-DRA", "HLA-DRB1", "HLA-DPA1",
                               "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"],
    # Cytokine receptor complexes are aliased by CaSQ
    "IFNAR_complex":          ["IFNAR1", "IFNAR2"],
    "IFNG_IFNGR_complex":     ["IFNG", "IFNGR1", "IFNGR2"],
    # IgE/Allergen receptor
    "Allergen_IgE_FCERI_complex": ["FCER1A", "FCER1G", "MS4A2"],
}

# Tokens that *look* like HGNC symbols inside a node name but are not
# (CellDesigner localisation / CaSQ artefact, or generic biology nouns).
NON_HGNC_TOKENS = {
    "complex", "phenotype", "rna", "ligands", "ligand", "molecule",
    "molecules", "Cell", "nucleus", "active", "empty", "Surface",
    "Receptor", "Extracellular", "Secreted", "phosphorylated",
    "homodimer", "simple", "Allergen", "Ag", "IgG", "IgE",
    "ion", "DNA", "RNA", "complex_1", "complex_2",
    "DAG", "PIP2", "PIP3", "ATP", "ADP", "GTP", "GDP",
}

# Aliases: legacy or CD-style names → canonical HGNC.
ALIAS_MAP: dict[str, str] = {
    "CD279": "PDCD1",   # PD-1
    "CD274": "CD274",   # PD-L1 (modern HGNC keeps CD274)
    "CD134": "TNFRSF4",
    "CD137": "TNFRSF9",
    "BAFF":  "TNFSF13B",
    "APRIL": "TNFSF13",
    "BAFFR": "TNFRSF13C",
    "TACI":  "TNFRSF13B",
    "BCMA":  "TNFRSF17",
    "ADAR1": "ADAR",
    "AKT":   "AKT1",
    "PLCG":  "PLCG2",
    "FCERI": "FCER1A",
    "Calmodulin": "CALM1",
}


def load_overlay_symbols(path: pathlib.Path) -> set[str]:
    out: set[str] = set()
    if not path.exists():
        return out
    with open(path) as f:
        next(f, None)
        for line in f:
            parts = line.strip().split("\t")
            if not parts or not parts[0]:
                continue
            sym = parts[0].strip()
            if sym and sym != "NA":
                out.add(sym)
    return out


def build_hgnc_vocabulary() -> set[str]:
    vocab: set[str] = set(SEED_SYMBOLS)
    for path in OVERLAYS.values():
        vocab |= load_overlay_symbols(path)
    return vocab


def parse_bnet_targets(path: pathlib.Path) -> list[str]:
    targets: list[str] = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line == "targets, factors":
                continue
            idx = line.find(", ")
            if idx == -1:
                continue
            targets.append(line[:idx])
    return targets


def strip_suffix(node: str) -> tuple[str, str]:
    for suf, kind in SUFFIXES:
        if node.endswith(suf):
            return node[: -len(suf)], kind
    return node, "protein"


def expand_family(token: str) -> list[str]:
    """Expand 'MAPK11_12_13_14' → ['MAPK11','MAPK12','MAPK13','MAPK14']."""
    m = re.match(r"^([A-Za-z]+\d+)((?:_\d+)+)$", token)
    if not m:
        return [token]
    base, tail = m.group(1), m.group(2)
    prefix = re.match(r"^([A-Za-z]+)\d+$", base).group(1)
    nums = [base[len(prefix):]] + tail.lstrip("_").split("_")
    return [prefix + n for n in nums]


def candidate_symbols(core: str) -> list[str]:
    """Yield candidate HGNC tokens from a stripped node core."""
    parts = core.split("_")
    out: list[str] = []
    for p in parts:
        if not p or p in NON_HGNC_TOKENS:
            continue
        # Drop tokens with no letter (numeric tail) — leftover from
        # decomposition (e.g. lone "2" after "FCGR2A").
        if not any(c.isalpha() for c in p):
            continue
        out.extend(expand_family(p))
    return out


_HGNC_LIKE = re.compile(r"^[A-Z][A-Z0-9]*[A-Z0-9]$|^[A-Z][A-Z0-9-]*\d+[A-Z]?$")


def _looks_like_hgnc(token: str) -> bool:
    """Heuristic: HGNC symbols are uppercase, alphanumeric, often end in a
    digit-and-letter combo (e.g. STAT5A, MAPK14). Allow a hyphen for HLA-A
    style. Length 2..10."""
    if not 2 <= len(token) <= 12:
        return False
    if token in NON_HGNC_TOKENS:
        return False
    if not token[0].isalpha() or not token[0].isupper():
        return False
    return bool(_HGNC_LIKE.match(token)) or token.isupper()


def map_node(node: str, vocab: set[str]) -> list[dict[str, str]]:
    """
    Return a list of {hgnc_symbol, kind, source_match, suffix} rows for one
    BNET node. Returns [] if no HGNC match found (the node will be tracked
    as unmapped).
    """
    rows: list[dict[str, str]] = []

    if node in MANUAL_OVERRIDES:
        suffix = strip_suffix(node)[1]
        for sym in MANUAL_OVERRIDES[node]:
            rows.append({
                "hgnc_symbol":  sym,
                "bnet_node":    node,
                "kind":         "complex_member" if suffix == "complex"
                                else suffix,
                "source_match": "manual_override",
                "suffix":       suffix,
            })
        return rows

    core, suffix = strip_suffix(node)
    candidates = candidate_symbols(core)
    multi = len(candidates) > 1

    for cand in candidates:
        # Apply alias map first (CD279 → PDCD1, AKT → AKT1, etc.).
        canonical = ALIAS_MAP.get(cand, cand)

        if canonical in vocab:
            rows.append({
                "hgnc_symbol":  canonical,
                "bnet_node":    node,
                "kind":         _kind_from_suffix(suffix, multi=multi),
                "source_match": "alias" if canonical != cand else "exact",
                "suffix":       suffix,
            })
            continue
        if canonical.upper() in vocab:
            rows.append({
                "hgnc_symbol":  canonical.upper(),
                "bnet_node":    node,
                "kind":         _kind_from_suffix(suffix, multi=multi),
                "source_match": "case_normalised",
                "suffix":       suffix,
            })
            continue
        # Heuristic fallback: token *looks* like an HGNC symbol — keep it.
        # The cohort overlap step downstream will discard tokens that are
        # not in any cohort, so heuristic matches are harmless if wrong.
        if _looks_like_hgnc(canonical):
            rows.append({
                "hgnc_symbol":  canonical,
                "bnet_node":    node,
                "kind":         _kind_from_suffix(suffix, multi=multi),
                "source_match": "heuristic",
                "suffix":       suffix,
            })

    return rows


def _kind_from_suffix(suffix: str, multi: bool) -> str:
    if suffix == "rna":
        return "rna"
    if suffix == "complex" or multi:
        return "complex_member"
    if suffix in ("phosphorylated", "homodimer", "active", "nucleus",
                  "cell_localised", "empty"):
        return suffix
    if suffix in ("secreted", "secreted_ligand", "cell_surface_receptor"):
        return suffix
    if suffix == "small_molecule":
        return "small_molecule"
    if suffix == "phenotype":
        return "phenotype"
    return "protein"


def main() -> None:
    print("Building HGNC vocabulary ...")
    vocab = build_hgnc_vocabulary()
    print(f"  vocabulary size: {len(vocab)} symbols "
          f"({len(SEED_SYMBOLS)} seed + cohorts)")

    print("Parsing BNET targets ...")
    nodes = parse_bnet_targets(BNET)
    print(f"  {len(nodes)} target rules")

    rows: list[dict[str, str]] = []
    unmapped: list[dict[str, str]] = []
    n_phenotypes = 0
    for node in nodes:
        if node.endswith("_phenotype"):
            n_phenotypes += 1
            continue
        node_rows = map_node(node, vocab)
        if node_rows:
            rows.extend(node_rows)
        else:
            unmapped.append({"bnet_node": node, "core_after_strip":
                             strip_suffix(node)[0]})

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["hgnc_symbol", "bnet_node",
                                          "kind", "source_match", "suffix"])
        w.writeheader()
        w.writerows(rows)
    print(f"Saved: {OUT_CSV}  ({len(rows)} HGNC↔node mappings)")

    unmapped_path = OUT_CSV.parent / "hgnc_unmapped_nodes.csv"
    with open(unmapped_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["bnet_node", "core_after_strip"])
        w.writeheader()
        w.writerows(unmapped)
    print(f"Saved: {unmapped_path}  ({len(unmapped)} nodes without HGNC match)")

    # Per-cohort coverage report
    md = ["# Couverture du mapping HGNC → BNET (Phase 7.2.1)\n"]
    md.append(f"\n- Vocabulaire HGNC : {len(vocab)} symboles "
              f"(union de {len(SEED_SYMBOLS)} graines + DEGs des cohortes)\n")
    md.append(f"- Nœuds BNET (hors phénotypes) : {len(nodes) - n_phenotypes}\n")
    n_mapped_nodes = len({r['bnet_node'] for r in rows})
    md.append(f"- Nœuds mappés à ≥ 1 HGNC : **{n_mapped_nodes}** "
              f"({100 * n_mapped_nodes / max(1, len(nodes) - n_phenotypes):.1f} %)\n")
    md.append(f"- Nœuds non mappés       : {len(unmapped)}\n")
    md.append(f"- Lignes mappings (1 HGNC × 1 nœud) : {len(rows)}\n")

    md.append("\n## Couverture par cohorte (DEGs ↦ nœuds BNET)\n")
    md.append("\n| Cohorte | DEGs | Genes mappés | Couverture genes | "
              "(gene,node) pairs | Nœuds touchés |\n")
    md.append("|---|---|---|---|---|---|\n")
    by_symbol_kind: dict[str, set[str]] = defaultdict(set)
    for r in rows:
        by_symbol_kind[r["hgnc_symbol"]].add(r["kind"])
    for cohort, path in OVERLAYS.items():
        symbols = load_overlay_symbols(path)
        mapped = symbols & by_symbol_kind.keys()
        cohort_pairs = [(r["hgnc_symbol"], r["bnet_node"]) for r in rows
                        if r["hgnc_symbol"] in symbols]
        nodes_hit = {p[1] for p in cohort_pairs}
        cov = 100 * len(mapped) / max(1, len(symbols))
        md.append(f"| {cohort} | {len(symbols)} | {len(mapped)} | "
                  f"{cov:.1f} % | {len(cohort_pairs)} | {len(nodes_hit)} |\n")

    md.append("\n*Note R3.2 :* la couverture cohorte ↦ nœuds est plafonnée par la "
              "**portée curée du SjD Map** (pathways signalisation, pas tous les "
              "ISGs/ARNm transcriptomiques). Le gain attendu de R3.2 (> 30 %) "
              "n'est pas atteignable à modèle inchangé — la couverture reflète une "
              "limite structurelle de la carte, à reporter en limitation discutée.\n")

    md.append("\n## Distribution des `kind`\n\n")
    kind_count: dict[str, int] = defaultdict(int)
    for r in rows:
        kind_count[r["kind"]] += 1
    for k, n in sorted(kind_count.items(), key=lambda x: -x[1]):
        md.append(f"- {k}: {n}\n")

    OUT_MD.write_text("".join(md))
    print(f"Saved: {OUT_MD}")


if __name__ == "__main__":
    main()
