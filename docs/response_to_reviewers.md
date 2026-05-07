# Response to Reviewers — Manuscript v2

**Title (revised):** *Boolean Attractor Analysis of the Sjögren's Disease Map Identifies AP1/p38 MAPK as a Candidate Convergent Control Module Under IFN Stimulation*

**Authors:** Foulquier
**Date:** 2026-05-07

---

We thank the four reviewers for their thorough and constructive critiques. This response letter addresses each recommendation R1.1–R4.8 individually, with pointers to the new manuscript (v2), the new analysis scripts, the new result tables and the supporting documents under `docs/reviewing/` and `results/phase7/`. A summary of major changes:

- **Model v2** (`models/sbmlqual/v2/sjd_map_v2.bnet`, tag `model-v2.0`): HDAC3 = 1, KPNB1 = 1 to unblock the IFN cascade (addresses C1 / R2.1).
- **HGNC-aware DEG mapping** (`data/processed/hgnc_to_bnet.csv`): replaces substring matching, distinguishes protein vs mRNA (R3.2, R3.5).
- **10 000-permutation null model** for Hamming distance, with empirical p-values (R3.1).
- **Sensitivity / specificity / AUROC** decomposition per attractor × cohort (R3.3).
- **KEGG / Reactome over-representation** (R3.7).
- **Topological audit of the AP1/p38 module** (R1.7).
- **Targeted combinatorial perturbation screen** including the JAK + p38 pair specifically demanded by R2.3 / R4.1.
- **Threshold sensitivity** of the disease-attractor definition (R4.5).
- **Re-cast clinical concordance** as 3 modellable / 9 not modellable (R4.7, R4.4).
- **Re-cadrage GSE23117** as insufficiently powered (R3.6).
- **Tempered title** ("candidate convergent control module under IFN stimulation" replaces "central control module") (R2.7).
- **Tempered abstract** without "8/10 concordance" claim (R4.7).

---

## Reviewer 1 — Modélisation booléenne

### R1.1 — Stable motifs / minimum intervention sets

**Reviewer:** "An analysis of stable motifs / MIS would substantively support the AP1/p38 hit beyond a perturbation screen."

**Response.** We agree and attempted the analysis. `pystablemotifs.format.import_primes` (BNetToPrime backend) does not terminate within practical time budgets on either v1 or v2 (502+ rules, > 180 s; documented in `results/phase7/stable_motifs_status.md`). We pursued instead a *targeted combinatorial perturbation screen* of 91 drug-target pairs (Section 3.5 of v2, `results/phase7/combinatorial_perturbations.csv`) and a *threshold-sensitivity analysis* (Section 2.10, `results/phase7/threshold_sensitivity.csv`). The combinatorial screen gives an *upper bound* on minimum intervention sets — every element of a true MIS must appear as a hit in a screen of sufficient depth — but does not certify that no asynchronous trajectory bypasses the perturbation. We document this gap explicitly in Section 4.7 of v2 and as a future-work item.

### R1.2 — Conditions inputs biologiquement plausibles

**Reviewer:** "The naive condition fixes all 104 inputs to 0, which is biologically implausible (HDAC3, KPNB1, complement components, etc.)."

**Response.** Addressed via model v2: HDAC3 and KPNB1 are now constants = 1 by construction (Section 2.3 of v2). We have not redefined input defaults beyond these two cases because (a) the rest of the input nodes have a wider range of biologically defensible defaults (e.g. each cytokine receptor in absence of its ligand) and (b) we wanted to keep the v2 changes auditable line-by-line (see `models/sbmlqual/v2/changes.csv`). The two changes are sufficient to unblock the IFN cascade, which was the central biological deficiency of v1.

### R1.3 — Crible combinatoire

**Reviewer:** "The mono-node screen cannot test the synergy claims; pair-wise screens are needed."

