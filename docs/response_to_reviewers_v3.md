# Response to reviewers

We thank the four reviewers for their thoughtful and constructive evaluations. The recommended revisions are addressed point by point below. Each reviewer recommendation is identified by the reviewer number (R1 boolean modelling, R2 immuno-clinician, R3 bioinformatics, R4 pharmacology / drug discovery) and the section number under which it was raised in the report. Pointers to the corresponding text or supporting file in the revised manuscript follow each response.

A summary of the principal changes:

- **Tables 2 and 3** are extended with the multi-test correction (Benjamini-Hochberg), bootstrap CI for all five cohorts, class-composition columns (n_up, n_down, up:down ratio, coverage_%) and explicit baseline rows for every cohort.
- **Section 1** introduces the lymphomagenic risk in SjD and the Soret 2021 molecular stratification.
- **Section 3.3** discusses the BH correction on the cohort × attractor tests and the cluster-aware reading of the cohort concordance.
- **Section 3.5** adds a multi-test correction for the combinatorial screen with concentration-based and permutation-based p-values.
- **Section 3.7** distinguishes filgotinib / baricitinib / tofacitinib pharmacologically, defines ESSDAI in a footnote, and explicitly states the anti-IFNAR-alone insufficiency message implied by the anifrolumab simulation.
- **Section 4.2** distinguishes the two interpretations of `*` (single-cell oscillation vs population-level variability).
- **Section 4.4** is substantially expanded with: SYK inhibitor selectivity discussion, PKR re-framed as an orphan target requiring *de novo* development rather than repositioning, BAFF/APRIL gap explicit, IL-14α-Tg as the preferred preclinical model for the lymphomagenic dimension, untestable-combination disclosure.
- **Section 4.7** adds an explicit blood-vs-salivary-gland tissue boundary statement.
- **Section 4.10** documents the parameter configurations tried for `pystablemotifs` and modular partitioning as future work.
- **New SI files** (Phase 9): `naive_fp1_active_origin.csv`, `ifn_stim_trap_space_invariants.csv`, `enrichment_top5_per_attractor.csv`, `combinatorial_multi_test.csv`, `table2_extended.csv`, `table3_extended.csv`, and the documented `stable_motifs_status.md`.

---

## Reviewer 1 — Boolean modelling and executable semantics

**R1.3.1 — Stable motifs / pystablemotifs parameters and modular partitioning.**
We tested four parameter configurations of the BNetToPrime backend: `max_simulate_size` ∈ {default, 0, 10, 20} crossed with `max_in_degree` ∈ {default, 5, 10}; each exceeded the 180-second budget. The CaSQ-derived BNET has a heavy-tailed in-degree distribution (several nodes with > 20 regulators) which dominates the prime-implicant cost, so reducing `max_in_degree` truncates the search rather than reducing it. We document this and identify modular partitioning [Klamt2018, Naldi2017] as the most promising path forward in Section 4.10 of the manuscript and in `docs/stable_motifs_status.md`.

**R1.3.2 — Cost of an exhaustive combinatorial screen.**
Section 3.5 was extended with a multi-test footprint of the targeted screen (273 tests, 3 synergies, concentration p ≈ 0.04 analytic / 0.11 permutation; `results/phase9/combinatorial_multi_test_summary.md`). Running an exhaustive 2-pair screen across all 508 dynamic targets would require ≈ 2-3 hours of CPU and is identified as a feasible future extension, but is not required to support the present claims because the targeted screen is a superset of the pharmacologically relevant pairs and the synergistic hits cluster mechanistically rather than randomly.

**R1.3.3 — Origin of activity in the Naive fixed point.**
We trace the 45 active nodes of Naive FP1 to their rule and classify them by source: 1 node depends only on HDAC3 / KPNB1 (constitutive), 22 are cascaded from already-active nodes, 2 are constants, and 20 fall in a "mixed" class whose rule depends on inactive nodes (an encoding artefact we document). The full per-node classification is in `results/phase9/naive_fp1_active_origin.csv` with the summary `results/phase9/naive_fp1_origin_summary.md`. The Naive condition is reframed in Section 3.2 as a *baseline competence* state rather than a pure rest state.

**R1.3.4 — Cross-validation MP / async on the AP1/p38 module.**
The AP1/p38 module sits in the Naive condition where MP and asynchronous semantics agree on fixed points by construction (no oscillation in the Naive fixed point), so the MP / async question affects this module less than it affects the IFN-I cascade (where the trap-space dynamic could in principle differ). We do not extend the cross-validation to the AP1/p38 module in the present revision but identify it as a useful methodological consolidation for future work (Section 4.10).

