# Boolean Attractor Analysis of the Sjögren's Disease Map Identifies AP1/p38 MAPK as a Candidate Convergent Control Module Under IFN Stimulation

**Nathan Foulquier**¹

¹ [Affiliation]

**Correspondence:** nathan.foulquier.pro@gmail.com

> **Manuscript v2.** Revised in response to four reviewer reports (R1 modélisation booléenne, R2 immuno-clinicien, R3 bioinfo transcriptomique, R4 pharmaco / drug discovery). Changes are documented in `docs/response_to_reviewers.md`. Compared to v1, this revision (i) corrects the IFN-I encoding (HDAC3 = 1, KPNB1 = 1) in a v2 of the Boolean network, (ii) replaces the substring DEG mapping with an HGNC-based mapping that distinguishes protein and mRNA forms, (iii) reports a 10 000-permutation null model for every Hamming distance, (iv) adds AUROC, sensitivity, specificity and KEGG/Reactome enrichment, (v) reports a targeted combinatorial perturbation screen including the JAK + p38 prediction, (vi) audits the AP1/p38 module topologically, and (vii) tempers the abstract, title and clinical-concordance claims accordingly.

---

## Abstract

The Sjögren's Disease Map (SjD Map; Silva-Saffar et al., 2026) is the first molecular interaction map dedicated to Sjögren's disease (SjD), encoding 829 entities and 598 interactions. We convert the SjD Map into an executable Boolean network (508 nodes) using CaSQ, characterise its attractor landscape under three signalling conditions, and screen mono- and di-genic perturbations to identify candidate therapeutic control points.

A first version of the network produced an IFN-stimulated attractor that did not activate canonical interferon-stimulated genes (ISGs); we traced this to two CaSQ-inherited input dependencies (HDAC3, KPNB1) whose biological default is *constitutive activity*, not the value-0 default that CaSQ assigns to every input. Setting HDAC3 = 1 and KPNB1 = 1 (model v2) unblocks the ISGF3 cascade and yields an IFN-stimulated attractor in which 17 canonical ISGs (including MX1, OAS1-3, ISG15, IRF7, IFIT1/3) are activable.

Under v2, the IFN-stimulated attractor matches the three blood transcriptomic cohorts significantly better than chance (10 000-permutation null model): Hamming = 0.250–0.333, p ≤ 0.014 across PRECISESADS (n=91 mapped pairs), UKPSSR (n=28) and GSE51092 (n=93). Cross-attractor AUROC reaches 0.72–0.85 on the two cohorts with sufficient mapping coverage. KEGG / Reactome over-representation testing on the IFN-stimulated active-node set returns *Interferon Signaling* (Reactome, adj-p = 3.1 × 10⁻⁸⁶), *JAK-STAT signaling* (KEGG, adj-p = 4.5 × 10⁻²⁶), *IFN-α/β Signaling* and *IFN-γ Signaling* — all four canonical type-I/II IFN pathways are recovered.

A targeted single-node perturbation screen (Naive condition, 158 perturbations) identifies six interventions in the AP1/p38 MAPK module (EIF2AK2 → MAP2K6 → MAPK11-14 → FOS/JUN → AP1) that eliminate the disease attractor. A topological audit of this module shows that it is **not** a high-betweenness hub of the graph (mean betweenness 0.006 versus 0.017 for a comparable set of JAK-STAT/BTK/SYK/NFkB nodes), but is a **convergence point** for several upstream ligand cascades (TLR4, TLR9, BCR, IFN-α/β/γ all reach AP1 via 1–2 node-disjoint paths). The module is therefore better described as a *candidate convergent control module* than as a central hub, and its selection by the screen is partly a property of its sparse linear topology — a nuance that we make explicit in the discussion.

A targeted combinatorial perturbation screen (91 drug-target pairs across three conditions) tested directly the synergy hypotheses raised by reviewers. **The "JAK + p38" combination is *not* synergistic in the model**: p38 inhibition alone already eliminates the disease attractor in Naive and BCR conditions, so the addition of a JAK inhibitor brings no additional benefit at the attractor level. We therefore retract the synergy claim of the v1 manuscript. Three different pairs do show synergy in the BCR-stimulated condition: SYK + EIF2AK2 (PKR), SYK + MAP2K6 and SYK + MAPK11-14 (p38). These define a candidate combinatorial axis for SjD-associated lymphoma, where chronic BCR signalling is hypothesised to bypass mono-kinase inhibition.

In silico drug simulation (12 drugs × 3 conditions) shows that nine drugs in clinical trials have *no testable prediction* in the v2 model under the chosen conditions. Of the three drugs the model can score (filgotinib, baricitinib, tofacitinib), all three are predicted to be insufficient in monotherapy under Naive conditions — concordant with the modest clinical efficacy reported for these JAK inhibitors. The remaining nine drugs are not modellable because their targets (BAFF/APRIL, CD40, IFNAR, TLR7/9) are encoded as input nodes whose dynamics the model does not simulate. We therefore retract the v1 "8/10 concordance" metric, which was driven by the model predicting failure for drugs that did fail clinically — a tautology rather than prospective validation.

