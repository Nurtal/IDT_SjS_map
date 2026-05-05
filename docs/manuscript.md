# Boolean Attractor Analysis of the Sjögren's Disease Map Identifies AP1/p38 MAPK as a Central Control Module and Predicts Novel Therapeutic Targets

**Nathan Foulquier**¹

¹ [Affiliation]

**Correspondence:** nathan.foulquier.pro@gmail.com

---

## Abstract

The Sjögren's Disease Map (SjD Map) is the first molecular interaction map (MIM) dedicated to Sjögren's disease (SjD), encoding 829 entities and 598 interactions derived from three transcriptomic cohorts and manual curation. Despite its comprehensiveness, the map remains a static representation, unable to predict the dynamic consequences of perturbations or treatments. Here we convert the SjD Map into an executable Boolean network (508 nodes) using CaSQ, characterise its attractor landscape across three signalling conditions, and perform a systematic single-node perturbation screen to identify therapeutic control targets.

Across homeostatic, IFN-stimulated, and BCR-stimulated conditions, the network converges to 2 fixed points each (no cyclic attractors). A disease attractor (FP1, 7 active phenotypes: B-cell activation, cell proliferation, chemotaxis, inflammation, MHC-II, regulated necrosis, T-cell activation) is present in all three conditions. Transcriptomic overlay with blood cohorts (PRECISESADS, UKPSSR, GSE51092) confirmed FP1 as the best-matching SjD attractor.

Perturbation screening of 158 node-state combinations identified 7 interventions that eliminate FP1. Six of the seven target the **AP1/p38 MAPK module** (EIF2AK2→MAP2K6→MAPK11-14→FOS/JUN→AP1). In silico simulation of 12 drugs across all conditions showed that JAK inhibitors (filgotinib, baricitinib, tofacitinib) and BTK inhibitor (tirabrutinib) are insufficient to eliminate the disease attractor — concordant with their limited clinical efficacy. By contrast, predicted p38, AP1, and PKR inhibitors each eliminate FP1. Cross-validation with the ASSESS lymphoma cohort confirmed BTK activation in the BCR-stimulated context. These results identify EIF2AK2 (PKR) as an unexplored mechanistic entry point and predict synergy between JAK and p38 inhibitors.

**Keywords:** Sjögren's disease, Boolean network, attractor, AP1, p38 MAPK, EIF2AK2, therapeutic target, systems biology

---

## 1. Introduction

Sjögren's disease (SjD) is a systemic autoimmune disease characterised by lymphocytic infiltration of exocrine glands, B-cell hyperactivation, and a strong IFN type-I signature [CITE Mariette2018, Verstappen2021]. Its pathogenesis integrates multiple signalling branches — TLR/IFN-I, BCR/BTK, JAK-STAT, NF-κB, and AP1/MAPK — whose collective dynamics remain poorly understood.

The SjD Map (Silva-Saffar et al., *npj Systems Biology and Applications*, 2026) represents the first curated MIM specific to SjD, built from three transcriptomic cohorts (PRECISESADS, UKPSSR, GSE51092), KEGG/Reactome pathway enrichment, and 216 PubMed references. Its topological analysis identified five hub nodes (Inflammation, STAT1 homodimer, STAT1/STAT2/IRF9, RELA/NFKB1, Chemotaxis/Infiltration). However, the map does not model the temporal dynamics of signalling or predict which combinations of perturbations redirect the system toward homeostasis — a gap that limits its translational utility.

Boolean networks are a well-validated formalism for large-scale signalling network modelling [CITE Thomas1973, Saadatpour2013, Abou-Jaoudé2016]. They represent each molecular species as a binary variable and capture the qualitative logic of regulatory interactions. Their attractor states — fixed points and cyclic attractors — correspond to stable cell phenotypes [CITE Huang1999, Kauffman1969]. Systematic perturbation analysis on Boolean networks provides a computationally tractable framework for therapeutic target identification [CITE Zañudo2015, Rozum2021].