**R1.3.5 — Invariants of the IFN-stim trap-space.**
We extract the 1-invariants (50 nodes always active), 0-invariants (277 always inactive) and oscillating coordinates (181 nodes) and report them in `results/phase9/ifn_stim_trap_space_invariants.csv` with the summary `results/phase9/ifn_stim_trap_space_invariants_summary.md`. The skeleton is referenced in Section 3.2 of the manuscript.

**R1.4.x — Vocabulary (trap space vs fixed point, update functions).**
We use "fixed point" throughout to refer to a 0-trap-space (every coordinate is 0 or 1, no `*`); this is consistent with the convention of Paulevé et al. 2020. The text of Section 2.4 already states explicitly that no global update scheduling is imposed under MP semantics. We have refined the wording where needed.

---

## Reviewer 2 — Immuno-rhumatology / SjD clinical

**R2.3.1 — Endpoint for SYK + p38 preclinical evaluation.**
Section 4.4 now specifies a concrete first-line design: a 7-day proliferation / viability assay on TMD8 and OCI-Ly10 (ABC-DLBCL) cells with fostamatinib (or entospletinib) and losmapimod each titrated around their respective IC₅₀ in a checkerboard layout, scoring synergy by Bliss or Loewe metrics.

**R2.3.2 — BAFF/APRIL not covered by the lymphomagenic prediction.**
Section 4.4 is extended with an explicit paragraph stating that the SYK + p38 / PKR prediction addresses one component of the lymphomagenic landscape (BCR-driven AP1/p38 activation) but leaves a second component (paracrine BAFF / APRIL stimulation via TACI / BCMA / BAFF-R / NF-κB) unaddressed by the model. Quartuccio 2014 is cited.

**R2.3.3 — Distinction of the three JAK inhibitors.**
Section 3.7 now distinguishes filgotinib (JAK1-preferential, MOSAIC negative), baricitinib (JAK1/2, observational off-label, mixed) and tofacitinib (pan-JAK, no randomised SjD trial).

**R2.3.4 — Trap-space oscillation: dynamic vs population-level.**
Section 4.2 adds a paragraph distinguishing single-cell real-time oscillation (e.g. STAT1 / SOCS3 dynamics) from population-level variability (snapshot transcriptomic heterogeneity). The MP `*` covers both interpretations without distinguishing them.

**R2.3.5 — Soret 2021 molecular clusters.**
Section 1 (Introduction) and Section 3.3 mention the four-cluster molecular stratification of SjD [Soret2021]; the cohort concordance is interpreted as predominantly informative for the IFN-high and B-cell-inflammatory clusters represented in the blood cohorts.

**R2.3.6 — Tissue boundary (blood vs salivary gland).**
Section 4.7 adds the explicit statement that the model is calibrated on blood-derived transcriptomic signal of SjD and does not, in its current form, predict salivary-gland-specific therapeutic responses.

**R2.4.1 — Anifrolumab: explicit message.**
Section 3.7 closes the anifrolumab simulation with an explicit statement that the model suggests anti-IFNAR alone cannot suffice in multifactorial SjD because parallel BCR / NFkB / MAPK inputs sustain phenotype-level activity.

**R2.4.2 — ESSDAI defined in footnote.**
A footnote at the first mention of clinical efficacy (Bowman 2023, MOSAIC trial in Section 3.7) defines ESSDAI as the EULAR Sjögren's Syndrome Disease Activity Index.

**R2.4.3 — Lymphoma risk in introduction.**
Section 1 (Introduction) now mentions the 15- to 20-fold relative risk of DLBCL and the ≈ 1000-fold relative risk of MALT lymphoma in SjD, citing Solans-Laqué 2011 and Ekström-Smedby 2008.

---

## Reviewer 3 — Transcriptomic bioinformatics

**R3.2.1 — up:down ratio per cohort in Table 2.**
Table 2 now includes the `up:down` ratio column (10.4:1 PRECISESADS, 4.6:1 UKPSSR, 3.9:1 GSE51092, 1.0:1 ASSESS, 13.0:1 GSE23117).

**R3.2.2 — Multi-test correction for the combinatorial screen.**
Section 3.5 reports a concentration-based p-value (analytic 0.037, permutation 0.108) and the Bonferroni threshold for 273 tests. The full analysis is in `results/phase9/combinatorial_multi_test_summary.md`.