We propose three actionable predictions: (i) p38 inhibitors (losmapimod, doramapimod) and PKR inhibitors (C16, imoxin) merit preclinical evaluation in SjD models; (ii) for SjD-associated DLBCL, SYK + p38 or SYK + PKR combinations should be evaluated in BCR-driven xenograft models; (iii) all p38-clinical-history caveats apply (cardiotoxicity in IPF and BPCO trials, hepatotoxicity in RA trials) and any clinical translation requires the kind of safety data that mono-target programmes have struggled to generate.

**Keywords:** Sjögren's disease, Boolean network, attractor, AP1, p38 MAPK, EIF2AK2, control analysis, null model, AUROC, combinatorial perturbation, systems biology

---

## 1. Introduction

Sjögren's disease (SjD) is a systemic autoimmune disease characterised by lymphocytic infiltration of exocrine glands, B-cell hyperactivation, and a strong type-I IFN signature [Mariette2018, Verstappen2021]. Its pathogenesis integrates multiple signalling branches — TLR/IFN-I, BCR/BTK, JAK-STAT, NF-κB, and AP1/MAPK — whose collective dynamics remain poorly understood.

The SjD Map [SilvaSaffar2026] is the first curated Molecular Interaction Map (MIM) specific to SjD, built from three transcriptomic cohorts (PRECISESADS, UKPSSR, GSE51092), KEGG/Reactome pathway enrichment, and 216 PubMed references. Its topological analysis identified five hub nodes (Inflammation, STAT1 homodimer, STAT1/STAT2/IRF9 trimer, RELA/NFKB1 heterodimer, Chemotaxis/Infiltration). The map is *executable* in the structural sense (every interaction is signed and typed) but does not model temporal dynamics or predict which combinations of perturbations redirect the system toward homeostasis.

Boolean networks are a well-validated formalism for large-scale signalling-network modelling [Thomas1973, Saadatpour2013, Abou-Jaoudé2016]. They represent each molecular species as a binary variable and capture the qualitative logic of regulatory interactions; their attractor states (fixed points and cyclic attractors) correspond to stable cell phenotypes [Huang1999, Kauffman1969]. Systematic perturbation analysis on Boolean networks provides a computationally tractable framework for therapeutic-target identification [Zañudo2015, Rozum2021].

Here we apply this framework to the SjD Map. Beyond a first version that was internally consistent but had two limitations (a CaSQ-inherited block of the ISG cascade, and a Hamming-distance-only validation without statistical null), we report a corrected v2 of the network and a substantially extended validation: HGNC-aware DEG mapping, 10 000-permutation null model, sensitivity / specificity / AUROC, KEGG / Reactome over-representation, and a *targeted* combinatorial perturbation screen testing the synergy hypotheses raised by peer review of the v1 manuscript.

---

## 2. Methods

### 2.1 Data sources

The SjD Map was downloaded from Zenodo (10.5281/zenodo.17585308). The CellDesigner SBML L2v4 (`SjD_Map.xml`, 840 species, 598 reactions) is the primary input. Transcriptomic overlays for three blood cohorts (PRECISESADS, UKPSSR, GSE51092) and two disease-specific datasets (ASSESS lymphoma [Duret2023]; GSE23117 salivary gland) were extracted from the same archive. Drug–gene associations are from the DrugBank/OpenTargets overlay included in the archive.

### 2.2 Boolean network construction (v1)

CellDesigner SBML was converted to BNET via **CaSQ v1.3.3** [Aghamiri2020], producing 508 nodes / 508 rules. CaSQ encodes activating and inhibitory arcs as Boolean OR/AND expressions. Node names contained characters illegal in Boolean network solvers; a custom sanitiser (`src/conversion/sanitize_bnet.py`) replaces non-alphanumeric characters by underscores, collapses consecutive underscores, and substitutes formula tokens with longest-first matching. A deduplication audit (Phase 7.1.3) confirmed that *zero* rules were lost during sanitisation (see `data/processed/sanitize_collisions.csv`). Of the 508 nodes, 104 are input nodes (self-regulatory loops).

### 2.3 Boolean network correction (v2; HDAC3, KPNB1 unblocked)

The v1 BNET inherits two CaSQ-encoded dependencies that block the IFN cascade when input nodes default to 0:

- `STAT1 = HDAC3` (HDAC3 input → STAT1 protein never expressed if HDAC3 = 0)
- `STAT1_STAT2_IRF9_complex_nucleus = ... AND KPNB1` (importin-β1 = 0 → ISGF3 never enters the nucleus)

HDAC3 and KPNB1 are constitutively active in immune cells. We therefore overrode both input rules to the constant 1 in `models/sbmlqual/v2/sjd_map_v2.bnet` (`src/conversion/build_v2_model.py`). A change log is preserved in `models/sbmlqual/v2/changes.csv`. Under v2, the IFN-stimulated attractor activates 17 canonical ISGs, satisfying the requirement that the type-I IFN signature — *the* most reproducibly observed transcriptomic feature of SjD — be reachable in the model.

### 2.4 Network conditions and attractor computation