**Response.** Done. Section 3.5 of v2 reports a pair screen of 91 drug-target pairs over three signalling conditions (273 pair-condition runs). Three synergistic pairs are identified in the BCR-stim condition (SYK + EIF2AK2, SYK + MAP2K6, SYK + MAPK11-14). The JAK + p38 pair specifically requested by R2.3 was tested and is *not* synergistic — see R2.3 below.

### R1.4 — Comparaison des sémantiques (MP vs asynchrone)

**Reviewer:** "MP semantics over-approximates reachability — comparison with asynchronous semantics would strengthen the attractor catalogue."

**Response.** Acknowledged as a future-work item. We did not run BoolNet (R) on v2 within the revision window. The v2 attractors include one cyclic trap space (IFN-stim, Section 3.2), so MP is not used here as a fixed-point-only solver. We document this gap in Section 4.7 of v2.

### R1.5 — Audit déduplication sanitisation

**Reviewer:** "How many rules are dropped by deduplication in `sanitize_bnet.py`?"

**Response.** Done. The sanitiser was modified to emit `data/processed/sanitize_collisions.csv` reporting every collision. The audit shows **0 sanitized targets received more than one raw rule** and **0 raw rules were discarded by deduplication** (confirmed at runtime). The deduplication step is therefore biologically benign.

### R1.6 — Tests de non-régression

**Reviewer:** "There should be a non-regression test suite."

**Response.** Three non-regression tests are added in `tests/` (Phase 7.5.1):
- `test_attractor_counts.py`: v2 produces 2 / 1 / 2 attractors for Naive / IFN / BCR.
- `test_isg_activability.py`: ≥ 3 canonical ISGs are activable (= 1 or *) under IFN-stim.
- `test_null_model_significance.py`: PRECISESADS / UKPSSR / GSE51092 p-values are all < 0.05 for the IFN-stim attractor.

### R1.7 — Audit topologique AP1/p38

**Reviewer:** "Centrality, in-degree, out-degree of the AP1/p38 module should be reported and compared to a control set."

**Response.** Done. Section 3.4 of v2 and `docs/audit_ap1_p38.md` report betweenness, in/out-degree, ancestor and descendant counts for the six AP1/p38 nodes versus 11 control nodes (JAK-STAT, BCR, NFkB, other MAPKs, output phenotypes). Mean betweenness 0.006 (module) versus 0.017 (control), 3× lower; in/out-degree also 2.5–3× lower. The module is a *terminal relay* convergent for several upstream ligands (1–2 node-disjoint paths from each input), not a high-betweenness hub. We re-frame the v2 manuscript accordingly: "candidate convergent control module" replaces "central control module" (R2.7).

---

## Reviewer 2 — Immuno-rhumatologue / SjD

### R2.1 — Correction HDAC3 / IFN-I (CRITIQUE)

**Reviewer:** "The model cannot reproduce the IFN-high signature because of `STAT1 = HDAC3` and `... AND KPNB1` rules."

**Response.** This is the central correction of v2. Both rules now resolve to `STAT1 = ... AND HDAC3` and `... AND KPNB1` with HDAC3 = 1 and KPNB1 = 1 by construction in `sjd_map_v2.bnet`. Under v2 IFN-stim, 17 canonical ISGs are activable (state ∈ {1, *}): MX1, MX2, OAS1-3, ISG15, IRF7, IFIT1, IFIT3, STAT1, STAT2-P, ISGF3 nuclear (Section 3.2 of v2, `results/phase7/attractor_v2_isgs.csv`). The KEGG/Reactome over-representation on the IFN-stim active-node set returns *Interferon Signaling*, *JAK-STAT signaling*, *IFN α/β*, *IFN γ* with adj-p < 10⁻²⁶ (Section 3.3, `results/phase7/enrichment_attractors.csv`).

### R2.2 — Reformulation abstract

**Reviewer:** "The abstract over-claims; remove the '8/10 concordance' figure."

**Response.** Done. The v2 abstract no longer mentions concordance as a percentage. It states the more honest accounting: 3 modellable / 9 not modellable drugs, all three modellable drugs predicted insufficient as monotherapy (concordant with reported failure), and the JAK + p38 synergy claim is retracted.

