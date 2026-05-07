"""
Phase 7.5.1 — Non-regression test: ISG activability under IFN-stim (R1.6, R2.1).

The Phase 7.1.1 correction (HDAC3=1, KPNB1=1) must result in at least 3
canonical ISGs being activable (state ∈ {1, '*'}) in the IFN-stimulated
attractor of v2. A drift below this threshold means the IFN cascade has
been re-blocked by an unintended rule edit.
"""

from __future__ import annotations

import pathlib

import mpbn

BNET_V2 = pathlib.Path(__file__).resolve().parent.parent / \
          "models/sbmlqual/v2/sjd_map_v2.bnet"

CANONICAL_ISGS = ("MX1", "OAS1", "ISG15_Cell")


def test_isgs_activable_under_ifn() -> None:
    assert BNET_V2.exists(), f"v2 BNET missing: {BNET_V2}"
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
    assert len(attrs) >= 1, "no IFN-stim attractor"

    for isg in CANONICAL_ISGS:
        assert any(str(a.get(isg, 0)) in ("1", "*") for a in attrs), (
            f"ISG {isg} is not activable in any IFN-stim attractor"
        )


if __name__ == "__main__":
    test_isgs_activable_under_ifn()
    print("PASS")