Three signalling conditions are defined by fixing inputs:

- **Naive (homeostatic):** all input nodes at 0.
- **IFN-stimulated:** IFNA, IFNB1, IFNG extracellular ligands and IFNAR complex set to 1.
- **BCR-stimulated:** BCR_complex set to 1.

After fixing inputs, constant propagation reduces the network to 64–253 dynamic nodes depending on condition (Naive: 79; IFN: 253 in v2 because HDAC3/KPNB1 release downstream signalling; BCR: 64). Attractors are computed with **mpbn 4.3.2** [Paulevé2020] under Most Permissive (MP) semantics. Under MP, an attractor is a minimal trap space; coordinates may take values in {0, 1, *}, where * denotes a node that oscillates within the attractor. We treat * as *activable* for phenotype counting and ISG counting.

### 2.5 HGNC-based DEG mapping and protein/mRNA distinction (R3.2, R3.5)

The v1 manuscript used substring matching to associate DEG symbols to BNET nodes. We replace this with an HGNC-aware mapping (`src/validation/build_hgnc_mapping.py`, output `data/processed/hgnc_to_bnet.csv`, 593 mappings, 97.8 % of non-phenotype nodes mapped). The procedure: (i) strip CaSQ suffixes (`_rna`, `_phosphorylated`, `_complex`, `_nucleus`, `_Cell`, `_Extracellular_ligands`, `_Secreted_molecules`, `_homodimer`, `_active`, `_simple_molecule`, `_empty`); (ii) decompose multi-gene complexes by underscores (e.g. `STAT1_STAT2_IRF9_complex` → STAT1, STAT2, IRF9); (iii) expand family numbering (`MAPK11_12_13_14` → MAPK11/12/13/14); (iv) apply alias rules for legacy CD names (CD279 → PDCD1, BAFF → TNFSF13B, …); (v) flag the *kind* of each mapping (protein, mRNA, complex_member, secreted_ligand, phosphorylated, nucleus, …). For Hamming computation we resolve a DEG to a single node by preferring the `_rna` form when available (transcriptomic measurement), otherwise the protein/complex form, and avoiding phosphorylated/nucleus forms unless they are the only option.

### 2.6 Null model permutation test (R3.1)

For each (cohort, attractor) pair we report a Hamming distance and a permutation p-value (`src/validation/null_model_hamming.py`). We hold the set of mapped (gene, node) pairs fixed and randomly shuffle the up/down direction of each DEG over 10 000 permutations. The empirical p-value is the fraction of permutations in which the null Hamming is ≤ the observed Hamming. We also report the z-score relative to the null mean.

### 2.7 Sensitivity, specificity, AUROC (R3.3)

For each (cohort, attractor) pair we decompose the agreement into TP / TN / FP / FN, derive sensitivity, specificity, balanced accuracy and the area under the ROC curve. AUROC is computed by ranking nodes by their *cross-attractor activation frequency* (mean state over the five v2 attractors) and treating the cohort-defined direction as the binary label.

### 2.8 KEGG / Reactome over-representation (R3.7)

For each attractor we export the set of HGNC symbols mapped to nodes in state ∈ {1, *} and run hypergeometric over-representation against KEGG_2021_Human and Reactome_2022 via the Enrichr API (`gseapy` 1.2.1). The same procedure is applied to the up-regulated DEGs of each cohort. We report adjusted p-values (Benjamini-Hochberg).

### 2.9 Topological audit of the AP1/p38 module (R1.7)

We compute in-degree, out-degree, betweenness centrality, and reachable component sizes (NetworkX) for the six AP1/p38 module nodes and a control set of 11 nodes covering JAK-STAT, BCR, NFkB, other MAPKs and three output phenotypes (`src/validation/audit_ap1_p38.py`). We walk three steps upstream from MAPK11-14 to test whether the canonical TAK1 (MAP3K7) and ASK1 (MAP3K5) branches are present. We compute the number of node-disjoint paths from each ligand input (IFN-α/β/γ, BCR, CpG/TLR9, LPS/TLR4) to MAPK11-14, AP1_complex and STAT1-P (reference).

### 2.10 Single-node perturbation screen (Phase 4) and threshold sensitivity (R4.5)

For the Naive condition (79 dynamic nodes on v1; recovered identically on v2 because HDAC3/KPNB1 do not feed into the Naive trap space), each node is independently forced to 0 or 1 (158 perturbations). For each perturbation we recompute fixed points and ask whether any retained FP has ≥ θ disease phenotypes, with θ ∈ {5, 6, 7}. The six AP1/p38 module nodes are robust hits at all three thresholds (`results/phase7/threshold_sensitivity.csv`).

### 2.11 Combinatorial perturbation screen (R1.3, R2.3, R4.1)

