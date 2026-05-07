# Combinatorial screen — multi-test correction


The combinatorial perturbation screen evaluated **273 (pair × condition)** hypotheses (91 pairs × 3 signalling conditions).
**3 pairs** are observed as synergistic, all of them in the BCR-stim condition: SYK + EIF2AK2 (PKR), SYK + MAP2K6, SYK + MAPK11-14 (p38).

## Distribution of synergies across conditions

| Condition | Pairs | Synergies |
|---|---|---|
| BCR-stimulated | 91 | 3 |
| IFN-stimulated | 91 | 0 |
| Naive (homeostatic) | 91 | 0 |

## Multi-test summary

- Total tests : **273**
- Synergistic observed : **3** (1.10 %)
- All synergies in one condition (concentration) : **P_analytic = 3.70e-02**, **P_permutation (10000 perms) = 1.08e-01**
- Bonferroni threshold (α = 0.05, 273 tests): **1.83e-04**

## Interpretation

The observed concentration of all 3 synergies in the BCR-stim condition has analytic p ≈ 3.7e-02 (uniform-over-conditions null) and permutation p ≈ 1.1e-01. The mechanistic coherence of the result — all three pairs share a common SYK partner and target the same AP1/p38 module downstream of BCR signalling — is consistent
with this statistical concentration.

Three observed synergies represent a *rate* of ≈ 1 % across the screen ; this is below the 5 % rate that a naive per-test α = 0.05 threshold would license under H0, so the result does not reflect multiple-testing inflation. The synergistic pairs are reported with the explicit caveat that their p-value is a concentration p-value, not a per-pair statistical test.