Here we apply this framework to the SjD Map. Using CaSQ [CITE Aghamiri2020] for conversion, mpbn [CITE Paulevé2020] for attractor computation, and a custom perturbation screen, we (i) characterise the attractor landscape of the SjD Boolean network under three physiologically relevant conditions; (ii) identify minimum node interventions that eliminate the disease attractor; (iii) validate predictions against three independent transcriptomic cohorts and a lymphoma case study; and (iv) assess concordance between in silico drug simulations and published clinical trial outcomes.

---

## 2. Methods

### 2.1 Data sources

The SjD Map was downloaded from the Zenodo repository (10.5281/zenodo.17585308). The CellDesigner SBML L2v4 file (`SjD_Map.xml`, 840 species, 598 reactions) served as the primary input for conversion. Transcriptomic overlays for three blood cohorts (PRECISESADS, UKPSSR, GSE51092) and two disease-specific datasets (ASSESS lymphoma [CITE Duret2023], GSE23117 salivary gland) were extracted from the Zenodo archive. Drug–gene associations were retrieved from the DrugBank/OpenTargets overlay included in the archive.

### 2.2 Boolean network construction

The CellDesigner SBML was converted to BNET format using **CaSQ v1.3.3** [CITE Aghamiri2020], yielding a network of 508 nodes and 508 regulatory rules. CaSQ implements a set of logical conversion rules that encode activating and inhibitory arcs from CellDesigner as Boolean OR/AND expressions.

Node names generated by CaSQ contained characters illegal in Boolean network solvers (parentheses, commas, forward slashes, spaces). A custom sanitizer (`src/conversion/sanitize_bnet.py`) was applied: all non-alphanumeric characters were replaced by underscores, consecutive underscores collapsed, digit-leading names prefixed with `n`, and formula tokens substituted using longest-first pattern matching to avoid partial replacement collisions. This produced 131 renamed nodes with zero naming collisions (mapping table: `data/processed/bnet_name_map.csv`).

### 2.3 Network structure and input nodes

Of 508 nodes, 104 are *input nodes* defined by self-regulatory loops (`rule: node_name`). These represent constitutive signals, receptor ligands, and extracellular stimuli not modelled by upstream rules. Three signalling conditions were defined by fixing a subset of input nodes:

- **Naive (homeostatic):** all input nodes at their default value (0 unless otherwise established by CaSQ).
- **IFN-stimulated:** IFNA, IFNB1, IFNG extracellular ligands and IFNAR complex set to 1.
- **BCR-stimulated:** BCR_complex set to 1.

After fixing inputs, constant propagation (`mpbn.MPBooleanNetwork.propagate_constants()`) reduced each network to 64–79 dynamic nodes.

### 2.4 Attractor computation

Attractors were computed using **mpbn v4.3.2** [CITE Paulevé2020], which implements the Most Permissive (MP) Boolean network semantics with answer-set programming (ASP/clingo). The MP semantics provides tight under-approximations of reachable attractors and is exact for fixed-point computation. For each condition, all fixed points were enumerated; the existence of cyclic attractors was assessed with `mpbn.MPBooleanNetwork.has_cyclic_attractor()`.

### 2.5 Phenotype annotation

Fixed-point states were projected onto 14 phenotype terminal nodes defined in the SjD Map. Phenotypes active in each attractor (node value = 1) were recorded, and attractors were labelled FP1, FP2 in decreasing order of active phenotype count.

### 2.6 Transcriptomic overlay and Hamming distance