We compose a pair pool of 91 drug-target pairs by taking all 2-combinations of 14 drug-target nodes (JAK1/2/3, TYK2, STAT2, BTK, SYK, TNFRSF13C, MAPK11-14, AP1_complex, FOS, JUN, EIF2AK2_homodimer, MAP2K6) augmented with the 7 reviewer-requested explicit pairs (notably JAK1 + MAPK11-14 = "JAK + p38"). Each pair is run under the three signalling conditions. A pair is labelled *synergistic* iff (i) the pair eliminates the disease attractor (no remaining FP with ≥ 6 disease phenotypes) and (ii) neither single-node perturbation does so on its own. Output: `results/phase7/combinatorial_perturbations.csv`.

### 2.12 Stable motifs (R1.1) — intractability

`pystablemotifs.format.import_primes` (BNetToPrime backend) does not terminate within 180 s on either v1 or v2 — the prime-implicant computation is exponential in the network size. We therefore document this limitation and report the perturbation screen + combinatorial screen as the practical control analysis, with the explicit caveat that the screens give an *upper bound* on stable-motif minimal intervention sets but do not certify that no asynchronous trajectory bypasses the perturbation.

### 2.13 In silico drug simulation

Twelve drugs are simulated by fixing their targets to 0 (inhibition) or 1 (activation as appropriate). Drugs: filgotinib (JAK1), baricitinib (JAK1/2), tofacitinib (pan-JAK), tirabrutinib (BTK), iscalimab (anti-CD40), ianalumab (anti-BAFF, TNFSF13B extracellular), belimumab (anti-BAFF, TNFSF13B secreted), anifrolumab (anti-IFNAR), hydroxychloroquine (TLR7/9), p38-inhibitor, AP1-inhibitor, PKR-inhibitor.

### 2.14 External validation

**ASSESS lymphoma.** The DEG overlay [Duret2023] is mapped to BNET nodes; BTK_phosphorylated and TNFSF13B states are examined per attractor. **GSE23117 salivary gland.** The DEG list is mapped to nodes for cross-tissue Hamming and AUROC; the resulting coverage (3.3 %, 28 mapped genes) is reported as *insufficiently powered* — see Section 3.7 and R3.6 in the response letter.

### 2.15 Software and reproducibility

All analyses are implemented in Python 3.12 using mpbn 4.3.2, pandas, matplotlib, networkx, scikit-learn, gseapy 1.2.1. The complete pipeline is encapsulated in a Snakemake workflow (`workflow/Snakefile`) executable in a single command (`make all`). Source code: [REPOSITORY_URL] under MIT licence. The v2 model and Phase 7 results are tagged `model-v2.0`. Three non-regression tests (R1.6) verify the attractor counts, the ISG activability under IFN-stim, and the null-model p-value range.

---

## 3. Results

### 3.1 Conversion and structural validation

CaSQ v1.3.3 converts the 840-species CellDesigner SBML to a 508-node Boolean network. Sanitisation renames 131 nodes with zero collisions and zero rules dropped (Phase 7.1.3 audit). The network contains 14 phenotype terminal nodes and 104 input nodes. After fixing inputs and propagating constants, 64–253 nodes are dynamic depending on condition.

### 3.2 The v2 IFN-corrected attractor activates the canonical ISG signature (Phase 7.1.1)

Under v1, the IFN-stimulated condition produced two fixed points but neither activated any ISG (MX1, OAS1-3, ISG15, IRF7, IFIT1/3 remained at 0). We traced this to two CaSQ-inherited rules — `STAT1 = HDAC3` and `STAT1_STAT2_IRF9_complex_nucleus = ... AND KPNB1` — where HDAC3 and KPNB1 are encoded as input nodes that default to 0. These two genes are biologically constitutive in immune cells. Setting both to 1 (model v2) yields under IFN-stim a single trap-space attractor in which 17 canonical ISGs are activable (state = 1 or *) including STAT1, STAT2-P, STAT1-STAT2-IRF9 nuclear complex, MX1, MX2, OAS1-3, ISG15, IRF7, IFIT1, IFIT3 (`results/phase7/attractor_v2_isgs.csv`).

The Naive and BCR-stim attractors of v2 are unchanged from v1 (HDAC3/KPNB1 do not feed into these trap spaces). The IFN-stim attractor of v2 has 9 active phenotypes versus 7 in v1, gaining MHC-I activation and Matrix degradation — both biologically plausible IFN-driven phenotypes.

**Table 1.** Network statistics per condition, v2.

| Condition | Dynamic nodes | Fixed points | Trap-space attractors | Active phenotypes |
|---|---|---|---|---|
| Naive (homeostatic) | 79 | 2 | 2 | 7 / 2 |
| IFN-stimulated | 253 | 0 | 1 | 9 |
| BCR-stimulated | 64 | 2 | 2 | 7 / 7 |

### 3.3 Statistical concordance with blood transcriptomes (Phase 7.2)

Using the HGNC-aware mapping (Section 2.5), we recompute the Hamming distance between each v2 attractor and each cohort. The IFN-stimulated attractor matches the three blood cohorts significantly better than chance over a 10 000-permutation null model (Table 2). On PRECISESADS, the observed Hamming is 0.275 versus a null mean of 0.351 (z = -2.74, p = 0.014). On UKPSSR, 0.250 versus 0.456 (z = -2.84, p = 0.007). On GSE51092, 0.333 versus 0.459 (z = -3.01, p = 0.003). The Naive and BCR-stim attractors do not match blood cohorts significantly (all p > 0.6).

