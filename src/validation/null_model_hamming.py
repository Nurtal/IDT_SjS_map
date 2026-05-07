"""
Phase 7.2.2 — Null model permutation test for attractor↔cohort Hamming.

The Phase 3 report gave Hamming distances (0.755–0.964) without any null
distribution, so the reported "best-matching attractor" carried no
significance claim (R1.7, R3.1). This script computes:

  - the observed Hamming distance per attractor × cohort using the cleaner
    HGNC mapping (Phase 7.2.1);
  - a null distribution over 10 000 permutations of DEG directions, holding
    the set of mapped (gene, node) pairs fixed but randomising the +1/-1
    sign of each DEG;
  - an empirical one-sided p-value: P(Hamming_null ≤ Hamming_observed).

The mapping respects R3.5 (protein vs RNA): when computing the predicted
state for a DEG, we prefer the BNET node whose `kind` matches the assay type
(transcriptomic = `_rna` if available, otherwise the protein/complex form).

Outputs:
    results/phase7/attractor_cohort_distance_v2.csv
    figures/phase7/null_model_distribution.png

Usage:
    python3 src/validation/null_model_hamming.py [--n-permutations 10000]
"""

from __future__ import annotations

import argparse
import csv
import pathlib
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import mpbn  # noqa: E402
import numpy as np  # noqa: E402

BNET_V2 = pathlib.Path("models/sbmlqual/v2/sjd_map_v2.bnet")
HGNC_CSV = pathlib.Path("data/processed/hgnc_to_bnet.csv")
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

OUT_CSV = pathlib.Path("results/phase7/attractor_cohort_distance_v2.csv")
OUT_PNG = pathlib.Path("figures/phase7/null_model_distribution.png")

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

# kinds preferred for transcriptomic comparison: `rna` first, fallback to
# protein/complex. Phosphorylated/nucleus forms are ignored unless they are
# the only option (because mRNA up does not directly imply phosphorylation).
RNA_PREF_ORDER = ["rna", "protein", "complex_member", "secreted",
                  "secreted_ligand", "cell_localised", "active",
                  "phosphorylated", "homodimer", "nucleus", "empty",
                  "small_molecule", "cell_surface_receptor"]


def load_overlay(path: pathlib.Path) -> dict[str, int]:
    out: dict[str, int] = {}
    if not path.exists():
        return out
    with open(path) as f:
        next(f, None)
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2 or not parts[0] or parts[0] == "NA":
                continue
            sym, color = parts[0], parts[1]
            if "FF0000" in color.upper():
                out[sym] = +1
            elif "0000FF" in color.upper():
                out[sym] = -1
    return out


def load_hgnc_mapping() -> dict[str, list[tuple[str, str]]]:
    """Return {hgnc_symbol: [(bnet_node, kind), ...]}."""
    out: dict[str, list[tuple[str, str]]] = defaultdict(list)
    with open(HGNC_CSV) as f:
        for r in csv.DictReader(f):
            out[r["hgnc_symbol"]].append((r["bnet_node"], r["kind"]))
    return out


def best_node(nodes: list[tuple[str, str]]) -> str | None:
    """Pick the most appropriate node form for a DEG (R3.5 protein vs RNA).

    For transcriptomic data, prefer `_rna`; otherwise fall back to the
    canonical protein form. Skip the phosphorylated/nucleus forms unless no
    other option exists, since DEG direction does not imply post-translational
    state.
    """
    if not nodes:
        return None
    by_kind: dict[str, str] = {}
    for node, kind in nodes:
        # First entry of a kind wins; deterministic order from the CSV.
        by_kind.setdefault(kind, node)
    for kind in RNA_PREF_ORDER:
        if kind in by_kind:
            return by_kind[kind]
    return nodes[0][0]


def compute_attractor_states() -> dict[str, dict[str, int]]:
    """Return {attractor_key: {node: 0/1}} from v2.

    Trap-space coordinates `*` are treated as 1 (activable in some
    trajectory of the attractor) — consistent with the phenotype reporting
    of compute_attractors_v2.py.
    """
    bn_base = mpbn.MPBooleanNetwork(str(BNET_V2))
    inputs = [n for n, r in bn_base.items() if str(r) == n]
    out: dict[str, dict[str, int]] = {}
    for cond_name, overrides in CONDITIONS.items():
        bn = mpbn.MPBooleanNetwork(str(BNET_V2))
        for n in inputs:
            bn[n] = overrides.get(n, 0)
        bn.propagate_constants()
        attrs = list(bn.attractors())
        for i, attr in enumerate(attrs, 1):
            state = {}
            for n, r in bn.items():
                v = attr.get(n, str(r))
                v_str = str(v)
                if v_str == "1" or v_str == "*":
                    state[n] = 1
                else:
                    state[n] = 0
            out[f"{cond_name}|A{i}"] = state
    return out


