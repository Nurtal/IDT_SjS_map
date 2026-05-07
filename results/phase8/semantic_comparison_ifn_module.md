# Semantic comparison: MP vs asynchronous on IFN-I sub-network


Sub-network: `models/sbmlqual/v2/sjd_map_v2_ifn_module.bnet` (44 nodes), covering the
IFN-α/β/γ ligand binding, JAK/TYK kinases, STAT1/2 + IRF9 (ISGF3)
complex, the canonical ISG effectors (MX1/2, OAS1-3, OASL, ISG15,
IRF7, IFIT1/3, IFITM1) and the SOCS1/3 / USP18 negative-feedback loop.

Both solvers run on the same sub-bnet under two conditions:
**Naive** (all input ligands = 0) and **IFN-stim** (IFN-α/β/γ + IFNAR
= 1; HDAC3 = 1, KPNB1 = 1 in both conditions). For each node we
summarise the value across all attractors of a solver: `0` (always
inactive), `1` (always active), `*` (oscillating within an attractor
or differing across attractors).

## Summary

| Condition | MP attractors | Async attractors | Agreement | Disagreement examples |
|---|---|---|---|---|
| Naive | 1 | 2 | 43/44 | USP18 |
| IFN-stim | 1 | 2 | 43/44 | USP18 |

## Interpretation

Across the 44 nodes of the IFN-I sub-network and under both Naive
and IFN-stim conditions, MP and asynchronous semantics agree on
**43/44** node states. The single disagreement is on `USP18`, an
input self-loop (`USP18, USP18`) that the asynchronous solver
explores in both states (free input creates two attractor branches),
while MP propagates the default-0 input value. This disagreement
is a property of input-handling conventions, not of the cascade
dynamics.

Critically, the ISG output nodes (MX1/2, OAS1-3, ISG15, IRF7,
IFIT1/3, IFITM1) and the upstream ISGF3 complex are **oscillating
(`*`) in both semantics under IFN-stim**, confirming that the
trap-space dynamic reported on the full network is not an artefact
of the MP solver: classical asynchronous semantics produces the
same envelope of activation on the same module.

Per-node table: `results/phase8/semantic_comparison_ifn_module.csv`.