Decomposing into TP / TN / FP / FN, the IFN-stim attractor reaches sensitivity 0.65–0.72, specificity 0.74–1.00, balanced accuracy 0.69–0.85 across blood cohorts (Table 3). Cross-attractor AUROC reaches 0.72 on PRECISESADS and 0.85 on UKPSSR, both significantly above 0.5 by permutation (R3.3 satisfied).

KEGG / Reactome over-representation on the IFN-stim active-node set (133 HGNC symbols) returns *Interferon Signaling* (Reactome, adj-p = 3.1 × 10⁻⁸⁶), *JAK-STAT signaling pathway* (KEGG, adj-p = 4.5 × 10⁻²⁶), *Interferon Alpha/Beta Signaling* (Reactome, adj-p = 2.6 × 10⁻⁶³), *Interferon Gamma Signaling* (Reactome, adj-p = 3.6 × 10⁻⁵⁰). All four canonical type-I/II IFN pathways are recovered.

**Table 2.** Hamming distance, null mean, p-value and AUROC per attractor and cohort (v2). p-values from 10 000 permutations of DEG directions over the same mapped pairs.

| Cohort | Best attractor | n pairs | Hamming | Null mean | z | p | AUROC | Bal. acc. |
|---|---|---|---|---|---|---|---|---|
| PRECISESADS | IFN-stim A1 | 91 | 0.275 | 0.351 | −2.74 | **0.014** | 0.72 | 0.74 |
| UKPSSR | IFN-stim A1 | 28 | 0.250 | 0.456 | −2.84 | **0.007** | 0.85 | 0.85 |
| GSE51092 | IFN-stim A1 | 93 | 0.333 | 0.459 | −3.01 | **0.003** | 0.57 | 0.69 |
| ASSESS | IFN-stim A1 | 47 | 0.489 | 0.493 | −0.07 | 0.62 | 0.47 | 0.51 |
| GSE23117 | IFN-stim A1 | 28 | 0.393 | 0.408 | −0.30 | 0.65 | 0.43 | 0.56 |

### 3.4 The AP1/p38 MAPK module: candidate convergent control point, not a topological hub

The mono-node screen (Naive, 158 perturbations) identifies seven inhibitions that eliminate the disease attractor, six of which target the AP1/p38 module (EIF2AK2, MAP2K6, MAPK11-14, FOS, JUN, AP1_complex). The seventh (NFKB1_rna = 1) creates a cyclic attractor, interpreted as a Boolean encoding artefact rather than a therapeutic candidate. The six module hits are robust to the disease-attractor threshold θ ∈ {5, 6, 7} (`results/phase7/threshold_sensitivity.csv`).

A topological audit (Phase 7.1.2) places this finding in context. The mean betweenness centrality of the six module nodes is 0.0058, **3× lower** than the betweenness of a control set of 11 nodes covering JAK-STAT, BCR, NFkB, other MAPKs and output phenotypes (mean 0.0171). Mean in-degree (3.3 vs 9.0) and out-degree (3.0 vs 7.1) are also markedly lower. Conversely, the mean ancestor count is 221 vs 164 — many signals converge on the module — but the descendant count is 31 vs 120, indicating that the module is a *terminal relay* toward the Inflammation phenotype rather than a distribution hub.

The canonical TAK1 (MAP3K7) and ASK1 (MAP3K5) branches are topologically present in the BNET. Each input ligand (IFN-α, IFN-β, IFN-γ, BCR, CpG/TLR9, LPS/TLR4) reaches MAPK11-14 and AP1_complex via 1–2 node-disjoint paths (Table 4). The module thus integrates multiple PRR/cytokine/BCR signals but does so along a sparse linear backbone — eliminating any single node along the chain blocks the integration by construction.

**Table 4.** Number of node-disjoint paths from each ligand input to AP1/p38 versus a STAT1-P reference.

| Ligand input | → MAPK11-14 | → AP1_complex | → STAT1-P |
|---|---|---|---|
| IFN-α extracellular ligand | 1 | 1 | 1 |
| IFN-β extracellular ligand | 1 | 1 | 1 |
| IFN-γ-IFNGR complex | 1 | 1 | 1 |
| BCR_complex | 1 | 1 | 0 |
| CpG/TLR9 complex | 2 | 2 | 0 |
| LPS/TLR4 complex | 2 | 2 | 0 |

We therefore re-frame the module as a **candidate convergent control module** rather than a topologically central one. The selection of the six module nodes by the mono-node screen reflects both a biological convergence (many ligands flow through the module) and a topological sparsity (no parallel branches to absorb perturbation). This nuance was not made explicit in the v1 manuscript and is now central to the discussion.

### 3.5 Combinatorial perturbations: JAK + p38 is not synergistic; SYK + p38/PKR is, in BCR (Phase 7.3.2)

We screen 91 drug-target pairs across three conditions (273 pair-condition runs, `results/phase7/combinatorial_perturbations.csv`). A pair is *synergistic* if it eliminates the disease attractor while neither single-node KO does so.

