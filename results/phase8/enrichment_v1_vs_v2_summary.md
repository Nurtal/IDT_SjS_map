# Differential enrichment v1 vs v2 IFN-stim attractor

- v1 active nodes : 72 (→ 53 HGNC)
- v2 active nodes : 231 (→ 133 HGNC)
- Δ (v2 − v1)     : 159 nodes (80 genes)

## Pathway terms classified

| Kind | Description | N |
|---|---|---|
| stable  | significant in v1 *and* v2 | 16 |
| v2_new  | significant in v2, *not* in v1 | 4 |
| v1_only | significant in v1, *not* in v2 (regression) | 44 |
| neither | not significant in either | 0 |

## Canonical SjD IFN pathways — comparison

| Term | v1 adj_p | v2 adj_p | Verdict |
|---|---|---|---|
| JAK-STAT signaling pathway | 1.30e-28 | 4.51e-26 | stable |
| Interferon Signaling R-HSA-913531 | 1.85e-10 | 3.13e-86 | stable |
| Interferon Alpha/Beta Signaling R-HSA-909733 | — | 2.55e-63 | v2-only |
| Interferon Gamma Signaling R-HSA-877300 | — | 3.60e-50 | v2-only |

## Interpretation

The v2 enrichment of canonical IFN pathways is the *direct*
consequence of releasing HDAC3 and KPNB1 from their default-0
encoding: ISG output nodes (MX1, OAS1-3, ISG15, IRF7, IFIT1/3)
become activable, producing a coherent pathway signature
(internal-consistency check). The v1 enrichment, by contrast,
captures only the upstream JAK/STAT signalling that was already
active independently of HDAC3/KPNB1.

This differential establishes that the v2 corrected model
produces an *internally-consistent* IFN signature — necessary
but not sufficient for biological validation; the cohort-level
Hamming/AUROC tests provide the latter.
