"""
Phase 7.5.1 — Non-regression test: v2 attractor counts (R1.6).

The v2 BNET (HDAC3=1, KPNB1=1) must yield:
  - Naive (homeostatic): 2 fixed points
  - IFN-stimulated: 0 fixed points, 1 trap-space attractor
  - BCR-stimulated: 2 fixed points

A drift in any of these counts indicates a structural change in the model
(e.g. an unintended rule edit) and should fail the test.
"""

from __future__ import annotations

import pathlib

import mpbn

BNET_V2 = pathlib.Path(__file__).resolve().parent.parent / \
          "models/sbmlqual/v2/sjd_map_v2.bnet"

CONDITIONS: dict[str, dict[str, int]] = {
    "Naive (homeostatic)": ({}, 2, 2),
    "IFN-stimulated": ({
        "IFNA_Extracellular_ligands":  1,
        "IFNB1_Extracellular_ligands": 1,
        "IFNG_IFNGR_complex":          1,
        "IFNAR_complex":               1,
    }, 0, 1),
    "BCR-stimulated": ({"BCR_complex": 1}, 2, 2),
}


def _setup(overrides: dict[str, int]) -> mpbn.MPBooleanNetwork:
    bn = mpbn.MPBooleanNetwork(str(BNET_V2))
    inputs = [n for n, r in bn.items() if str(r) == n]
    for n in inputs:
        bn[n] = overrides.get(n, 0)
    bn.propagate_constants()
    return bn


def test_attractor_counts() -> None:
    assert BNET_V2.exists(), f"v2 BNET missing: {BNET_V2}"
    for cond, (overrides, expected_fps, expected_attrs) in CONDITIONS.items():
        bn = _setup(overrides)
        fps = list(bn.fixedpoints())
        attrs = list(bn.attractors())
        assert len(fps) == expected_fps, (
            f"{cond}: expected {expected_fps} fixed points, got {len(fps)}"
        )
        assert len(attrs) == expected_attrs, (
            f"{cond}: expected {expected_attrs} attractors, got {len(attrs)}"
        )


if __name__ == "__main__":
    test_attractor_counts()
    print("PASS")