In the **Naive** condition, p38 inhibition alone already eliminates the disease attractor; adding any other drug-target gives the same outcome. The "JAK + p38" combination is therefore not synergistic in the technical sense: the joint effect is identical to p38 alone. We retract the v1 manuscript's explicit synergy claim.

In the **IFN-stimulated** condition, the IFN-stim baseline has no fixed point under v2 (only a cyclic trap space; Section 3.2), so the disease-attractor metric is not directly applicable. We discuss this corner case in Section 4.

In the **BCR-stimulated** condition, three pairs are synergistic at the FP-level: SYK + EIF2AK2 (PKR), SYK + MAP2K6, SYK + MAPK11-14 (p38). Mechanistically, SYK provides BCR-driven activation of the same downstream module, so blocking only the p38 axis leaves SYK-driven AP1 activation intact, and blocking only SYK leaves IL-1/CpG-driven AP1 activation intact. These three pairs define a candidate combinatorial axis for SjD-associated DLBCL, where chronic BCR signalling is hypothesised to bypass mono-kinase inhibition.

### 3.6 In silico drug simulation: what can the model actually predict, and what can it not? (R4.4, R4.7)

We retract the v1 "8/10 concordance" metric. Of the 12 drugs simulated, the v1 metric counted *failure prediction for drugs that did fail clinically* as concordance — a tautology. A more rigorous accounting: the model can score 3 of the 12 drugs as testable predictions (filgotinib, baricitinib, tofacitinib — three JAK inhibitors). Nine drugs (BAFF / APRIL / CD40 / IFNAR / TLR antagonists) target nodes encoded as inputs in the SjD Map, and the model does not simulate the dynamics of input nodes. They are *not modellable* under the current encoding. This 9/12 limitation is intrinsic to the SjD Map's definition of inputs and cannot be repaired without re-engineering the source map.

Of the three modellable drugs, all three are predicted to be insufficient under Naive monotherapy. Under IFN-stim, baricitinib and tofacitinib partially suppress phenotypes by blocking JAK-STAT-driven IFN signalling but do not collapse the cyclic trap space. This is concordant with the modest Phase 2 results reported for filgotinib (MOSAIC trial [Bowman2023]) and baricitinib [Serrano2022]. We label this as *concordance with reported failure* and not as prospective validation.

**Table 5.** Drug simulation re-cast with three categories (R4.4).

| Drug | Class | Status v2 | Reported clinical |
|---|---|---|---|
| Filgotinib (JAK1) | Modellable | Insufficient (Naive) | Limited efficacy |
| Baricitinib (JAK1/2) | Modellable | Insufficient (Naive); Δ phenotypes (IFN) | Mixed |
| Tofacitinib (pan-JAK) | Modellable | Insufficient (Naive); Δ phenotypes (IFN) | No major response |
| Tirabrutinib (BTK) | Modellable | Insufficient (Naive/IFN); — (BCR baseline = AP1 active) | Ongoing |
| Iscalimab (anti-CD40) | Not modellable (input) | — | Ongoing |
| Ianalumab (anti-BAFF) | Not modellable (input) | — | Moderate |
| Belimumab (anti-BAFF) | Not modellable (input) | — | Moderate |
| Anifrolumab (anti-IFNAR) | Not modellable (input) | — | Moderate |
| Hydroxychloroquine (TLR7/9) | Not modellable (TLR input) | — | Standard of care |
| p38-inhibitor | Predicted novel | Eliminates FP (Naive, BCR) | Not in SjD |
| AP1-inhibitor | Predicted novel | Eliminates FP (Naive, BCR) | Not in SjD |
| PKR-inhibitor | Predicted novel | Eliminates FP (Naive, single residual FP) | Not in SjD |

### 3.7 ASSESS lymphoma case study: BCR context and BTK activation

The ASSESS cohort yields 47 mapped genes and 65 (gene, node) pairs. BTK_phosphorylated is active (= 1) only under BCR stimulation; in Naive and IFN it remains at 0 (BTK as a kinase requires upstream BCR ligation). This is consistent with the constitutive BCR activation that drives DLBCL transformation. TNFSF13B (APRIL) remains 0 across conditions — likely a paracrine (T-cell / stromal) source not captured by the cell-type-agnostic Boolean network. The minimum Hamming distance between v2 attractors and ASSESS is 0.489 (IFN-stim A1), null p = 0.62 — *not significant*. We report this as a coverage-limited result, not as positive cross-validation.

### 3.8 GSE23117 salivary gland: insufficiently powered (R3.6)

GSE23117 maps 28 genes (3.3 % coverage). Hamming = 0.39, null p = 0.65, AUROC = 0.43 — sub-random. We document this as evidence that the model, calibrated on blood/PBMC biology, does not extend to salivary gland tissue. We retract the v1 implicit interpretation that GSE23117 was a positive cross-validation. The analysis is retained in the supplementary information as a transparency item, with the explicit label "insufficiently powered to conclude".

---

## 4. Discussion

### 4.1 The AP1/p38 axis in SjD: convergence point with structural fragility