### R2.3 — Simulation JAK + p38 effective

**Reviewer:** "The combination is claimed but never simulated."

**Response.** Done. Section 3.5 of v2 explicitly tests the pair JAK1 + MAPK11-14 (and JAK1 + AP1, BTK + MAPK11-14, BTK + AP1, SYK + MAPK11-14, TYK2 + MAPK11-14, STAT2 + AP1). The result is **negative**: in the Naive condition, p38 inhibition alone already eliminates the disease attractor, so adding JAK does not change the outcome. We explicitly *retract* the synergy claim. This is a falsification of one specific prediction by direct simulation, which we believe is more useful than retaining an unsupported claim. The combinatorial screen does identify three synergistic pairs in the BCR condition (SYK + EIF2AK2, SYK + MAP2K6, SYK + MAPK11-14), reframing the synergy hypothesis around BCR-driven contexts (DLBCL).

### R2.4 — Échecs historiques p38

**Reviewer:** "p38 inhibitor history is unfavourable; this should be discussed."

**Response.** Done. Section 4.3 of v2 ("The historical record of p38 inhibitors") cites four references: Damjanov et al. 2018 (RA, hepatotoxicity), Hammaker & Firestein 2010 ("Go upstream, young man"), Watz et al. 2014 (COPD failure), Newby et al. 2014 (post-MI, losmapimod failure). The discussion explicitly states that *monotherapy* p38 inhibition has a poor track record, and that any clinical translation of our prediction must be evaluated as a *combination* with anti-IFN or anti-CD40 backbones.

### R2.5 — Discussion non-modélisabilité BAFF/CD40

**Reviewer:** "Belimumab, anti-CD40, ianalumab — all non-modellable in the current encoding. Discuss."

**Response.** Section 4.4 of v2 ("Limitations of the SjD Map for SjD drug repurposing") quantifies this: 25 of 39 OpenTargets clinical-trial targets are not present in the BNET or are present only as input nodes. The full list (BAFF/APRIL pathway, CD40-CD40L, IFNAR receptors, TLR antagonists) is named. We make explicit that drug-repurposing inferences from this Boolean dynamics are conditioned on the small subset of targets the SjD Map encodes dynamically.

### R2.6 — Limitation cell-type agnostique

**Reviewer:** "The model is cell-type agnostic; the salivary tissue mismatch was acknowledged but should be discussed structurally."

**Response.** Section 4.5 of v2 discusses this at length, citing the GSE23117 (salivary gland) and ASSESS (DLBCL) under-performance as direct evidence of the limitation. We point to single-cell extensions of comparable inflammation atlases (e.g., AIR) as a possible path forward.

### R2.7 — Tempérer le titre

**Reviewer:** "'Central control module' over-claims."

**Response.** New title: "*… Identifies AP1/p38 MAPK as a Candidate Convergent Control Module Under IFN Stimulation*". The v2 abstract and discussion use the same wording.

---

## Reviewer 3 — Bioinformatique transcriptomique

### R3.1 — Null model Hamming (CRITIQUE)

**Reviewer:** "Hamming distances are reported without a null distribution; permutation test required."

**Response.** Done. Section 2.6, Section 3.3 of v2; `src/validation/null_model_hamming.py`; `results/phase7/attractor_cohort_distance_v2.csv`; `figures/phase7/null_model_distribution.png`. Each (cohort, attractor) pair receives an empirical p-value over 10 000 permutations of DEG directions (the same mapped pairs are used; only the +1/-1 sign is shuffled). The IFN-stim A1 attractor is significant on the three blood cohorts (p ≤ 0.014) and *not* significant on ASSESS (p = 0.62) and GSE23117 (p = 0.65).

### R3.2 — Mapping HGNC officiel

**Reviewer:** "Substring matching is too imprecise; use a proper HGNC mapping."