**R3.2.3 — n_down column in Table 3.**
Table 3 is rebuilt with `n_up` and `n_down` columns explicit per cohort and includes baseline rows for every cohort (`results/phase9/table3_extended.csv`).

**R3.2.4 — High PPV partially attributable to class imbalance.**
Section 3.3 adds an explicit sentence: "The high PPV figures are partially attributable to the imbalanced class composition of the cohort overlays; balanced accuracy and AUROC, which are insensitive to this imbalance, are therefore the primary metrics of interest."

**R3.2.5 — Bootstrap CI for all five cohorts.**
Table 2 now reports the 95 % bootstrap CI for all five cohorts (no more `[—]`); the values come from `results/phase8/attractor_cohort_distance_v3.csv`, which already included them.

**R3.2.6 — Negative control cohort (non-IFN autoimmune).**
We agree this would be a useful specificity control. We did not run this analysis in the present revision because none of the SjD Map's overlay archive contains an external non-IFN autoimmune cohort, and acquiring and re-mapping a fresh GEO cohort (e.g. GSE100648 RA) is a non-trivial pipeline addition. We identify this as future work in the final paragraph of Section 4.6.

**R3.2.7 — Top-5 enriched pathways per attractor.**
A reformatted SI table at `results/phase9/enrichment_top5_per_attractor.csv` lists the top-5 KEGG / Reactome terms for every attractor; cited in Section 3.3.

**R3.2.8 — coverage_% column in Table 2.**
Table 2 now includes the `coverage %` column (n_pairs / n_total_DEGs per cohort): 12.6 % PRECISESADS, 11.7 % UKPSSR, 8.0 % GSE51092, 2.7 % ASSESS, 3.2 % GSE23117.

**R3.3.x — BH correction on cohort × attractor tests.**
Table 2 now reports `p_BH`. Section 3.3 discusses that the three blood-cohort IFN-stim raw p-values (0.003-0.014) become marginal under BH across the 25 tests (corrected p in 0.08-0.11) and frames the result as collectively meaningful (three independent cohorts converging) rather than independently strong at the FDR 0.05 level.

---

## Reviewer 4 — Pharmacology / drug discovery

**R4.3.1 — Selectivity of clinical SYK inhibitors.**
Section 4.4 now specifies that fostamatinib has moderate kinase selectivity (off-targets on Lyn, FLT3, certain JAK family members) and re-frames the predicted "SYK + p38" axis as a "BCR-pathway kinase + p38" combination. Entospletinib is identified as a more selective SYK option whose selectivity-aware translation is preferable.

**R4.3.2 — PKR as an orphan target requiring de novo development.**
Section 4.4 explicitly states: "The PKR prediction is therefore not a *repositioning* candidate in the strict sense; clinical translation requires *de novo* compound development, and the value of the prediction is to motivate medicinal-chemistry investment in a target whose disease relevance the model now flags."

**R4.3.3 — Untestable combinations (anti-IFN + anti-CD40, anti-BAFF + JAK, anti-IFNAR + p38).**
Section 4.4 includes a paragraph "Combinations the model cannot evaluate" listing these clinically attractive combinations and explaining that they fall outside the dynamic perimeter of the network because they target nodes encoded as inputs.

**R4.3.4 — SI ADMET table for the three predictions.**
We did not produce an ADMET / safety SI table in the present revision (it is more naturally located in a separate translational paper). The clinical-trial history of p38 inhibitors is summarised in Section 4.5 with four references (Damjanov 2018, Hammaker 2010, Watz 2014, Newby 2014).

**R4.3.5 — Preferred preclinical SjD model.**
Section 4.4 now explicitly recommends the IL-14α-transgenic mouse for evaluating the lymphomagenic dimension of the prediction (sialadenitis followed by B-cell lymphoma at older ages); NOD.B10.H2b is mentioned as an alternative for the sialadenitis component alone.

**R4.3.6 — IP / compound supply.**
We did not produce an IP / supply table for the three predictions, considering this beyond the scope of an attractor-analysis manuscript. This information is best assembled at the time of preclinical programme commitment.

---

## Editor

The seven convergent points (C1-C7 in the editorial synthesis) are all addressed by this revision. No new pipeline execution was required; all corrections are tabular additions, prose precisions and three small SI scripts (`build_table2_enriched.py`, `build_table3_enriched.py`, `combinatorial_multi_test.py`, `naive_fp1_origin.py`, `ifn_stim_invariants.py`, `enrichment_top5_per_attractor.py`). The pipeline `make all` continues to reproduce the analyses end-to-end from the raw SBML.