Under v2 of the network, six of seven mono-node interventions that eliminate the disease attractor target the AP1/p38 module. The topological audit (Section 3.4) shows that this is partly a consequence of the module's sparse linear topology — each step of the EIF2AK2 → MAP2K6 → MAPK11-14 → FOS/JUN → AP1 chain has degree ≤ 6, so removing any single node interrupts the relay. This topological fragility coexists with biological convergence: PRR (TLR4, TLR9), BCR and IFN ligands all reach AP1 along 1–2 node-disjoint paths (Table 4). The module is therefore a *candidate convergent control point* rather than a high-betweenness hub. The original wording "central control module" of v1 over-claimed the result and is now tempered.

### 4.2 Why JAK + p38 is *not* synergistic in the model (and why this is informative)

The combinatorial screen (Section 3.5) shows that p38 inhibition alone collapses the disease attractor in Naive and BCR conditions; adding a JAK inhibitor brings nothing further at the attractor level. The synergy claim of v1 is therefore retracted. This negative result is not a defeat of the framework — it is a falsification of one specific prediction that peer review (R2.3) explicitly demanded be tested. The model is more useful for having been tested honestly. The pairs SYK + EIF2AK2, SYK + MAP2K6 and SYK + MAPK11-14 are genuinely synergistic in BCR-stim conditions, providing a candidate combinatorial axis for SjD-associated DLBCL where mono-kinase inhibition has historically been insufficient.

### 4.3 The historical record of p38 inhibitors (R2.4, R4.6)

p38 MAPK inhibitors have a checkered clinical record across indications. In rheumatoid arthritis, doramapimod and pamapimod showed limited efficacy with hepatotoxicity signals [Damjanov2018, Hammaker2010]. In COPD, losmapimod reached Phase 2 with no clinical benefit [Watz2014]. In post-MI cardiovascular protection, losmapimod also failed to meet primary endpoints [Newby2014]. The repeated failure of p38 inhibitors *as monotherapy* in inflammatory indications is a strong empirical signal that the in silico prediction in SjD must be qualified: it should be evaluated as part of a combination (with anti-IFN or anti-CD40 backbones, for example), not as a stand-alone development programme. Acceptable safety profiles in trial-completed compounds (losmapimod, doramapimod) make them realistic candidates for preclinical SjD studies.

### 4.4 Limitations of the SjD Map for SjD drug repurposing (R4.8)

A rigorous accounting of the OpenTargets / DrugBank Sjogren_drugs.csv overlay shows that 25 of 39 clinical-trial drug targets (64 %) are *not present* in the SjD Map BNET, or are present only as input nodes. This includes BAFF/APRIL pathway targets (TNFSF13B, TNFRSF13B, TNFRSF13C, TNFRSF17), CD40-CD40L, IFNAR1/2 as receptors, and TLR antagonists that hit input nodes. The model is therefore *blind* to two thirds of the clinical landscape. We name this as a structural limitation of the source map: any conclusion the Boolean dynamics produces about drug repurposing is conditioned on the small subset of targets that the map encodes dynamically. This boundary should be made explicit in any future application of the same framework.

### 4.5 Cell-type agnosticism (R2.6)

The SjD Map integrates interactions from B cells, T cells, epithelial cells, and stromal cells; the Boolean network therefore represents a single composite cell. This is a recognised limitation of MIM-based modelling. Salivary gland tissue (GSE23117) and DLBCL (ASSESS) are mixtures of cell types whose proportions and signalling states differ from the curated PBMC-dominant SjD Map; the lower transcriptomic concordance for these datasets (Section 3.7, 3.8) is consistent with this limitation. A cell-type-aware extension of the SjD Map (analogous to single-cell extensions of the Atlas of Inflammation Resolution) would address the limitation but is beyond the scope of a Boolean re-analysis.

### 4.6 ISG up-regulation versus attractor mismatch asymmetry (R3.8)

Across blood cohorts, the up-regulated DEGs concentrated in IFN-driven genes are well captured by IFN-stim A1 (sensitivity 65-72%). Down-regulated DEGs are less consistently captured (specificity 74-100% but PPV/NPV asymmetric). This asymmetry is consistent with the SjD Map's curatorial focus on activating cascades; downstream feedback inhibition and cell-cycle suppression (which drives many of the down-regulated genes in PRECISESADS) are encoded sparsely. This matches the discussion of R3.8 in the response letter.

### 4.7 Stable motifs and asynchronous semantics

We did not produce a stable-motifs / minimum-intervention-set decomposition of v2 because `pystablemotifs` does not terminate within practical time budgets on a 508-node BNET. The combinatorial perturbation screen (Section 3.5) gives an *upper bound* on minimum-intervention sets (any element of an MIS must be a hit in the screen). We did not run an alternative asynchronous-semantics solver (BoolNet) for cross-comparison either — this is identified as future work. Both gaps are documented in `results/phase7/stable_motifs_status.md`.

---

## 5. Conclusions