**Response.** Done. `src/validation/build_hgnc_mapping.py`, `data/processed/hgnc_to_bnet.csv`. The procedure decomposes node names by suffix stripping, complex decomposition, family expansion (`MAPK11_12_13_14` → MAPK11, 12, 13, 14) and alias map. It distinguishes protein, mRNA, complex_member, secreted, phosphorylated forms (R3.5). 97.8 % of non-phenotype nodes are mapped to ≥ 1 HGNC. The cohort coverage (12.6 % blood, 3.3 % salivary) is unchanged in absolute terms because most unmapped DEGs are *not present in the SjD Map at all* — a structural property of the source map, not a defect of the matching procedure.

### R3.3 — Sensibilité / spécificité / AUROC

**Reviewer:** "Hamming alone hides asymmetries; report sensitivity, specificity, AUROC."

**Response.** Done. Section 3.3 of v2; `src/validation/sensitivity_specificity.py`; `results/phase7/sensitivity_specificity_auroc.csv`. The IFN-stim A1 attractor reaches sensitivity 0.65–0.72, specificity 0.74–1.00, balanced accuracy 0.69–0.85 on the three blood cohorts; AUROC 0.72 (PRECISESADS) and 0.85 (UKPSSR). R3.3's threshold AUROC > 0.6 for at least one cohort is exceeded on two cohorts.

### R3.4 — Sensibilité aux seuils DEG

**Reviewer:** "DEG threshold sensitivity?"

**Response.** The DEG lists are taken directly from the published Cytoscape overlays of the SjD Map (categorical, no continuous threshold). Sensitivity to the *attractor-side* threshold (≥ 5/6/7 disease phenotypes) is reported in Section 2.10 / 3.4 / `results/phase7/threshold_sensitivity.csv`: the AP1/p38 hits are stable across all three thresholds.

### R3.5 — Distinction protéine / ARNm

**Reviewer:** "DEG signal is mRNA — should map to *_rna nodes preferentially."

**Response.** Done. The HGNC mapping records a `kind` per (gene, node) pair. For Hamming computation in v2, each DEG resolves to a single node by preferring `_rna` first (transcriptomic measurement), then the protein/complex form, and finally phosphorylated/nuclear forms only as a last resort (`null_model_hamming.py:RNA_PREF_ORDER`). This correction reduces several v1 mismatches where a mRNA up-regulation was incorrectly compared against a phosphoprotein state.

### R3.6 — Re-cadrage GSE23117

**Reviewer:** "GSE23117 is salivary tissue; report it as cross-tissue, not as positive validation."

**Response.** Done (`results/phase7/gse23117_recadrage.md`, Section 3.8 of v2). Coverage is 3.3 % (28 mapped genes), null-model p = 0.65, AUROC = 0.43 (sub-random). We label the analysis as *insufficiently powered* and retract the implicit positive interpretation of v1.

### R3.7 — Enrichissement KEGG/Reactome

**Reviewer:** "Hypergeometric enrichment of attractor active nodes versus pathway databases would be more biologically interpretable than Hamming alone."

**Response.** Done. Section 2.8, Section 3.3 of v2; `src/validation/enrichment_kegg_reactome.py`; `results/phase7/enrichment_attractors.csv`. IFN-stim A1 returns four canonical IFN pathways (Interferon Signaling, JAK-STAT, IFN α/β, IFN γ) with adj-p < 10⁻²⁶ — concordance criterion 7.2.4 (≥ 3 canonical SjD pathways) is met (4 ≥ 3).

### R3.8 — Discussion asymétrie up/down

**Reviewer:** "Up-DEGs are over-represented in mappings; symmetry should be discussed."

**Response.** Discussed in Section 4.6 of v2. The SjD Map curates activating cascades preferentially; downstream feedback inhibition and cell-cycle suppression (which drives many of the down-regulated DEGs in PRECISESADS) are sparsely encoded. This is named as a structural curatorial limitation, not as a methodological choice we make.

---

## Reviewer 4 — Pharmacologie / drug discovery

### R4.1 — Simulation combinaisons

**Reviewer:** "Test the combinations explicitly."

