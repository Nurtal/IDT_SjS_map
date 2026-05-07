"""
Phase 7.5.1 — Non-regression test: null-model significance (R1.6, R3.1).

The IFN-stim attractor of v2 must match the three blood cohorts
(PRECISESADS, UKPSSR, GSE51092) significantly better than chance under a
1 000-permutation null model (we use 1k here to keep the test fast; the
manuscript reports 10k). A drift above p > 0.05 on any blood cohort means
the model has lost its IFN-driven concordance.
"""

from __future__ import annotations

import csv
import pathlib

import mpbn
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
BNET_V2 = ROOT / "models/sbmlqual/v2/sjd_map_v2.bnet"
HGNC_CSV = ROOT / "data/processed/hgnc_to_bnet.csv"
OVERLAY_DIR = ROOT / (
    "data/raw/zenodo_17585308/TheSjDMap/TheSjDMap/Statistics_Overlays/"
    "Blood_datasets"
)
COHORTS = {
    "PRECISESADS": OVERLAY_DIR / "overlay_PRECISESADS.txt",
    "UKPSSR":      OVERLAY_DIR / "overlay_UKPSSR.txt",
    "GSE51092":    OVERLAY_DIR / "overlay_GSE51092.txt",
}
P_THRESHOLD = 0.05
N_PERMUTATIONS = 1_000

RNA_PREF_ORDER = ("rna", "protein", "complex_member", "secreted",
                  "secreted_ligand", "cell_localised", "active",
                  "phosphorylated", "homodimer", "nucleus", "empty",
                  "small_molecule", "cell_surface_receptor")


def _load_overlay(path: pathlib.Path) -> dict[str, int]:
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


def _hgnc_map() -> dict[str, list[tuple[str, str]]]:
    out: dict[str, list[tuple[str, str]]] = {}
    with open(HGNC_CSV) as f:
        for r in csv.DictReader(f):
            out.setdefault(r["hgnc_symbol"], []).append(
                (r["bnet_node"], r["kind"])
            )
    return out


def _best_node(nodes: list[tuple[str, str]]) -> str | None:
    if not nodes:
        return None
    by_kind = {}
    for node, kind in nodes:
        by_kind.setdefault(kind, node)
    for kind in RNA_PREF_ORDER:
        if kind in by_kind:
            return by_kind[kind]
    return nodes[0][0]


def _ifn_state() -> dict[str, int]:
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
    state = {}
    for n, r in bn.items():
        v = str(a.get(n, str(r)))
        state[n] = 1 if v in ("1", "*") else 0
    return state


def test_blood_cohort_significance() -> None:
    state = _ifn_state()
    hgnc = _hgnc_map()
    rng = np.random.default_rng(0)

    for cohort, path in COHORTS.items():
        deg = _load_overlay(path)
        pairs = []
        signs = []
        for sym, direction in deg.items():
            node = _best_node(hgnc.get(sym, []))
            if node is None:
                continue
            pairs.append(node)
            signs.append(direction)
        signs_arr = np.array(signs, dtype=np.int8)
        activation = np.array([state.get(n, 0) for n in pairs], dtype=np.int8)
        expected = (signs_arr == +1).astype(np.int8)
        n = len(pairs)
        obs_h = float(np.mean(activation != expected))

        null_h = np.empty(N_PERMUTATIONS, dtype=np.float32)
        perm = signs_arr.copy()
        for i in range(N_PERMUTATIONS):
            rng.shuffle(perm)
            null_h[i] = float(np.mean(activation != (perm == +1).astype(np.int8)))
        p = float(np.mean(null_h <= obs_h))
        assert p < P_THRESHOLD, (
            f"{cohort}: p = {p:.3f} (n={n}, obs={obs_h:.3f}); "
            f"IFN-stim concordance has degraded"
        )


if __name__ == "__main__":
    test_blood_cohort_significance()
    print("PASS")