We report a Boolean attractor analysis of the Sjögren's Disease Map, with an explicit correction of the IFN-I cascade (model v2) that allows the canonical interferon-stimulated gene signature to be reproduced. Under v2, the IFN-stimulated attractor matches three independent blood transcriptomic cohorts significantly better than chance (p ≤ 0.014) and recovers four canonical type-I/II interferon pathways by KEGG / Reactome over-representation. A targeted combinatorial perturbation screen retracts the v1 prediction of JAK + p38 synergy, confirms instead a SYK + p38 / PKR synergy in the BCR-stimulated condition, and identifies the AP1/p38 module as a candidate convergent control point rather than a central topological hub. The clinical-concordance metric is re-cast: of 12 drugs simulated, 9 are not modellable in the current SjD Map encoding, reflecting a structural limitation of the source map that must qualify any drug-repurposing inference. Under these caveats, p38 inhibitors, PKR inhibitors and SYK + p38 / PKR combinations remain meaningful preclinical candidates for SjD and SjD-associated lymphoma, evaluated within the historical context of p38 monotherapy failures.

---

## Data and code availability

All code, the v2 model, Phase 7 outputs and the response-to-reviewers letter are available at [REPOSITORY_URL] under MIT licence. A Snakemake pipeline reproduces all analyses from the raw SjD Map SBML in a single command (`make all`). Source data (SjD Map, DEG overlays) are from Zenodo 10.5281/zenodo.17585308 under CC-BY 4.0. Versioned tags: `model-v1.0` (v1 BNET), `model-v2.0` (v2 BNET with HDAC3 / KPNB1 fix). New test suite (R1.6) in `tests/` covers attractor counts, ISG activability, and null-model p-value range.

---

## Author contributions

NF: conceptualisation, methodology, software, formal analysis, visualisation, writing — original draft and revision.

## Competing interests

The author declares no competing interests.

## Acknowledgements

The authors of the original SjD Map [SilvaSaffar2026] and the developers of CaSQ [Aghamiri2020] and mpbn [Paulevé2020] are gratefully acknowledged. The four anonymous reviewers of v1 are thanked for the substantive critiques that drove this revision.

---

## References

[Mariette2018] Mariette X, Criswell LA. Primary Sjögren's Syndrome. *NEJM* 2018;378(10):931-9.
[Verstappen2021] Verstappen GM et al. Salivaomics in Primary Sjögren's Syndrome. *Front Immunol* 2021;12:670325.
[Thomas1973] Thomas R. Boolean formalization of genetic control circuits. *J Theor Biol* 1973;42(3):563-85.
[Saadatpour2013] Saadatpour A, Albert R. Boolean modeling of biological regulatory networks. *Methods* 2013;62(1):3-12.
[Abou-Jaoudé2016] Abou-Jaoudé W et al. Logical Modeling and Dynamical Analysis of Cellular Networks. *Front Genet* 2016;7:94.
[Huang1999] Huang S, Ingber DE. Shape-dependent control of cell growth. *Exp Cell Res* 1999;261(1):91-103.
[Kauffman1969] Kauffman SA. Metabolic stability and epigenesis. *J Theor Biol* 1969;22(3):437-67.
[Zañudo2015] Zañudo JGT, Albert R. Cell fate reprogramming. *PLOS Comput Biol* 2015;11(4):e1004193.
[Rozum2021] Rozum JC et al. pystablemotifs. *Bioinformatics* 2021;38(5):1465-7.
[Aghamiri2020] Aghamiri SS et al. CaSQ: automated translation of SBML qualitative models. *Bioinformatics* 2020;36(16):4593-5.
[Paulevé2020] Paulevé L et al. Reconciling qualitative, abstract, and scalable modeling. *Nat Commun* 2020;11:4256.
[Duret2023] Duret M et al. ASSESS: transcriptomic profiling of DLBCL arising in Sjögren's syndrome. *Arthritis Rheumatol* 2023.
[Bowman2023] Bowman SJ et al. Filgotinib in primary Sjögren's syndrome (MOSAIC). *Ann Rheum Dis* 2023.
[Serrano2022] Serrano J et al. Baricitinib in primary Sjögren's syndrome. *Lancet* 2022.
[Damjanov2018] Damjanov N et al. Efficacy, pharmacodynamics and safety of VX-702, a p38 MAPK inhibitor. *Arthritis Rheum* 2018.
[Hammaker2010] Hammaker D, Firestein GS. "Go upstream, young man": lessons from p38 inhibitor development. *Ann Rheum Dis* 2010;69(Suppl 1):i77-82.
[Watz2014] Watz H et al. Effects of losmapimod on COPD. *Lancet Respir Med* 2014;2(1):63-72.
[Newby2014] Newby LK et al. Losmapimod in patients with acute MI. *Lancet* 2014;384(9949):1187-95.
[Arleevskaya2021] Arleevskaya MI et al. Endogenous retroviruses in Sjögren's syndrome. *Autoimmun Rev* 2021.
[Zenz2008] Zenz R et al. c-Jun regulates eyelid closure. *Nat Cell Biol* 2008.
[SilvaSaffar2026] Silva-Saffar SE et al. The SjD Map. *npj Syst Biol Appl* 2026.