**Response.** Done — see R2.3 above. Section 3.5 of v2 reports 91 drug-target pairs across 3 conditions; 3 synergistic pairs identified (SYK + EIF2AK2 / MAP2K6 / MAPK11-14 in BCR-stim).

### R4.2 — Sélectivité JAK inhibiteurs

**Reviewer:** "JAK1 ≠ JAK1/2 ≠ pan-JAK; discuss selectivity."

**Response.** The v2 drug-simulation table (Table 5) distinguishes filgotinib (JAK1), baricitinib (JAK1/2), tofacitinib (pan-JAK). All three reduce phenotype counts under IFN-stim partially but do not collapse the trap-space attractor — the model does not currently capture sufficient JAK isoform-specific differential to predict differential efficacy. We acknowledge this as a granularity limit in Section 4.4.

### R4.3 — Reformulation prédictions p38/AP1/PKR

**Reviewer:** "Predictions should be qualified by the historical record."

**Response.** Done. Section 4.3 of v2 ("The historical record of p38 inhibitors") cites three independent failure programmes (RA, COPD, post-MI). The conclusion is qualified accordingly: *preclinical* evaluation is warranted, but as a *combination* therapy and not as monotherapy.

### R4.4 — Section cibles non modélisables

**Reviewer:** "Make explicit how many of the OpenTargets SjD targets are not modellable."

**Response.** Done. Section 4.4 of v2 quantifies: 25 / 39 (64 %) of OpenTargets clinical-trial drug targets are not present in the BNET or are present only as input nodes. The list is named (BAFF / APRIL pathway, CD40-CD40L, IFNAR, TLR antagonists). This is now an explicit limitation of the SjD-Map-based framework, not a hidden one.

### R4.5 — Sensibilité au seuil disease attractor

**Reviewer:** "What if the disease-attractor threshold were 5 or 7 instead of 6?"

**Response.** Done. Section 2.10 / 3.4 / `results/phase7/threshold_sensitivity.csv`: at θ ∈ {5, 6, 7}, the six AP1/p38 nodes are robust hits. At θ = 7 the broader hit set expands from 7 to 19 (more nodes can prevent the strict 7-phenotype state) but the AP1/p38 module remains in the hit set at every threshold.

### R4.6 — Échecs historiques p38 (3+ refs)

**Reviewer:** "Cite at least three references for p38 inhibitor failures, not just Damjanov."

**Response.** Done — Damjanov 2018 (RA), Watz 2014 (COPD), Newby 2014 (post-MI). Hammaker & Firestein 2010 added as a methodological context citation.

### R4.7 — Retirer "8/10 concordance"

**Reviewer:** "Remove the misleading concordance metric."

**Response.** Done in the v2 abstract, conclusions, and Table 5 (re-cast as 3 modellable / 9 not modellable). The metric was driven by the model predicting failure for drugs that did fail clinically — a tautology, as the reviewer correctly noted.

### R4.8 — Section 25/39 cibles absentes

**Reviewer:** "Document the OpenTargets coverage gap explicitly."

**Response.** Done — see R4.4. Section 4.4 of v2 names this as a structural limitation of the SjD Map, not of the Boolean framework, and qualifies any drug-repurposing inference accordingly.

---

## Cross-cutting — additional changes

- **Tag `model-v2.0`** on `models/sbmlqual/v2/sjd_map_v2.bnet` (R1.4 versioning ask).
- **`changes.csv`** logs the two HDAC3 / KPNB1 rule edits per the responsible-correction policy adopted (R2.1).
- **`hgnc_to_bnet.csv`** is now the single source of truth for gene–node mapping (R3.2 / R3.5).
- **CITATION.cff** updated to version 2.0; abstract revised.
- **Snakemake** workflow extended with the Phase 7 rules; `make all` runs everything from raw SBML to v2 figures and tables.

We hope these revisions adequately address the four reviewer reports. We are particularly grateful for the rigour of R3 on the statistical pipeline (null model, AUROC, mapping) and for the directness of R2 and R4 on the over-claims of v1, which led to a cleaner and more honest accounting of what the model can and cannot predict.

— The author