def compute_hamming(state: dict[str, int],
                    pairs: list[tuple[str, int]]) -> tuple[int, int]:
    """Return (n_mismatches, n_pairs) for a list of (node, expected) pairs."""
    miss = 0
    for node, expected in pairs:
        if state.get(node, 0) != expected:
            miss += 1
    return miss, len(pairs)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-permutations", type=int, default=10_000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)

    print("Loading HGNC mapping ...")
    hgnc_map = load_hgnc_mapping()

    print("Computing v2 attractor states ...")
    states = compute_attractor_states()
    print(f"  {len(states)} attractors")

    rng = np.random.default_rng(args.seed)
    rows: list[dict] = []
    fig, axes = plt.subplots(len(OVERLAYS), 1, figsize=(8, 2.5 * len(OVERLAYS)),
                             sharex=False)
    if len(OVERLAYS) == 1:
        axes = [axes]

    for ax, (cohort, path) in zip(axes, OVERLAYS.items()):
        print(f"\nCohort: {cohort}")
        deg = load_overlay(path)
        # Build the (node, expected_state) list from the DEG.
        pairs_observed: list[tuple[str, int]] = []
        signs: list[int] = []
        for sym, direction in deg.items():
            nodes = hgnc_map.get(sym, [])
            node = best_node(nodes)
            if node is None:
                continue
            expected = 1 if direction == +1 else 0
            pairs_observed.append((node, expected))
            signs.append(direction)
        n_mapped = len(pairs_observed)
        if n_mapped == 0:
            print(f"  no mapped DEGs — skipping")
            continue
        print(f"  {n_mapped} mapped (gene, node) pairs")

        # Permute the directions of the SAME mapped genes.
        signs_arr = np.array(signs, dtype=np.int8)
        # Pre-extract attractor states for mapped nodes for vectorisation
        attr_keys = list(states.keys())
        node_idx: dict[str, int] = {n: i for i, n in enumerate(
            sorted({p[0] for p in pairs_observed}))}
        idx_per_pair = np.array([node_idx[p[0]] for p in pairs_observed],
                                dtype=np.int32)
        # Build per-attractor activation vector aligned to node_idx
        n_nodes_used = len(node_idx)
        attr_activation = np.zeros((len(attr_keys), n_nodes_used), dtype=np.int8)
        for ai, k in enumerate(attr_keys):
            for n, ni in node_idx.items():
                attr_activation[ai, ni] = states[k].get(n, 0)

        for ai, attr_key in enumerate(attr_keys):
            cond, fp = attr_key.split("|")
            activation = attr_activation[ai, idx_per_pair]
            # Observed expected = (signs_arr == +1) → 1; (signs_arr == -1) → 0.
            expected = (signs_arr == +1).astype(np.int8)
            obs_miss = int(np.sum(activation != expected))
            obs_h = obs_miss / n_mapped

            # Permutation: re-shuffle signs of the SAME genes.
            null_h = np.empty(args.n_permutations, dtype=np.float32)
            perm_signs = signs_arr.copy()
            for p in range(args.n_permutations):
                rng.shuffle(perm_signs)
                perm_expected = (perm_signs == +1).astype(np.int8)
                miss = int(np.sum(activation != perm_expected))
                null_h[p] = miss / n_mapped

            p_val = float(np.mean(null_h <= obs_h))
            mean_null = float(np.mean(null_h))
            std_null = float(np.std(null_h))
            z = (obs_h - mean_null) / std_null if std_null > 0 else float("nan")

            rows.append({
                "cohort":      cohort,
                "condition":   cond,
                "attractor":   fp,
                "n_pairs":     n_mapped,
                "hamming":     round(obs_h, 4),
                "null_mean":   round(mean_null, 4),
                "null_std":    round(std_null, 4),
                "z_score":     round(z, 3),
                "p_value":     round(p_val, 4),
            })

            # Plot null for the best attractor (lowest observed hamming) per
            # cohort
        ax.set_title(f"{cohort} — null Hamming (10k perms) — best attractors")

        # Find best (lowest) per cohort
        cohort_rows = [r for r in rows if r["cohort"] == cohort]
        cohort_rows.sort(key=lambda r: r["hamming"])
        # Re-do permutation for the best attractor for plotting
        best = cohort_rows[0]
        ai = attr_keys.index(f"{best['condition']}|{best['attractor']}")
        activation = attr_activation[ai, idx_per_pair]
        null_h_plot = np.empty(args.n_permutations, dtype=np.float32)
        perm_signs = signs_arr.copy()
        for p in range(args.n_permutations):
            rng.shuffle(perm_signs)
            perm_expected = (perm_signs == +1).astype(np.int8)
            miss = int(np.sum(activation != perm_expected))
            null_h_plot[p] = miss / n_mapped
        ax.hist(null_h_plot, bins=50, color="grey", alpha=0.7)
        ax.axvline(best["hamming"], color="red", linewidth=2,
                   label=f"obs={best['hamming']:.3f}, p={best['p_value']:.3g}")
        ax.set_xlabel(f"Null Hamming ({best['condition']} {best['attractor']})")
        ax.set_ylabel("count")
        ax.legend(loc="best", fontsize=8)

    plt.tight_layout()
    fig.savefig(OUT_PNG, dpi=130)
    print(f"\nSaved: {OUT_PNG}")

    fieldnames = ["cohort", "condition", "attractor", "n_pairs", "hamming",
                  "null_mean", "null_std", "z_score", "p_value"]
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"Saved: {OUT_CSV}  ({len(rows)} attractor × cohort rows)")


if __name__ == "__main__":
    main()