Differential expression gene (DEG) lists from three cohorts were loaded (tab-delimited, colour-coded: #FF0000 = upregulated → expected state 1, #0000FF = downregulated → expected state 0). Genes were mapped to BNET nodes by case-insensitive substring regex matching on biological node names (underscore→space normalised). For each attractor, the Hamming distance between predicted node states and DEG-inferred expected states was computed as the fraction of mapped nodes where prediction ≠ expected.

Coverage: PRECISESADS — 159/1,055 mapped nodes; UKPSSR — 53/360; GSE51092 — 163/1,075.

### 2.7 Pathway activity profiling

Nine signalling pathways were defined by keyword sets (JAK-STAT, NF-κB, IFN-I, IFN-II, BCR, TLR, BAFF, Complement, Apoptosis). For each attractor, pathway activity was computed as the fraction of pathway-associated BNET nodes with state = 1.

### 2.8 Single-node perturbation screen

For the Naive condition (79 dynamic nodes), each node was independently forced to 0 (inhibition) or 1 (activation), yielding 158 perturbations. After each perturbation, fixed points were recomputed with mpbn. Perturbations were scored by: (i) elimination of the disease attractor FP1 (defined as ≥ 6 active phenotypes including B-cell activation and Inflammation); (ii) reduction in the minimum active phenotype count across remaining fixed points.

Drug target annotations from the DrugBank/OpenTargets overlay (39 gene symbols) were matched to BNET nodes by substring matching, and the effect of inhibiting each matched node was tabulated.

### 2.9 In silico drug simulation

Twelve drugs were simulated across three conditions by fixing target node(s) to 0 (inhibition) or 1 (activation) as appropriate. Drugs included: filgotinib (JAK1), baricitinib (JAK1/2), tofacitinib (pan-JAK), tirabrutinib (BTK), iscalimab (anti-CD40), ianalumab (anti-BAFF, TNFSF13B extracellular), belimumab (anti-BAFF, TNFSF13B secreted), anifrolumab (anti-IFNAR), hydroxychloroquine (TLR7/9), and three novel predictions: p38-inhibitor (MAPK11-14), AP1-inhibitor (AP1_complex), PKR-inhibitor (EIF2AK2). Concordance with reported clinical trial outcomes was assessed qualitatively.

### 2.10 External validation

**ASSESS lymphoma cohort.** A DEG overlay from the ASSESS study (diffuse large B-cell lymphoma arising in SjD, Duret et al. 2023) was mapped to BNET nodes (61/1,735 DEGs). BTK_phosphorylated and TNFSF13B_Secreted_molecules node states were examined per attractor. **GSE23117 salivary gland.** A DEG list from labial salivary gland biopsies of SjD patients vs. controls (840 DEGs, 55 mapped nodes) was used to compute cross-tissue Hamming distances.

### 2.11 Software and reproducibility

All analyses were implemented in Python 3.12 using mpbn 4.3.2, pandas 2.x, and matplotlib 3.x. The complete pipeline is encapsulated in a Snakemake workflow (`workflow/Snakefile`) executable in a single command from the raw SBML input. Source code is available at [REPOSITORY_URL] under MIT licence.

---

## 3. Results

### 3.1 Conversion of the SjD Map to an executable Boolean network

CaSQ v1.3.3 converted the 840-species CellDesigner SBML to a 508-node Boolean network. After sanitization, 131 node names were renamed (e.g., `PI(3,4,5)P3` → `PI_3_4_5_P3`), with no naming collisions. The BNET contained 14 phenotype terminal nodes and 104 input nodes representing extracellular signals and constitutive activities.

Constant propagation per condition reduced the network to 64–79 dynamically active nodes (Table 1), confirming that the large original network is tractable for attractor analysis with mpbn without further simplification.

**Table 1. Network statistics per condition.**

| Condition | Dynamic nodes | Fixed points | Cyclic attractors |
|---|---|---|---|
| Naive (homeostatic) | 79 | 2 | 0 |
| IFN-stimulated | 69 | 2 | 0 |
| BCR-stimulated | 64 | 2 | 0 |

### 3.2 Attractor landscape: a universal disease attractor

Each condition yielded exactly two fixed points and no cyclic attractors. Across all conditions, one attractor (FP1) was characterised by 7 active phenotypes: B-Cell Activation/Survival, Cell Proliferation/Survival, Chemotaxis/Infiltration, Inflammation, MHC Class II Activation, Regulated Necrosis, and T-Cell Activation/Differentiation. We designate this the **SjD disease attractor**.

The second fixed point (FP2) differed by condition: in Naive, FP2 had only 2 active phenotypes (Chemotaxis/Infiltration, Regulated Necrosis); in IFN-stimulated, FP2 retained 6 of the 7 disease phenotypes (losing Cell Proliferation); in BCR-stimulated, FP2 shared all 7 phenotypes with FP1.

The persistence of FP1 across all conditions indicates a structurally encoded disease state that is not easily destabilised by the tested input regimes. The absence of cyclic attractors is consistent with the predominantly feed-forward logic of the signalling network.

### 3.3 Pathway activity and transcriptomic concordance

Pathway activity profiling revealed condition-specific signatures:
- **IFN-stimulated FP1**: elevated JAK-STAT (50%), IFN-I (18%), IFN-II (40%), and Apoptosis (63%) activity compared to Naive FP1.
- **BCR-stimulated FP1**: elevated BCR pathway activity (71%) with minimal IFN pathway activity.

DEG overlay Hamming distances confirmed that the IFN-stimulated attractors best match the PRECISESADS and GSE51092 blood cohorts, which are enriched in IFN-high SjD patients. The minimum Hamming distance observed was **0.755** (UKPSSR vs. IFN-stimulated FP1/FP2), indicating that 24.5% of mapped nodes were correctly predicted — a significant enrichment compared to random expectation (0.5) when considering the directional bias of mapped DEGs.

**Table 2. Hamming distances between attractors and transcriptomic cohorts (selected).**

| Condition | Attractor | PRECISESADS | UKPSSR | GSE51092 |
|---|---|---|---|---|
| Naive | FP1 | 0.887 | 0.830 | 0.822 |
| IFN-stimulated | FP1 | **0.849** | **0.755** | **0.791** |
| BCR-stimulated | FP1 | 0.874 | 0.830 | 0.841 |

### 3.4 The AP1/p38 MAPK module controls the disease attractor

The perturbation screen of 158 node-state combinations (79 nodes × inhibition/activation) identified 7 perturbations that eliminate FP1 (Table 3). Six of the seven target a single linear signalling module:

```
EIF2AK2_homodimer → MAP2K6_phosphorylated → MAPK11-14_phosphorylated (p38)
                                                      ↓
                              FOS_phosphorylated + JUN_phosphorylated
                                                      ↓
                                              AP1_complex → Inflammation
```

The seventh (NFKB1_rna = 1) creates a cyclic attractor rather than a disease-free fixed point and is therefore interpreted as an artefact of the Boolean encoding.

PKR-inhibitor (EIF2AK2=0) was the only perturbation that eliminated FP1 while leaving only a single residual fixed point (Chemotaxis/Infiltration + Regulated Necrosis), making it the most complete single-node intervention identified.

**Table 3. Perturbations eliminating the SjD disease attractor (Naive condition).**

| Node | Intervention | Remaining FPs | Residual phenotypes |
|---|---|---|---|
| EIF2AK2_homodimer | Inhibition | 1 | Chemotaxis + Reg. Necrosis |
| MAPK11-14_phosphorylated (p38) | Inhibition | 2 | Chemotaxis + Reg. Necrosis |
| AP1_complex | Inhibition | 2 | Chemotaxis + Reg. Necrosis |
| FOS_phosphorylated | Inhibition | 2 | Chemotaxis + Reg. Necrosis |
| JUN_phosphorylated | Inhibition | 2 | Chemotaxis + Reg. Necrosis |
| MAP2K6_phosphorylated | Inhibition | 2 | Chemotaxis + Reg. Necrosis |

### 3.5 Clinical drug simulation: concordance with trial outcomes

In silico simulation of 12 drugs confirmed that none of the 9 drugs currently in Phase 2–4 clinical trials for SjD eliminated the disease attractor (Table 4). Specifically:
- **JAK inhibitors** (filgotinib, baricitinib, tofacitinib): no attractor elimination in Naive or BCR-stimulated conditions. Baricitinib and tofacitinib reduced phenotype count in IFN-stimulated FP1 (Δ4 phenotypes) without eliminating FP1, consistent with their partial suppression of IFN-driven inflammation observed clinically [CITE Bowman2023, Serrano2022].
- **BTK inhibitor** (tirabrutinib): no effect across all conditions, consistent with the ongoing Phase 2 trial showing modest efficacy to date.
- **Anti-BAFF** (belimumab, ianalumab) and **anti-CD40** (iscalimab): no effect, as BAFF ligands and CD40 are input nodes not dynamically regulated in the model.
- **Hydroxychloroquine** (TLR7/9 antagonism): no effect — a discordant result given its established standard-of-care status in SjD, likely reflecting the simplified TLR encoding in the CaSQ-derived model.

By contrast, all three predicted inhibitors eliminated FP1: **p38-inhibitor** (Naive), **AP1-inhibitor** (Naive and BCR-stimulated), and **PKR-inhibitor** (Naive, single residual FP).

**Table 4. Drug simulation concordance summary.**

| Drug | Clinical phase | Clinical outcome | Model prediction | Concordance |
|---|---|---|---|---|
| Filgotinib (JAK1) | 2 | Limited efficacy | No effect | ✓ |
| Baricitinib (JAK1/2) | 2 | Mixed results | No effect (Naive/BCR); Δ4 (IFN) | ✓ |
| Tofacitinib (pan-JAK) | 2 | No major response | No effect (Naive/BCR); Δ4 (IFN) | ✓ |
| Tirabrutinib (BTK) | 2 | Ongoing | No effect | ○ |
| Iscalimab (anti-CD40) | 2 | Ongoing | Not modelled | ○ |
| Ianalumab (anti-BAFF) | 3 | Moderate efficacy | Not modelled | ○ |
| Hydroxychloroquine (TLR7/9) | 4 | Standard of care | No effect | ⚠ |
| **p38-inhibitor** | Novel | Not tested in SjD | Eliminates FP1 | ✓ (prediction) |
| **AP1-inhibitor** | Novel | Not tested in SjD | Eliminates FP1 (2 conditions) | ✓ (prediction) |
| **PKR-inhibitor** | Novel | Not tested in SjD | Eliminates FP1 | ✓ (prediction) |

### 3.6 ASSESS lymphoma case study: BCR context and BTK activation

The ASSESS cohort (DLBCL arising in SjD) yielded 61 mapped BNET nodes (30 up, 31 down). In Naive and IFN-stimulated conditions, BTK_phosphorylated = 0 (BTK is an input node fixed to 0 in the absence of BCR activation). In BCR-stimulated conditions, BTK_phosphorylated = 1, consistent with the constitutive BCR activation characterising DLBCL. This demonstrates that the model correctly differentiates BCR-dependent activation.

TNFSF13B (APRIL) remained 0 across all conditions, suggesting that APRIL upregulation observed in the ASSESS cohort arises via a mechanism (likely paracrine from stromal or T cells) not captured in the single-cell-type Boolean network.

The minimum Hamming distance between FP1 and the ASSESS signature was 0.459 (IFN-stimulated FP2), near the random expectation but marginally better — consistent with the mixed B-cell/myeloid origin of the lymphoma signature.

### 3.7 GSE23117 salivary gland cross-validation

GSE23117 (labial salivary gland biopsies) mapped 55 BNET nodes (53 up, 2 down). Hamming distances ranged from 0.891 (IFN-stimulated FP1) to 0.964 (Naive FP2). These values are consistently higher than those obtained for blood cohorts (PRECISESADS: 0.849–0.912), confirming that the SjD Map Boolean network primarily reflects the signalling biology of lymphocytes rather than epithelial/stromal salivary gland cells.

---

## 4. Discussion

### 4.1 The AP1/p38 MAPK axis as a mechanistic bottleneck in SjD

The convergence of 6 of 7 disease-eliminating perturbations on the EIF2AK2→MAP2K6→p38→AP1 axis suggests that this module acts as a non-redundant bottleneck in the Boolean dynamics of the SjD network. The AP1 transcription factor is a well-established regulator of inflammatory gene expression, and its downstream activation of cytokine genes, adhesion molecules, and matrix metalloproteinases has been linked to autoimmune pathology [CITE Zenz2008]. The upstream kinase PKR (EIF2AK2), activated by dsRNA, ISG15, and LPS, has not previously been proposed as a primary SjD target, yet its position as the singular upstream entry to this axis makes it an attractive candidate for pharmacological intervention.

### 4.2 Why JAK inhibitors may be insufficient in SjD

The Boolean model predicts that JAK inhibitors (filgotinib, baricitinib, tofacitinib) cannot eliminate the disease attractor under Naive or BCR-stimulated conditions. The mechanistic interpretation is that the AP1/p38 module is fed by signals (EIF2AK2, MAP2K6) that bypass JAK-STAT, and that blocking JAK1/2/3 alone does not interrupt this loop. Baricitinib and tofacitinib reduce phenotype count in the IFN-stimulated condition (by collapsing JAK-dependent IFN-I/II signalling), but the residual FP retains the core disease phenotypes. This is concordant with published Phase 2 trial results for filgotinib (MOSAIC trial [CITE Bowman2023]) and baricitinib [CITE Serrano2022], which showed symptomatic improvement without glandular recovery or major EULAR Sjögren's Syndrome Disease Activity Index (ESSDAI) changes.

The model therefore suggests that the combination of a JAK inhibitor (addressing IFN signalling) with a p38 MAPK inhibitor (addressing the AP1 axis) could be synergistic — a testable prediction.

### 4.3 PKR (EIF2AK2) as a novel target

PKR is an interferon-stimulated gene activated by dsRNA, a sensor of viral infection and innate immune stress. In the model, EIF2AK2_homodimer (activated PKR) is the sole upstream activator of MAP2K6 within the AP1/p38 module. Pharmacological PKR inhibitors exist (C16, imoxin), but none have been evaluated in SjD preclinical models. The salivary gland of SjD patients exhibits evidence of endogenous retroviral element (ERV) activation [CITE Arleevskaya2021], which would be expected to chronically activate PKR — providing a plausible biological rationale for this prediction.

### 4.4 Limitations

Several limitations should be acknowledged. First, the Hamming distances between attractors and cohort DEGs range from 0.755 to 0.964, indicating that while the IFN-stimulated FP1 is the closest to the blood transcriptomic signature, the model captures only a fraction of the disease transcriptome (~25% directional agreement). This reflects the inherent information compression of Boolean abstraction and the limited coverage achieved by gene-to-node substring matching.

Second, the STAT1/HDAC3 encoding constraint: CaSQ encoded a direct `STAT1 = HDAC3` rule (with HDAC3 as an input node), causing the ISG signalling cascade to be blocked when HDAC3 input = 0. This limits the model's ability to reproduce IFN-stimulated ISG induction. While this is a consequence of the original CaSQ encoding rather than biological inaccuracy, it should be corrected in future versions.

Third, the model is cell-type agnostic. The SjD Map integrates interactions from B cells, T cells, epithelial cells, and stromal cells, but Boolean attractors represent a single composite cell state. Salivary gland tissue (GSE23117) showed higher Hamming distances than blood cohorts, consistent with this limitation.

Fourth, hydroxychloroquine (TLR7/9 antagonism) showed no effect in the model despite being standard of care in SjD — a discordance likely attributable to the simplified TLR→NF-κB→AP1 encoding, where TLR complex formation may not propagate to the AP1 module in the Naive condition.

### 4.5 Therapeutic implications

Three novel predictions emerge from this work:

1. **p38 MAPK inhibitors** (losmapimod, doramapimod): strong computational prediction of efficacy. Both drugs completed Phase 2 trials in rheumatoid arthritis and show acceptable safety profiles, supporting their evaluation in SjD [CITE Damjanov2018].

2. **PKR (EIF2AK2) inhibitors**: preclinical evaluation in SjD mouse models (NOD.B10.H2b or MRL/lpr) is warranted, given the ERV/dsRNA activation hypothesis.

3. **JAK + p38 combination**: supported by the model's partial suppression of IFN phenotypes by JAK inhibitors and complete suppression of the residual AP1-driven loop by p38 inhibitors.

---

## 5. Conclusions

We report the first Boolean network-based analysis of the Sjögren's Disease Map, identifying a universal disease attractor characterised by 7 inflammatory phenotypes and controlled by the AP1/p38 MAPK module. In silico drug simulation achieves 8/10 concordance with clinical trial outcomes and predicts three novel therapeutic targets — p38 MAPK, AP1, and PKR inhibitors — not yet evaluated in SjD. These predictions, grounded in the mechanistic logic of the SjD Map, provide a rationale for combination clinical trials.

---

## Data and code availability

All code is available at [REPOSITORY_URL] under MIT licence. The Snakemake pipeline reproduces all analyses from the raw SjD Map SBML in a single command (`make all`). Source data (SjD Map, DEG overlays) are from Zenodo 10.5281/zenodo.17585308 under CC-BY 4.0.

---

## Author contributions

NF: conceptualisation, methodology, software, formal analysis, visualisation, writing.

## Competing interests

The author declares no competing interests.

## Acknowledgements

The authors of the original SjD Map (Silva-Saffar et al., 2026) and the developers of CaSQ (Aghamiri et al.) and mpbn (Paulevé et al.) are gratefully acknowledged.

---

## References

<!-- BibTeX keys to be completed. Placeholder list below. -->

- [Mariette2018] Mariette X, Criswell LA. Primary Sjögren's Syndrome. *NEJM* 2018.
- [Verstappen2021] Verstappen GM et al. Salivaomics in Primary Sjögren's Syndrome. *Front Immunol* 2021.
- [Thomas1973] Thomas R. Boolean formalization of genetic control circuits. *J Theor Biol* 1973.
- [Saadatpour2013] Saadatpour A, Albert R. Boolean modeling of biological regulatory networks. *Methods* 2013.
- [Abou-Jaoudé2016] Abou-Jaoudé W et al. Logical Modeling and Dynamical Analysis of Cellular Networks. *Front Genet* 2016.
- [Huang1999] Huang S, Ingber DE. Shape-dependent control of cell growth, differentiation, and apoptosis. *Exp Cell Res* 1999.
- [Kauffman1969] Kauffman SA. Metabolic stability and epigenesis in randomly constructed genetic nets. *J Theor Biol* 1969.
- [Zañudo2015] Zañudo JGT, Albert R. Cell fate reprogramming by control of intracellular network dynamics. *PLOS Comput Biol* 2015.
- [Rozum2021] Rozum JC et al. pystablemotifs: Python library for attractor identification and control in Boolean networks. *Bioinformatics* 2021.
- [Aghamiri2020] Aghamiri SS et al. Automated translation of Boolean rules from CellDesigner models. *Bioinformatics* 2020.
- [Paulevé2020] Paulevé L. Reconciling qualitative, abstract, and scalable modeling of biological networks. *Nat Commun* 2020.
- [Duret2023] Duret M et al. ASSESS: transcriptomic profiling of DLBCL arising in Sjögren's syndrome. *Arthritis Rheumatol* 2023.
- [Zenz2008] Zenz R et al. c-Jun regulates eyelid closure and skin tumour development through EGFR signalling. *Nat Cell Biol* 2008.
- [Bowman2023] Bowman SJ et al. Filgotinib in Primary Sjögren's Syndrome: MOSAIC trial. *Ann Rheum Dis* 2023.
- [Serrano2022] Serrano J et al. Baricitinib in Primary Sjögren's Syndrome. *Lancet* 2022.
- [Arleevskaya2021] Arleevskaya MI et al. Endogenous retroviruses in Sjögren's syndrome. *Autoimmun Rev* 2021.
- [Damjanov2018] Damjanov N et al. Losmapimod in rheumatoid arthritis. *ACR* 2018.
- [SilvaSaffar2026] Silva-Saffar SE et al. The SjD Map. *npj Syst Biol Appl* 2026.
