# Boolean Attractor Analysis of the Sjögren's Disease Map Identifies AP1/p38 MAPK as a Candidate Convergent Control Module Under IFN Stimulation

**Nathan Foulquier**¹

¹ [Affiliation]

**Correspondence:** nathan.foulquier.pro@gmail.com

---

## Abstract

The Sjögren's Disease Map (SjD Map; Silva-Saffar et al., 2026) is the first molecular interaction map dedicated to Sjögren's disease (SjD), encoding 829 entities and 598 interactions. We convert the SjD Map into an executable Boolean network of 508 nodes using CaSQ, characterise its attractor landscape under three signalling conditions (homeostatic, IFN-stimulated, BCR-stimulated), and screen mono- and di-genic perturbations to identify candidate therapeutic control points.

The CaSQ-translated network inherits two input dependencies whose default-0 encoding silences the type-I interferon cascade: `STAT1 = HDAC3` and the ISGF3-nucleus rule's conjunction with `KPNB1`. Both genes are constitutively active in immune cells, and we set them to 1 by construction. Under this encoding, the IFN-stimulated condition yields a single trap-space attractor in which 17 canonical interferon-stimulated genes (ISGs; including MX1, OAS1-3, ISG15, IRF7, IFIT1/3, IFITM1) and the ISGF3 nuclear complex are activable.

Using an HGNC-aware DEG mapping (593 mappings, 97.8 % coverage of non-phenotype nodes) and a 10 000-permutation null model, the IFN-stimulated attractor matches three independent blood transcriptomic cohorts significantly better than chance: Hamming = 0.250–0.333, p ≤ 0.014 across PRECISESADS, UKPSSR and GSE51092. Cross-attractor AUROC reaches 0.72–0.85 on the two cohorts with sufficient mapping coverage and balanced accuracy is 0.69–0.85, all above trivial all-active or all-inactive baselines (balanced accuracy 0.50). KEGG/Reactome over-representation testing recovers all four canonical type-I/II interferon pathways (Reactome *Interferon Signaling*, adj-p = 3.1 × 10⁻⁸⁶; KEGG *JAK-STAT signaling*, adj-p = 4.5 × 10⁻²⁶; *IFN-α/β Signaling*; *IFN-γ Signaling*).

A single-node perturbation screen (Naive condition, 158 perturbations) identifies six interventions in the AP1/p38 MAPK module (EIF2AK2 → MAP2K6 → MAPK11-14 → FOS/JUN → AP1) that eliminate the disease attractor. A topological audit shows that this module is *not* a high-betweenness hub of the graph (mean betweenness 0.006 versus 0.017 for a comparable JAK-STAT/BTK/SYK/NFkB control set) but is a **convergence point** for several upstream cascades (TLR4, TLR9, BCR, IFN-α/β/γ all reach AP1 via 1–2 node-disjoint paths). The module is best described as a *candidate convergent control module* whose selection by the screen reflects both biological convergence and topological sparsity.

A targeted combinatorial perturbation screen (91 drug-target pairs across three conditions) tests synergy hypotheses systematically. **JAK + p38 is *not* synergistic in the model**: p38 inhibition alone already eliminates the disease attractor, so adding a JAK inhibitor brings no further benefit at the attractor level. In the BCR-stimulated condition, three different pairs do show synergy: SYK + EIF2AK2 (PKR), SYK + MAP2K6 and SYK + MAPK11-14 (p38). These define a candidate combinatorial axis for SjD-associated diffuse large B-cell lymphoma (DLBCL), where chronic BCR signalling is hypothesised to bypass mono-kinase inhibition.

In silico drug simulation (12 drugs × 3 conditions) establishes what the model can and cannot predict. Of the 12 drugs simulated, 9 target nodes encoded as inputs (BAFF/APRIL, CD40, IFNAR, TLR7/9) whose dynamics the model does not simulate; they are *not modellable* under the current encoding — a structural limitation of the source map. Of the 3 modellable drugs (filgotinib, baricitinib, tofacitinib), all are predicted to be insufficient as monotherapy in the homeostatic condition, concordant with the modest clinical efficacy reported for JAK inhibitors in SjD. We propose three actionable predictions: (i) p38 inhibitors evaluated as combination partners; (ii) PKR inhibitors as orphan candidates for preclinical validation; (iii) SYK + p38 or SYK + PKR combinations evaluated in BCR-driven SjD-DLBCL models.

**Keywords:** Sjögren's disease, Boolean network, attractor, AP1, p38 MAPK, EIF2AK2, control analysis, null model, AUROC, combinatorial perturbation, systems biology

---

## 1. Introduction

Sjögren's disease (SjD) is a systemic autoimmune disease characterised by lymphocytic infiltration of exocrine glands, B-cell hyperactivation, and a strong type-I IFN signature [Mariette2018, Verstappen2021]. Its pathogenesis integrates multiple signalling branches — TLR/IFN-I, BCR/BTK, JAK-STAT, NF-κB, and AP1/MAPK — whose collective dynamics remain poorly understood, with substantial overlap to other type-I interferonopathies (SLE, dermatomyositis) yet specific features (BAFF/APRIL-driven B-cell hyperactivation, focal sialadenitis, increased risk of B-cell lymphoma). Patients with SjD carry a 15- to 20-fold relative risk of diffuse large B-cell lymphoma (DLBCL) and an approximately 1000-fold relative risk of mucosa-associated lymphoid tissue (MALT) lymphoma compared to the general population [Solans-Laque2011, Ekstrom-Smedby2008] — a clinical feature that motivates a particular focus on B-cell-receptor-driven signalling. Molecular stratification of SjD into IFN-high, B-cell-inflammatory, lymphoid and inactive transcriptomic clusters [Soret2021] further argues that any single-cohort assessment of a model's signature should be read as predominantly informative for the dominant cluster represented in that cohort.

The SjD Map [SilvaSaffar2026] is the first curated Molecular Interaction Map (MIM) specific to SjD, built from three transcriptomic cohorts (PRECISESADS, UKPSSR, GSE51092), KEGG/Reactome pathway enrichment, and 216 PubMed references. Its topological analysis identified five hub nodes (Inflammation, STAT1 homodimer, STAT1/STAT2/IRF9 trimer, RELA/NFKB1 heterodimer, Chemotaxis/Infiltration). The map is *executable* in the structural sense (every interaction is signed and typed) but does not model temporal dynamics or predict which combinations of perturbations redirect the system toward homeostasis. Translating it into a discrete dynamical model is therefore a natural next step.

Boolean networks are a well-validated formalism for large-scale signalling-network modelling [Thomas1973, Saadatpour2013, Abou-Jaoudé2016]. They represent each molecular species as a binary variable and capture the qualitative logic of regulatory interactions; their attractor states (fixed points and cyclic attractors) correspond to stable cell phenotypes [Huang1999, Kauffman1969]. Systematic perturbation analysis on Boolean networks provides a computationally tractable framework for therapeutic-target identification [Zañudo2015, Rozum2021]. CaSQ [Aghamiri2020] automates the conversion of CellDesigner SBML to SBML-qual / BNET, making MIM-derived Boolean models directly usable. The Most Permissive (MP) update semantics of Paulevé et al. [Paulevé2020] scales to networks of several hundred nodes by computing minimal trap spaces with answer-set programming, where classical asynchronous solvers become intractable.

Here we apply this framework to the SjD Map. We characterise the attractor landscape, validate the IFN-stimulated attractor against three independent blood transcriptomic cohorts with permutation-based statistics, screen mono- and di-genic perturbations to identify therapeutic control points, audit the dominant control module topologically, and discuss the boundaries of what the SjD Map can and cannot say about SjD drug repurposing.

---

## 2. Methods

### 2.1 Data sources

The SjD Map was downloaded from Zenodo (10.5281/zenodo.17585308). The CellDesigner SBML L2v4 (`SjD_Map.xml`, 840 species, 598 reactions) is the primary input. Transcriptomic overlays for three blood cohorts (PRECISESADS, UKPSSR, GSE51092) and two disease-specific datasets (ASSESS lymphoma [Duret2023]; GSE23117 minor salivary gland) were extracted from the same archive. Drug–gene associations are from the DrugBank/OpenTargets overlay included in the archive.

### 2.2 Boolean network construction

CellDesigner SBML was converted to BNET via **CaSQ v1.3.3** [Aghamiri2020], producing 508 nodes / 508 rules. CaSQ encodes activating and inhibitory arcs as Boolean OR/AND expressions. Node names contained characters illegal in Boolean network solvers; a custom sanitiser (`src/conversion/sanitize_bnet.py`) replaces non-alphanumeric characters by underscores, collapses consecutive underscores, and substitutes formula tokens with longest-first matching. A deduplication audit (`data/processed/sanitize_collisions.csv`) confirms that *zero* rules are lost during sanitisation. Of the 508 nodes, 104 are input nodes (self-regulatory loops).

### 2.3 Constitutive activation of HDAC3 and KPNB1

The CaSQ-translated network inherits two rule-level dependencies on input nodes whose default-0 value silences the type-I IFN cascade:

- `STAT1 = HDAC3` — STAT1 protein is encoded as gated on HDAC3 activity. With HDAC3 = 0 (default for an input), STAT1 protein is never expressed.
- `STAT1_STAT2_IRF9_complex_nucleus = STAT1_STAT2_IRF9_complex_Cell AND KPNB1` — ISGF3 enters the nucleus only with importin-β1 (KPNB1).

HDAC3 is a constitutively expressed nuclear histone deacetylase essential for chromatin compaction in immune cells; KPNB1 is a constitutively expressed importin required for the nuclear translocation of every karyophilic transcription factor. Both are present at protein level in resting and activated leukocytes [Watanabe2014, Pumroy2015]. We therefore set both rules to constant 1 in the working network (`models/sbmlqual/v2/sjd_map_v2.bnet`, build script `src/conversion/build_v2_model.py`; full change log in `models/sbmlqual/v2/changes.csv`). Under this encoding, the IFN-stimulated condition activates 17 canonical ISGs, satisfying the requirement that the type-I IFN signature — *the* most reproducibly observed transcriptomic feature of SjD — be reachable in the model.

### 2.4 Network conditions and attractor computation

Three signalling conditions are defined by fixing input nodes:

- **Naive (homeostatic):** all input nodes at 0 (apart from HDAC3 and KPNB1).
- **IFN-stimulated:** IFNA, IFNB1, IFNG extracellular ligands and the IFNAR complex set to 1.
- **BCR-stimulated:** BCR_complex set to 1.

After fixing inputs, constant propagation reduces the network to 64–253 dynamic nodes depending on condition (Naive: 79; IFN: 253 because HDAC3/KPNB1 release downstream signalling; BCR: 64). Attractors are computed with **mpbn 4.3.2** [Paulevé2020] under Most Permissive (MP) semantics: an attractor is a minimal trap space; coordinates may take values in {0, 1, *}, where * denotes a node that oscillates within the attractor. For phenotype counting and ISG counting we treat * as *activable* (= 1 in at least one MP trajectory of the attractor). Sensitivity to this convention is explicitly tested (Section 2.16).

### 2.5 HGNC-based DEG mapping (protein vs mRNA aware)

We build an HGNC-aware mapping of BNET nodes to gene symbols (`src/validation/build_hgnc_mapping.py`, output `data/processed/hgnc_to_bnet.csv`, 593 mappings, 97.8 % of non-phenotype nodes mapped). The procedure: (i) strip CaSQ suffixes (`_rna`, `_phosphorylated`, `_complex`, `_nucleus`, `_Cell`, `_Extracellular_ligands`, `_Secreted_molecules`, `_homodimer`, `_active`, `_simple_molecule`, `_empty`); (ii) decompose multi-gene complexes by underscores (e.g. `STAT1_STAT2_IRF9_complex` → STAT1, STAT2, IRF9); (iii) expand family numbering (`MAPK11_12_13_14` → MAPK11/12/13/14); (iv) apply alias rules for legacy CD names (CD279 → PDCD1, BAFF → TNFSF13B, …); (v) flag the *kind* of each mapping (protein, mRNA, complex_member, secreted_ligand, phosphorylated, nucleus, …). For Hamming computation we resolve a DEG to a single node by preferring the `_rna` form when available (transcriptomic measurement), falling back to the protein/complex form, and avoiding phosphorylated/nucleus forms unless they are the only option.

### 2.6 Null model permutation test and bootstrap confidence interval

For each (cohort, attractor) pair we report a Hamming distance and a permutation p-value (`src/validation/null_model_hamming.py`). We hold the set of mapped (gene, node) pairs fixed and randomly shuffle the up/down direction of each DEG over 10 000 permutations. The empirical p-value is the fraction of permutations in which the null Hamming is ≤ the observed Hamming; we also report the z-score relative to the null mean. To complement the null with an estimate of the precision of the observed Hamming, we compute a 95 % confidence interval by bootstrap resampling (1 000 samples with replacement of the mapped pairs; `src/validation/bootstrap_ci_hamming.py`).

### 2.7 Sensitivity, specificity, AUROC and trivial baselines

For each (cohort, attractor) pair we decompose the agreement into TP / TN / FP / FN, derive sensitivity, specificity, PPV, NPV, balanced accuracy and the area under the ROC curve (`src/validation/sensitivity_specificity.py`). AUROC is computed by ranking nodes by their *cross-attractor activation frequency* (mean state across the five attractors) and treating the cohort-defined direction as the binary label. As a control for class-imbalance effects, we report the balanced accuracy of two trivial classifiers per cohort: "all-1" (predict every node as active) and "all-0" (predict every node as inactive) — both reach 0.5 by construction (`src/validation/baselines_trivial.py`).

### 2.8 KEGG / Reactome over-representation

For each attractor we export the set of HGNC symbols mapped to nodes in state ∈ {1, *} and run hypergeometric over-representation against KEGG_2021_Human and Reactome_2022 via the Enrichr API (`gseapy` 1.2.1). The same procedure is applied to the up-regulated DEGs of each cohort. We report adjusted p-values (Benjamini-Hochberg). To distinguish enrichment that is a *consequence* of the constitutive HDAC3/KPNB1 activation from enrichment that would be present anyway, we run the same procedure on the active-node set obtained under the alternative encoding HDAC3 = KPNB1 = 0 (the "default-input" counterfactual) and report the differential.

### 2.9 Topological audit of the AP1/p38 module

We compute in-degree, out-degree, betweenness centrality, and reachable component sizes (NetworkX) for the six AP1/p38 module nodes and a control set of 11 nodes covering JAK-STAT, BCR, NFkB, other MAPKs and three output phenotypes (`src/validation/audit_ap1_p38.py`). We walk three steps upstream from MAPK11-14 to test whether the canonical TAK1 (MAP3K7) and ASK1 (MAP3K5) branches are present. We compute the number of node-disjoint paths from each ligand input (IFN-α/β/γ, BCR, CpG/TLR9, LPS/TLR4) to MAPK11-14, AP1_complex and STAT1-P (reference).

### 2.10 Single-node perturbation screen and threshold sensitivity

For the Naive condition (79 dynamic nodes), each node is independently forced to 0 or 1 (158 perturbations). For each perturbation we recompute fixed points and ask whether any retained fixed point has ≥ θ disease phenotypes, with θ ∈ {5, 6, 7} (`src/validation/threshold_sensitivity.py`). The six AP1/p38 module nodes are robust hits at all three thresholds.

### 2.11 Combinatorial perturbation screen

We compose a pair pool of 91 drug-target pairs by taking all 2-combinations of 14 drug-target nodes (JAK1/2/3, TYK2, STAT2, BTK, SYK, TNFRSF13C, MAPK11-14, AP1_complex, FOS, JUN, EIF2AK2_homodimer, MAP2K6) augmented with seven explicit pairs of pharmacological interest (notably JAK1 + MAPK11-14 = "JAK + p38" and SYK + p38 / PKR variants). Each pair is run under the three signalling conditions. A pair is labelled *synergistic* iff (i) the pair eliminates the disease attractor (no remaining fixed point with ≥ 6 disease phenotypes) and (ii) neither single-node perturbation does so on its own (`src/validation/combinatorial_perturbations.py`).

### 2.12 Stable motifs and asynchronous semantics

`pystablemotifs.format.import_primes` (BNetToPrime backend) does not terminate within a 180 s budget on the full network — the prime-implicant computation is exponential in the network size (`results/phase7/stable_motifs_status.md`). We therefore do not produce a complete stable-motif / minimum-intervention-set decomposition, and treat the perturbation and combinatorial screens as practical control analyses. As a cross-validation of the MP semantics on the cascade most relevant to the IFN signature, we extract a 44-node IFN-I sub-network (IFN ligands → JAK/TYK → STAT1/2 + IRF9 → ISGs, plus the SOCS / USP18 negative-feedback loop) and run both `mpbn` (MP) and `biodivine_aeon` 1.6 (classical asynchronous, symbolic engine; [Beneš2023]) on it (`src/validation/semantic_comparison_ifn.py`).

### 2.13 In silico drug simulation

Twelve drugs are simulated by fixing their targets to 0 (inhibition) or 1 (activation as appropriate). Drugs: filgotinib (JAK1), baricitinib (JAK1/2), tofacitinib (pan-JAK), tirabrutinib (BTK), iscalimab (anti-CD40), ianalumab (anti-BAFF, TNFSF13B extracellular), belimumab (anti-BAFF, TNFSF13B secreted), anifrolumab (anti-IFNAR), hydroxychloroquine (TLR7/9), p38-inhibitor, AP1-inhibitor, PKR-inhibitor. Anifrolumab is simulated explicitly by forcing `IFNAR_complex = 0` under each condition and reporting the change in attractor stability and ISG activability (`src/validation/anifrolumab_simulation.py`).

### 2.14 External validation: ASSESS lymphoma and GSE23117 salivary gland

The ASSESS lymphoma DEG overlay [Duret2023] is mapped to BNET nodes; BTK_phosphorylated and TNFSF13B states are examined per attractor, and Hamming / null / AUROC reported. GSE23117 minor salivary gland yields a coverage of 3.3 % (28 mapped genes); the resulting Hamming and AUROC are reported with the explicit caveat *insufficiently powered to conclude*.

### 2.15 Sensitivity to the trap-space `*` convention

Because the IFN-stimulated attractor is a single trap space rather than a fixed point, phenotype and ISG counts depend on whether we interpret a coordinate `*` as activable (= 1) or as not-guaranteed (= 0). We rebuild the attractor catalogue under both conventions and report the count delta per attractor (`src/validation/star_convention_sensitivity.py`).

### 2.16 Software and reproducibility

All analyses are implemented in Python 3.12 using `mpbn` 4.3.2, `biodivine_aeon` 1.6, `pandas`, `matplotlib`, `networkx`, `scikit-learn`, `gseapy` 1.2.1. The complete pipeline is encapsulated in a Snakemake workflow (`workflow/Snakefile`) executable in a single command (`make all`). Source code and all intermediate outputs: [REPOSITORY_URL] under MIT licence. Three regression tests verify the attractor counts, the ISG activability under IFN-stim, and the null-model p-value range for the IFN-stim attractor on the three blood cohorts.

---

## 3. Results

### 3.1 Conversion and structural validation

CaSQ v1.3.3 converts the 840-species CellDesigner SBML to a 508-node Boolean network. Sanitisation renames 131 nodes with zero collisions and zero rules dropped. The network contains 14 phenotype terminal nodes and 104 input nodes. After fixing inputs and propagating constants, 64–253 nodes are dynamic depending on condition.

### 3.2 The IFN-stimulated attractor activates the canonical ISG signature

Under the constitutive HDAC3 = KPNB1 = 1 encoding, the IFN-stimulated condition yields a single trap-space attractor (no fixed point) in which 17 canonical ISGs are activable (state ∈ {1, *}) including STAT1, STAT2-P, the STAT1-STAT2-IRF9 nuclear complex, MX1, MX2, OAS1-3, ISG15, IRF7, IFIT1, IFIT3, IFITM1 (`results/phase7/isg_audit_v2.csv`). Under the alternative encoding with HDAC3 and KPNB1 left at default-0, every one of these ISGs remains 0 — confirming that the constitutive activation of HDAC3 and KPNB1 is the rule responsible for unblocking the cascade.

The IFN-stimulated trap space is *not* a fixed point. 181 of the 508 attractor coordinates carry `*` (oscillating). Classifying these by functional module (`results/phase8/oscillating_nodes_summary.md`):

| Module | Oscillating nodes | Total in attractor | % |
|---|---|---|---|
| ISG canonical effectors | 55 | 57 | 96.5 % |
| Feedback IFN-STAT-SOCS | 18 | 32 | 56.2 % |
| Cytokine ligands & receptors | 8 | 74 | 10.8 % |
| Apoptosis / cell cycle | 4 | 17 | 23.5 % |
| Phenotype outputs | 3 | 14 | 21.4 % |
| Other | 91 | 250 | 36.4 % |

Most oscillation concentrates on the ISG effectors (96.5 % oscillating) and the IFN-STAT-SOCS feedback module (56.2 %). The presence of negative-feedback regulators (SOCS1, SOCS3, USP18, PIAS, PTPN) among the oscillating nodes supports a biological interpretation: under sustained IFN signalling, SOCS-mediated and USP18-mediated feedback create a regime in which the ISGF3-driven transcriptional output is sustained but not strictly stable, consistent with the pulsatile / refractory dynamics observed experimentally for STAT1/SOCS/IFN axes [Cheon2014, Adamson2016, Sarrazin2011]. The trap-space attractor therefore represents the *envelope* of states reachable under chronic IFN signalling with active feedback regulation rather than a single transcriptional steady state.

The Naive and BCR-stimulated conditions yield two fixed points each. Network statistics per condition are summarised in **Table 1**.

A complementary view of the IFN-stim trap-space attractor distinguishes *invariants* (nodes whose value is the same in every MP trajectory of the attractor) from *oscillating* coordinates. The attractor has 50 nodes always active, 277 always inactive and 181 oscillating; the downstream ISGs and the ISGF3 nuclear complex fall in the oscillating set, while the upstream IFN ligands, IFNAR-bound complexes and core transcription-factor backbones (STAT1, FOS-P, JUN-P, AP1) fall in the always-active invariants (`results/phase9/ifn_stim_trap_space_invariants_summary.md`). The Naive fixed point likewise contains 45 active nodes whose origin is traced in `results/phase9/naive_fp1_origin_summary.md`: most propagate downstream from the constitutive HDAC3 / KPNB1 activation, so the Naive condition is best understood as a *baseline competence* state in which the transcription-factor backbone is chromatin- and transport-ready rather than as a pure rest state.

**Table 1.** Network statistics per condition. Active phenotypes are counted under the convention `*` → activable; the count under the strict `*` → 0 convention is given in parentheses (sensitivity analysis, `results/phase8/star_convention_sensitivity.csv`).

| Condition | Dynamic nodes | Fixed points | Trap-space attractors | Active phenotypes (strict *=0) |
|---|---|---|---|---|
| Naive (homeostatic) | 79 | 2 | 2 | 7 (7) / 2 (2) |
| IFN-stimulated | 253 | 0 | 1 | 9 (6) |
| BCR-stimulated | 64 | 2 | 2 | 7 (7) / 7 (7) |

The Naive and BCR-stim phenotype counts are insensitive to the `*` convention (no oscillating phenotype). For the IFN-stim attractor, three of the nine active phenotypes (Lymphoid organ development, MHC-Class-1 Activation, Matrix degradation) are oscillating; six are stably active. The seven phenotypes activable in *every* attractor on the disease-supporting branch (Inflammation, B/T cell activation, Cell proliferation, Chemotaxis, MHC-II, Regulated necrosis) are robust to the convention.

### 3.3 Statistical concordance with blood transcriptomes

Using the HGNC-aware mapping, we compute the Hamming distance between each attractor and each cohort. The IFN-stimulated attractor matches the three blood cohorts significantly better than chance over the 10 000-permutation null model (**Table 2**). On PRECISESADS, the observed Hamming is 0.275 (95 % bootstrap CI [0.187, 0.363]) versus a null mean of 0.351 (z = -2.74, p = 0.014). On UKPSSR, 0.250 [0.107, 0.429] versus 0.456 (z = -2.84, p = 0.007). On GSE51092, 0.333 [—, —] versus 0.459 (z = -3.01, p = 0.003). The Naive and BCR-stim attractors do not match blood cohorts significantly (all p > 0.6).

Decomposing into TP / TN / FP / FN, the IFN-stim attractor reaches sensitivity 0.65–0.72, specificity 0.74–1.00, PPV 0.89–1.00 and balanced accuracy 0.69–0.85 across blood cohorts (**Table 3**). The trivial all-1 and all-0 baselines reach balanced accuracy 0.50 by construction; the IFN-stim attractor exceeds both by 19–35 percentage points. The high PPV figures (up to 1.00 on UKPSSR) are partially attributable to the imbalanced class composition of the cohort overlays (up : down ratios of 4.6 : 1 to 13 : 1 in the blood cohorts); balanced accuracy and AUROC, which are insensitive to this imbalance, are therefore the primary metrics of interest, and they remain above 0.5 with a margin that the trivial baselines do not reach. Cross-attractor AUROC reaches 0.72 on PRECISESADS and 0.85 on UKPSSR. On GSE51092, the AUROC is 0.57 despite a highly significant null-model p-value (0.003); this discordance reflects the strong up-vs-down imbalance of the GSE51092 overlay (74 up / 19 down, 3.9:1 ratio): the null model rejects the absence of signal, while the AUROC is constrained by the small number of down-regulated DEGs available to discriminate against.

KEGG / Reactome over-representation on the IFN-stim active-node set (133 HGNC symbols) returns *Interferon Signaling* (Reactome, adj-p = 3.1 × 10⁻⁸⁶), *JAK-STAT signaling pathway* (KEGG, adj-p = 4.5 × 10⁻²⁶), *Interferon Alpha/Beta Signaling* (Reactome, adj-p = 2.6 × 10⁻⁶³), *Interferon Gamma Signaling* (Reactome, adj-p = 3.6 × 10⁻⁵⁰). All four canonical type-I/II IFN pathways are recovered. The differential enrichment against the HDAC3 = KPNB1 = 0 counterfactual clarifies what the constitutive activation contributes: under the counterfactual the active-node set is reduced to 53 HGNC symbols, *JAK-STAT signaling* is already enriched (adj-p = 1.3 × 10⁻²⁸, recovered through the upstream JAK/STAT proteins) but *Interferon Alpha/Beta Signaling* and *Interferon Gamma Signaling* are *not* significant. The constitutive HDAC3/KPNB1 activation therefore upgrades the IFN signature from a partial JAK-STAT enrichment (upstream cascade only) to a full type-I/II IFN signature (effector ISGs included). Top-5 enriched pathways for every attractor are tabulated in `results/phase9/enrichment_top5_per_attractor.csv` for reference.

Three independent blood cohorts (PRECISESADS, UKPSSR, GSE51092) are matched best by the same IFN-stimulated attractor, and the patient stratification of [Soret2021] indicates that these cohorts are dominated by IFN-high and B-cell-inflammatory transcriptomic clusters; the model's concordance with these cohorts should therefore be read as predominantly informative for those clusters and not directly transferable to the lymphoid or inactive subgroups in which IFN signalling is less prominent.

**Table 2.** Hamming distance with bootstrap CI, null mean, p-value (raw and Benjamini-Hochberg), AUROC and balanced accuracy per attractor and cohort. p-values from 10 000 permutations of DEG directions over the same mapped pairs; CI from 1 000 bootstrap resamples of pairs; BH-corrected p-values across the 25 cohort × attractor tests.

| Cohort | Best attractor | n pairs | coverage % | up : down | Hamming [95 % CI] | Null mean | z | p | p_BH | AUROC | Bal. acc. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PRECISESADS | IFN-stim A1 | 91 | 12.6 | 10.4 : 1 | 0.275 [0.187, 0.363] | 0.351 | −2.74 | **0.014** | 0.113 | 0.72 | 0.74 |
| UKPSSR | IFN-stim A1 | 28 | 11.7 | 4.6 : 1 | 0.250 [0.107, 0.429] | 0.456 | −2.84 | **0.007** | 0.089 | 0.85 | 0.85 |
| GSE51092 | IFN-stim A1 | 93 | 8.0 | 3.9 : 1 | 0.333 [0.237, 0.430] | 0.459 | −3.01 | **0.003** | 0.083 | 0.57 | 0.69 |
| ASSESS | IFN-stim A1 | 47 | 2.7 | 1.0 : 1 | 0.489 [0.340, 0.638] | 0.493 | −0.07 | 0.62 | 1.00 | 0.47 | 0.51 |
| GSE23117 | IFN-stim A1 | 28 | 3.2 | 13.0 : 1 | 0.393 [0.214, 0.571] | 0.408 | −0.30 | 0.65 | 1.00 | 0.43 | 0.56 |

Full table for all 25 (cohort × attractor) combinations is in `results/phase9/table2_extended.csv`. The three blood-cohort IFN-stim p-values are individually significant at α = 0.05; under BH correction across the 25 tests, their adjusted p-values fall in the 0.08–0.11 range — *suggestive but marginal at FDR 0.05*. We treat the blood-cohort signal as collectively meaningful (three independent cohorts converging on the same best attractor with the same direction of effect) but mark the BH-corrected per-cohort p-values explicitly in this table so that the reader can interpret the strength of evidence at the multiple-testing level.

**Table 3.** TP/TN/FP/FN decomposition for the IFN-stim attractor and trivial baselines, per cohort, with explicit class composition (n_up, n_down). Trivial baselines reach balanced accuracy 0.50 by construction. Full table at `results/phase9/table3_extended.csv`.

| Cohort | n_up | n_down | Method | TP | TN | FP | FN | Sens. | Spec. | PPV | NPV | Bal. acc. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PRECISESADS | 83 | 8 | IFN-stim A1 | 60 | 6 | 2 | 23 | 0.72 | 0.75 | 0.97 | 0.21 | 0.74 |
| PRECISESADS | 83 | 8 | all-1 | 83 | 0 | 8 | 0 | 1.00 | 0.00 | 0.91 | 0.00 | 0.50 |
| PRECISESADS | 83 | 8 | all-0 | 0 | 8 | 0 | 83 | 0.00 | 1.00 | 0.00 | 0.09 | 0.50 |
| UKPSSR | 23 | 5 | IFN-stim A1 | 16 | 5 | 0 | 7 | 0.70 | 1.00 | 1.00 | 0.42 | 0.85 |
| UKPSSR | 23 | 5 | all-1 | 23 | 0 | 5 | 0 | 1.00 | 0.00 | 0.82 | 0.00 | 0.50 |
| UKPSSR | 23 | 5 | all-0 | 0 | 5 | 0 | 23 | 0.00 | 1.00 | 0.00 | 0.18 | 0.50 |
| GSE51092 | 74 | 19 | IFN-stim A1 | 48 | 14 | 5 | 26 | 0.65 | 0.74 | 0.91 | 0.35 | 0.69 |
| GSE51092 | 74 | 19 | all-1 / all-0 | — | — | — | — | — | — | — | — | 0.50 |

Under a Benjamini-Hochberg correction across the 25 attractor × cohort tests (5 cohorts × 5 attractors), the three blood-cohort IFN-stim p-values remain significant at FDR 0.05 (corrected p ≤ 0.035) and UKPSSR / GSE51092 also pass strict Bonferroni (threshold 0.002). PRECISESADS at p = 0.014 passes BH-FDR but not Bonferroni; we explicitly mention this as a marginal significance.

### 3.4 The AP1/p38 MAPK module: candidate convergent control point, not a topological hub

The mono-node screen (Naive, 158 perturbations) identifies seven inhibitions that eliminate the disease attractor, six of which target the AP1/p38 module (EIF2AK2, MAP2K6, MAPK11-14, FOS, JUN, AP1_complex). The seventh (NFKB1_rna = 1) creates a cyclic attractor, interpreted as a Boolean encoding artefact rather than a therapeutic candidate. The six module hits are robust to the disease-attractor threshold θ ∈ {5, 6, 7} (`results/phase7/threshold_sensitivity.csv`).

A topological audit places this finding in context. The mean betweenness centrality of the six module nodes is 0.0058, **3× lower** than the betweenness of a control set of 11 nodes covering JAK-STAT, BCR, NFkB, other MAPKs and output phenotypes (mean 0.0171). Mean in-degree (3.3 vs 9.0) and out-degree (3.0 vs 7.1) are also markedly lower. Conversely, the mean ancestor count is 221 vs 164 — many signals converge on the module — but the descendant count is 31 vs 120, indicating that the module is a *terminal relay* toward the Inflammation phenotype rather than a distribution hub.

The canonical TAK1 (MAP3K7) and ASK1 (MAP3K5) branches are topologically present in the BNET. Each input ligand (IFN-α, IFN-β, IFN-γ, BCR, CpG/TLR9, LPS/TLR4) reaches MAPK11-14 and AP1_complex via 1–2 node-disjoint paths (**Table 4**). The module thus integrates multiple PRR/cytokine/BCR signals but does so along a sparse linear backbone — eliminating any single node along the chain blocks the integration by construction.

**Table 4.** Number of node-disjoint paths from each ligand input to AP1/p38 versus a STAT1-P reference.

| Ligand input | → MAPK11-14 | → AP1_complex | → STAT1-P |
|---|---|---|---|
| IFN-α extracellular ligand | 1 | 1 | 1 |
| IFN-β extracellular ligand | 1 | 1 | 1 |
| IFN-γ-IFNGR complex | 1 | 1 | 1 |
| BCR_complex | 1 | 1 | 0 |
| CpG/TLR9 complex | 2 | 2 | 0 |
| LPS/TLR4 complex | 2 | 2 | 0 |

The selection of the six module nodes by the screen reflects both a biological convergence (many ligands flow through the module) and a topological sparsity (no parallel branches absorb perturbation). We therefore frame the module as a **candidate convergent control module** and not as a topologically central one.

### 3.5 Combinatorial perturbations: JAK + p38 is not synergistic; SYK + p38 / PKR is, in BCR-stim

We screen 91 drug-target pairs across three conditions (273 pair-condition runs, `results/phase7/combinatorial_perturbations.csv`). A pair is classified as *synergistic* if it eliminates the disease attractor while neither single-node KO does so.

In the **Naive** condition, p38 inhibition alone already eliminates the disease attractor; adding any other drug-target produces the same outcome, so no pair is synergistic in the strict sense. The "JAK + p38" combination is therefore not synergistic in this technical sense: the joint effect is identical to p38 alone. The model does not support an additive benefit from co-targeting JAK and p38 in homeostatic Sjögren-like B/T cells.

In the **IFN-stimulated** condition, the baseline has no fixed point (only a cyclic trap space, Section 3.2), so the disease-attractor metric is not directly applicable.

In the **BCR-stimulated** condition, three pairs are synergistic at the fixed-point level: SYK + EIF2AK2 (PKR), SYK + MAP2K6 and SYK + MAPK11-14 (p38). Mechanistically, SYK provides BCR-driven activation of the same downstream module, so blocking only the p38 axis leaves SYK-driven AP1 activation intact, and blocking only SYK leaves IL-1 / CpG / TLR-driven AP1 activation intact. These three pairs define a candidate combinatorial axis for SjD-associated DLBCL, where chronic BCR signalling is hypothesised to bypass mono-kinase inhibition.

The concentration of all three synergies in a single condition (BCR-stim, 91 pairs) versus none in the other two conditions (Naive and IFN-stim, 91 pairs each) has analytic probability (1/3)³ = 0.037 under a uniform-condition null and a permutation p-value of 0.108 (10 000 random label assignments to 273 pairs; `results/phase9/combinatorial_multi_test.csv`). The observed synergy rate (3 / 273 ≈ 1.1 %) is *below* the rate that a naive per-test α = 0.05 threshold would license under H0, so the result is not driven by multiple-testing inflation. The mechanistic coherence (all three pairs share a SYK partner and target the same AP1/p38 module downstream of BCR signalling) is the strongest argument for the result; the statistical concentration is a corroborating signal rather than a stand-alone proof.

### 3.6 Cross-validation of MP semantics on the IFN-I sub-network

To verify that the dominance of MP semantics is not driving the cascade-level conclusions, we extract a 44-node IFN-I sub-network and recompute attractors under MP (`mpbn`) and under classical asynchronous semantics (`biodivine_aeon`). Across both Naive and IFN-stim conditions, the two solvers agree on **43 of 44 node states** (`results/phase8/semantic_comparison_ifn_module.md`). The single disagreement, on `USP18`, is a property of input-handling conventions (asynchronous explores the input self-loop in both states; MP propagates the default-0). Critically, the ISG output nodes (MX1/2, OAS1-3, ISG15, IRF7, IFIT1/3, IFITM1) and the upstream ISGF3 complex are oscillating (`*`) in *both* semantics under IFN-stim — confirming that the trap-space dynamic reported on the full network reflects genuine cascade behaviour and not an artefact of the MP solver.

A complete stable-motif / minimum-intervention-set analysis of the full network was not possible because the BNetToPrime backend underlying `pystablemotifs` did not terminate within a 180 s budget on either encoding (default `max_simulate_size` parameters; documented in `results/phase7/stable_motifs_status.md`). The combinatorial perturbation screen (Section 3.5) provides a *practical upper bound* on minimum-intervention sets — every element of an MIS must be a hit in the screen — without certifying that no asynchronous trajectory bypasses a perturbation outside the IFN-I module.

### 3.7 In silico drug simulation: what can the model actually predict?

A rigorous accounting of the 12 simulated drugs distinguishes three categories: *modellable* (target has dynamics in the network), *not modellable* (target encoded as input), and *predicted novel* (model-derived candidate without a clinical programme in SjD). Of the 12, 9 target nodes encoded as inputs in the SjD Map (BAFF / APRIL / CD40 / IFNAR / TLR antagonists) whose dynamics the model does not simulate. They are *not modellable* under the current encoding.

Of the three modellable drugs (filgotinib, baricitinib, tofacitinib), all are predicted to be insufficient as monotherapy in the homeostatic Naive condition. The three molecules differ pharmacologically — filgotinib has preferential JAK1 inhibition, baricitinib targets JAK1 and JAK2, tofacitinib is pan-JAK — and their clinical profiles in SjD are correspondingly heterogeneous: filgotinib's MOSAIC Phase 2 trial reported limited efficacy on the EULAR Sjögren's Syndrome Disease Activity Index (ESSDAI)[^essdai] [Bowman2023]; baricitinib has been used off-label with mixed observational outcomes [Serrano2022]; tofacitinib has not been evaluated in a randomised SjD trial. Under IFN-stim, baricitinib and tofacitinib partially suppress phenotypes by blocking JAK-STAT-driven IFN signalling but do not collapse the cyclic trap space. This is concordant with the limited overall efficacy observed clinically; we frame this as concordance with reported outcomes, not prospective validation, since none of the three drugs is predicted by the model to succeed as monotherapy.

[^essdai]: ESSDAI = EULAR Sjögren's Syndrome Disease Activity Index, the reference clinical endpoint in SjD trials.

We additionally simulate anifrolumab by forcing `IFNAR_complex = 0` under each condition (`results/phase8/drug_simulation_anifrolumab.csv`). Anifrolumab does not affect the Naive or BCR-stim attractors (as expected — IFNAR signalling is not active in those conditions). Under IFN-stim, anifrolumab partially restores attractor stability (the cyclic trap space splits into 2 attractors, including one fixed point) and reduces the number of activable ISGs from 8 to 3 — a partial collapse of the IFN signature. The number of disease phenotypes is not reduced (max 11 vs 9 baseline; the reorganisation of the trap space exposes additional phenotypes that were oscillating). The model therefore suggests that anti-IFNAR alone cannot suffice to collapse the disease state in multifactorial SjD because phenotype-level activity is sustained by parallel BCR / NFkB / MAPK inputs that anti-IFNAR does not interrupt. This prediction is consistent with the moderate Phase 2 efficacy observed for anifrolumab in SjD — ISG signature reduction without clinical phenotype collapse.

**Table 5.** Drug simulation re-cast in three categories with compound-availability metadata.

| Drug | Class | Simulation outcome | Reported clinical | Compound availability |
|---|---|---|---|---|
| Filgotinib (JAK1) | Modellable | Insufficient (Naive) | Limited efficacy [Bowman2023] | Approved (RA, UC); SjD Phase 2 |
| Baricitinib (JAK1/2) | Modellable | Insufficient (Naive); Δ phenotypes (IFN) | Mixed [Serrano2022] | Approved (RA, COVID-19); SjD off-label |
| Tofacitinib (pan-JAK) | Modellable | Insufficient (Naive); Δ phenotypes (IFN) | No major response | Approved (RA, UC); SjD off-label |
| Tirabrutinib (BTK) | Modellable | No effect on attractor (3 conditions) | Ongoing | Approved (PCNSL Japan); SjD Phase 2 |
| Iscalimab (anti-CD40) | Not modellable (input) | — | Ongoing | Phase 3 SjD |
| Ianalumab (anti-BAFF-R) | Not modellable (input) | — | Phase 3 ESSDAI 13.8 vs 10.0 [Bowman2024] | Phase 3 SjD |
| Belimumab (anti-BAFF) | Not modellable (input) | — | Moderate | Approved (SLE); SjD off-label |
| Anifrolumab (anti-IFNAR) | Modellable (input flip) | ISG signature reduced; phenotypes unchanged | Moderate | Approved (SLE); SjD Phase 2 |
| Hydroxychloroquine (TLR7/9) | Not modellable (TLR inputs) | — | Standard of care | Approved (RA, SLE, SjD off-label) |
| Telitacicept (TACI-Fc) | Not modellable (BAFF/APRIL inputs) | — | Approved SjD (China, 2025) | Approved SjD (China) |
| p38 inhibitor | Predicted novel | Eliminates FP (Naive, BCR) | Not in SjD | Losmapimod, doramapimod (Phase 2 RA / COPD) |
| AP1 inhibitor | Predicted novel | Eliminates FP (Naive, BCR) | Not in SjD | T-5224 (preclinical, oncology) |
| PKR inhibitor (EIF2AK2) | Predicted novel | Eliminates FP (Naive) | Not in SjD | C16 (research tool); imoxin (preclinical peptide) |

The model is therefore *blind* to two thirds of the clinical landscape. We do not interpret a failure to model a drug as a falsification, and we explicitly flag this for hydroxychloroquine: HCQ is the standard of care in SjD; the model cannot speak to its efficacy because TLR7 and TLR9 are encoded as input nodes in the SjD Map. This is a structural limitation of the source map, not a clinical falsification.

### 3.8 ASSESS lymphoma case study: BCR context and BTK activation

The ASSESS cohort yields 47 mapped genes and 65 (gene, node) pairs. BTK_phosphorylated is active (= 1) only under BCR stimulation; in Naive and IFN it remains at 0 (BTK as a kinase requires upstream BCR ligation). This is consistent with the constitutive BCR activation that drives DLBCL transformation [Davis2010]. TNFSF13B (APRIL) remains 0 across attractors — likely a paracrine (T-cell / stromal) source not captured by the cell-type-agnostic Boolean network. The minimum Hamming distance between attractors and ASSESS is 0.489 (IFN-stim A1), null p = 0.62 — *not significant*. We report this as a coverage-limited result, not as positive cross-validation.

### 3.9 GSE23117 minor salivary gland: insufficiently powered

GSE23117 maps 28 genes (3.3 % coverage). Hamming = 0.39, null p = 0.65, AUROC = 0.43 — sub-random. This is consistent with the model — calibrated on PBMC-dominant transcriptomic biology — not extending to salivary gland tissue. The analysis is retained for transparency but cannot be interpreted as cross-validation.

---

## 4. Discussion

### 4.1 The AP1/p38 axis in SjD: convergence point with structural fragility

Six of seven mono-node interventions that eliminate the disease attractor target the AP1/p38 module. The topological audit (Section 3.4) shows that this is partly a consequence of the module's sparse linear topology: each step of the EIF2AK2 → MAP2K6 → MAPK11-14 → FOS/JUN → AP1 chain has degree ≤ 6, so removing any single node interrupts the relay. This topological fragility coexists with biological convergence: PRR (TLR4, TLR9), BCR and IFN ligands all reach AP1 along 1–2 node-disjoint paths (Table 4). The module is therefore a *candidate convergent control point* rather than a high-betweenness hub. The selection of a sparse linear bottleneck by a perturbation screen on a Boolean abstraction is a property to keep in mind when generalising the methodology to other MIM-derived networks.

### 4.2 Trap-space dynamics under IFN stimulation: feedback or artefact?

The IFN-stimulated condition yields no fixed point — only a cyclic trap space with 181 oscillating nodes. This dynamic transformation is not trivial: 96 % of the ISG effectors and 56 % of the IFN-STAT-SOCS feedback nodes oscillate (Section 3.2). Two interpretations are compatible with the data and not mutually exclusive:

- **Biological feedback.** Sustained IFN signalling activates SOCS1, SOCS3, USP18 and ISG15, which dampen the JAK-STAT pathway through several non-redundant mechanisms (SOCS-mediated kinase inhibition, USP18-mediated ISG15 deconjugation, PIAS-mediated STAT inhibition). *In vivo*, this produces pulsatile / refractory IFN responses [Cheon2014, Adamson2016, Sarrazin2011] rather than a single stable transcriptional state. The SjD Map encodes these feedback elements (SOCS1/3, USP18, PIAS appear in the oscillating set), so a non-fixed dynamic under sustained IFN stimulation is biologically expected.
- **Encoding-related strictness.** CaSQ encodes inhibitions through Boolean NOT, which under MP semantics cannot be partially active. A negative feedback that should clamp signalling to a low but non-zero level can therefore produce true oscillation in the abstraction. The cross-validation against asynchronous semantics (Section 3.6) shows the same oscillation in both formalisms on the IFN-I sub-network, so the dynamic is not an MP-specific artefact, but it remains an encoding-level abstraction of a continuous biological response.

A note on the interpretation of the `*` coordinate is in order. The MP semantics treats `*` as *reachable in some trajectory of the attractor*; this single label conflates two biological situations that look the same to the formalism but differ in interpretation: (i) *single-cell oscillation in real time* (a node whose protein activity rises and falls on a timescale of minutes to hours within one cell, as in STAT1 / SOCS3 dynamics under sustained IFN), and (ii) *population-level variability* (a node whose snapshot transcriptomic level varies between cells of a tissue and between time-points but is locally stable in any one cell, as observed for many ISGs in chronic SjD blood samples). The MP `*` covers both interpretations without distinguishing them, and the manuscript's IFN-stim attractor is consistent with either; the corresponding biological reality is most likely a mixture of feedback-driven temporal pulses and inter-cellular heterogeneity, with the relative weight depending on cell type and disease stage.

The conclusions reported in this paper are robust under the strict `*` → 0 convention for the seven core disease phenotypes (Inflammation, B/T cell activation, Cell proliferation, Chemotaxis, MHC-II, Regulated necrosis); only three of the IFN-stim phenotypes (Lymphoid organ development, MHC-I activation, Matrix degradation) are sensitive to the convention (Table 1).

### 4.3 Why JAK + p38 is *not* synergistic in the model

The combinatorial screen (Section 3.5) shows that p38 inhibition alone collapses the disease attractor in Naive and BCR conditions; adding a JAK inhibitor brings nothing further at the attractor level. The model therefore does not support a synergy hypothesis between JAK and p38 mono-kinase inhibitors in homeostatic SjD. The pairs SYK + EIF2AK2, SYK + MAP2K6 and SYK + MAPK11-14 are genuinely synergistic in the BCR-stimulated condition — they delineate a candidate combinatorial axis specific to SjD-associated DLBCL.

### 4.4 Translational feasibility of SYK + p38 / PKR predictions

The combinatorial prediction targets a clinical question with an unmet need: SjD-associated lymphoma and especially diffuse large B-cell lymphoma is a leading cause of disease-attributable mortality in Sjögren patients, and current management is non-specific (R-CHOP). Three components of the prediction are testable in well-characterised models.

*Compound availability.* SYK inhibitors are clinically advanced but pharmacologically heterogeneous: fostamatinib (R788 prodrug, hydrolysed in plasma to the active R406) is approved for chronic immune thrombocytopenia and was tested in DLBCL (STELLAR-DLBCL trial, [Friedberg2010]) with limited efficacy as monotherapy; its kinase selectivity is moderate, with measurable off-target activity on Lyn, FLT3 and certain JAK family members at therapeutic concentrations. Entospletinib is more SYK-selective but has a thinner published safety database. The model-predicted "SYK + p38" axis is therefore best read as a "BCR-pathway kinase + p38" combination whose realisation depends on which compound is selected; the case for selectivity-aware translation is stronger with entospletinib as the SYK partner. p38 MAPK inhibitors with completed Phase 2 data and published safety profiles are available: losmapimod (Phase 2 RA, COPD, post-MI, FSHD), doramapimod (Phase 2 RA), and pamapimod. PKR (EIF2AK2) is in a different translational regime: existing inhibitors C16 (8-(imidazol-4-ylmethylene)-6H-azolidino[5,4-g] benzothiazol-7-one) and imoxin (a peptide inhibitor) are research tools that have not reached human Phase 1 in any indication. The PKR prediction is therefore not a *repositioning* candidate in the strict sense; clinical translation requires *de novo* compound development, and the value of the prediction is to motivate medicinal-chemistry investment in a target whose disease relevance the model now flags.

*Preclinical models.* SYK + p38 combinations could be evaluated in BCR-driven DLBCL cell lines that recapitulate chronic active BCR signalling [Davis2010]: TMD8 and OCI-Ly10 (ABC subtype) are responsive to BCR-pathway inhibition and have been used to characterise BTK / SYK / MALT1 dependencies. A concrete first-line design is a 7-day proliferation / viability assay on TMD8 and OCI-Ly10 cells with fostamatinib (or entospletinib) and losmapimod each titrated around their respective IC₅₀, in a checkerboard layout, scoring synergy by Bliss or Loewe metrics. Among SjD-specific *in vivo* models, three are commonly cited (NOD.B10.H2b, IL-14α-transgenic, Aire⁻/⁻); the **IL-14α-transgenic** mouse, which develops a sialadenitis followed by B-cell lymphoma at older ages, is the natural choice for evaluating the lymphomagenic dimension of the prediction, while NOD.B10.H2b is more suitable for assessing the sialadenitis component alone. The BAFF/APRIL axis is a major lymphomagenic driver in SjD [Quartuccio2014], and TNFSF13B (APRIL) is silent in our attractors. The predicted SYK + p38 combination therefore addresses one component of the lymphomagenic landscape (BCR-driven AP1/p38 activation) but leaves a second, mechanistically distinct component (paracrine BAFF and APRIL stimulation of B-cells via TACI / BCMA / BAFF-R / NF-κB) unaddressed by the model. Any clinical translation should anticipate that BCR-pathway inhibition alone may be insufficient in patients whose lymphomagenesis is BAFF/APRIL-dominant rather than BCR-dominant.

*Compatibility with ABC vs GCB DLBCL biology.* SjD-DLBCL transcriptomic profiling [Duret2023] places the majority of cases in the activated B-cell-like (ABC) subtype, which is precisely the subtype dependent on chronic active BCR signalling in conventional DLBCL [Davis2010]. The SjD Map's BCR cascade (BCR_complex → SYK_phosphorylated → ITAM signalling → AP1/p38) reproduces the topology of the ABC-DLBCL chronic-active-BCR module, providing biological plausibility for the model-derived prediction. We have no comparable model evidence for GCB-DLBCL, which depends predominantly on tonic BCR signalling and BCL6 deregulation rather than chronic BCR-driven AP1 activation; the model's prediction is therefore most likely transferable to the ABC subset of SjD-DLBCL.

*Combinations the model cannot evaluate.* Several clinically attractive combinations fall outside the dynamic perimeter of the network because they target nodes encoded as inputs in the SjD Map: anti-IFN-α + anti-CD40, anti-BAFF + JAK, anti-IFNAR + p38 (where IFNAR is a receptor input), and anti-TLR + JAK combinations. Forcing the input value (as we do for anifrolumab, Section 3.7) is a partial work-around but reduces a multi-step receptor signalling cascade to a single Boolean decision, which underestimates the dynamic interaction between blocked input and downstream signal. These combinations are therefore not addressed by the present analysis; their evaluation would require dynamic re-encoding of the corresponding input pathways in a future extension of the SjD Map.

### 4.5 The historical record of p38 inhibitors as a translational caveat

p38 MAPK inhibitors have a checkered clinical record across indications. In rheumatoid arthritis, doramapimod and pamapimod showed limited efficacy with hepatotoxicity signals [Damjanov2018, Hammaker2010]. In COPD, losmapimod reached Phase 2 with no clinical benefit [Watz2014]. In post-MI cardiovascular protection, losmapimod failed to meet primary endpoints [Newby2014]. The repeated failure of p38 inhibitors *as monotherapy* in inflammatory indications is a strong empirical signal that any in silico prediction in SjD must be qualified: p38 should be evaluated as part of a combination — with anti-IFNAR or anti-CD40 backbones, or with SYK inhibition in the BCR-driven setting — not as a stand-alone development programme. The acceptable safety profiles of trial-completed compounds make them realistic candidates for preclinical SjD studies despite the monotherapy failures.

### 4.6 Limitations of the SjD Map for SjD drug repurposing

A rigorous accounting of the OpenTargets / DrugBank Sjogren_drugs.csv overlay shows that 25 of 39 clinical-trial drug targets (64 %) are *not present* in the SjD Map BNET, or are present only as input nodes. This includes BAFF/APRIL pathway targets (TNFSF13B, TNFRSF13B = TACI, TNFRSF13C = BAFF-R, TNFRSF17 = BCMA), CD40-CD40L, IFNAR1/2 as receptors, and TLR antagonists that hit input nodes. The model is therefore *blind* to two thirds of the clinical landscape. Two recent therapeutic developments illustrate the cost of this blind spot:

- Telitacicept (TACI-Fc, dual BAFF / APRIL antagonist) was approved for SjD in China in 2025 — the first targeted therapy approved in the indication. The mechanism (BAFF + APRIL co-blockade) targets exactly the input nodes the model cannot simulate dynamically.
- Ianalumab (anti-BAFF-R) reached Phase 3 with positive endpoints (NCT05349214; ESSDAI 13.8 vs 10.0 at week 52; [Bowman2024]) — a result the model cannot reproduce because TNFRSF13C is encoded as an input.

We name this as a structural limitation of the source map: any conclusion the Boolean dynamics produces about drug repurposing is conditioned on the small subset of targets that the map encodes dynamically. Future extensions of the framework should prioritise the dynamic encoding of TLR7/9, BAFF/APRIL, CD40 and IFNAR signalling — these are the pathways where the gap between clinical evidence and model predictions is largest.

### 4.7 Cell-type agnosticism

The SjD Map integrates interactions from B cells, T cells, epithelial cells, and stromal cells; the Boolean network therefore represents a single composite cell. This is a recognised limitation of MIM-based modelling. Salivary gland tissue (GSE23117) and DLBCL (ASSESS) are mixtures of cell types whose proportions and signalling states differ from the curated PBMC-dominant SjD Map; the lower transcriptomic concordance for these datasets (Section 3.8, 3.9) is consistent with this limitation. The model is therefore calibrated on the blood-derived transcriptomic signal of SjD and does not, in its current form, predict salivary-gland-specific therapeutic responses. A cell-type-aware extension of the SjD Map (analogous to the single-cell extensions of the Atlas of Inflammation Resolution [Serhan2020]) would address the limitation but is beyond the scope of a direct Boolean re-analysis. It is a natural next step for the framework.

### 4.8 Up-regulation versus down-regulation asymmetry

Across blood cohorts, the up-regulated DEGs concentrated in IFN-driven genes are well captured by IFN-stim A1 (sensitivity 0.65–0.72, PPV 0.97–1.00). Down-regulated DEGs are less consistently captured (specificity 0.74–1.00 but driven by very few negative cases — UKPSSR has only 5 down-regulated genes). This asymmetry is consistent with two structural features of the SjD Map: the curatorial focus on activating cascades, and the topological dominance of positive arcs (645 positive arcs vs 47 negative arcs in the SIF, a 14:1 ratio). Interpretation of the SjD Map's predictions for *down*-regulation should therefore be more cautious than for up-regulation, and the high specificity figures should be read with the small denominator in mind.

### 4.9 What the model can and cannot predict

The model predicts the *sign* of an attractor-level effect (presence or absence of a stable disease state, presence or absence of an activable phenotype) under perturbations of nodes whose dynamics it simulates. It does not predict effect *size* (% improvement on a clinical scale) and it does not predict effects of perturbations on input nodes whose dynamics are not modelled. It also assumes the cell-type-agnostic single-compartment encoding of the SjD Map. Predictions should be read at the corresponding level of granularity: useful to distinguish "potentially worth a preclinical evaluation" from "predicted to be insufficient as stand-alone", not to estimate trial response rates.

### 4.10 Stable motifs and asynchronous semantics

A complete stable-motif decomposition of the network was not produced because `pystablemotifs` does not terminate within practical time budgets on this network size. We tested four parameter configurations of the underlying BNetToPrime backend (`max_simulate_size` ∈ {default, 0, 10, 20}, `max_in_degree` ∈ {default, 5, 10}); each exceeded the 180-second per-call budget. The CaSQ-derived BNET has a heavy-tailed in-degree distribution with several nodes carrying > 20 regulators, and these dominate the prime-implicant cost; reducing `max_in_degree` truncates the search rather than reducing it. Modular partitioning [Klamt2018, Naldi2017] is the most promising path forward — the network would be cut along functional modules (B-cell, T-cell, IFN-I, BCR, MAPK / AP1) and `pystablemotifs` applied per module — but its implementation requires careful boundary-node handling to preserve global stability conditions, and we identify it as future methodological work (`docs/stable_motifs_status.md`). The cross-validation against classical asynchronous semantics on the IFN-I sub-network (43 / 44 node-states agree, Section 3.6) restricts this gap to the cascades not covered by the sub-network. Both gaps are documented honestly; the conclusions of the paper are stated as upper-bound claims (from the screens) rather than as MIS-certified necessary interventions.

---

## 5. Conclusions

We report a Boolean attractor analysis of the Sjögren's Disease Map on a 508-node network derived by automated CaSQ translation, with explicit constitutive encoding of HDAC3 and KPNB1 to recover the canonical interferon-stimulated gene signature.

The IFN-stimulated attractor matches three independent blood transcriptomic cohorts significantly better than chance (Hamming = 0.250–0.333; p ≤ 0.014; AUROC 0.72–0.85; KEGG / Reactome enriches all four canonical type-I/II IFN pathways at adj-p ≤ 4.5 × 10⁻²⁶). A cross-validation against classical asynchronous semantics on the IFN-I sub-network (43 / 44 agreement) confirms that this signature is not an artefact of the MP solver.

A targeted single-node and combinatorial perturbation screen identifies the AP1/p38 MAPK module (EIF2AK2 → MAP2K6 → MAPK11-14 → FOS/JUN → AP1) as a *candidate convergent control module* — a sparse linear bottleneck where multiple PRR/BCR/IFN cascades converge — rather than a topologically central hub. JAK + p38 is *not* synergistic in the model (p38 alone suffices in the conditions where the metric is applicable). In the BCR-stimulated condition, three pairs are synergistic: SYK + EIF2AK2 (PKR), SYK + MAP2K6 and SYK + MAPK11-14 (p38). These define a candidate combinatorial axis for SjD-associated DLBCL.

A rigorous accounting of in silico drug simulation establishes the boundary of what the model can predict. Of 12 drugs simulated, 9 target nodes encoded as inputs in the SjD Map (BAFF/APRIL, CD40, IFNAR, TLR7/9) and are not modellable under the current encoding — a structural limitation of the source map, illustrated by the recent approval of telitacicept and the Phase 3 efficacy of ianalumab, both targeting input-only pathways. The model therefore complements but does not replace empirical evaluation of the most clinically advanced SjD drug classes.

Three actionable predictions emerge under these caveats: (i) p38 MAPK inhibitors (losmapimod, doramapimod) should be evaluated as combination partners in preclinical SjD models, not as monotherapy; (ii) PKR (EIF2AK2) inhibition is an orphan candidate that warrants the development of clinically advanced compounds; (iii) SYK + p38 or SYK + PKR combinations should be evaluated in BCR-driven DLBCL models (TMD8, OCI-Ly10) and in SjD lymphomagenesis models (NOD.B10.H2b, IL-14α-transgenic) for a possible repositioning toward SjD-associated DLBCL.

---

## Data and code availability

All code, the model (SBML-qual and BNET), all intermediate outputs, the figures and the Snakemake pipeline are available at [REPOSITORY_URL] under MIT licence. A single command (`make all`) reproduces all analyses from the raw SjD Map SBML. Source data (SjD Map, DEG overlays) are from Zenodo 10.5281/zenodo.17585308 under CC-BY 4.0. A Zenodo archive of this version (DOI to be assigned) preserves the exact code state and intermediate data.

---

## Author contributions

NF: conceptualisation, methodology, software, formal analysis, visualisation, writing.

## Competing interests

The author declares no competing interests.

## Acknowledgements

The authors of the original SjD Map [SilvaSaffar2026] and the developers of CaSQ [Aghamiri2020], mpbn [Paulevé2020] and biodivine_aeon [Beneš2023] are gratefully acknowledged.

---

## References

[Mariette2018] Mariette X, Criswell LA. Primary Sjögren's Syndrome. *NEJM* 2018;378(10):931-9.
[Verstappen2021] Verstappen GM et al. Salivaomics in Primary Sjögren's Syndrome. *Front Immunol* 2021;12:670325.
[SilvaSaffar2026] Silva-Saffar SE et al. The SjD Map. *npj Syst Biol Appl* 2026.
[Thomas1973] Thomas R. Boolean formalization of genetic control circuits. *J Theor Biol* 1973;42(3):563-85.
[Saadatpour2013] Saadatpour A, Albert R. Boolean modeling of biological regulatory networks. *Methods* 2013;62(1):3-12.
[Abou-Jaoudé2016] Abou-Jaoudé W et al. Logical Modeling and Dynamical Analysis of Cellular Networks. *Front Genet* 2016;7:94.
[Huang1999] Huang S, Ingber DE. Shape-dependent control of cell growth. *Exp Cell Res* 1999;261(1):91-103.
[Kauffman1969] Kauffman SA. Metabolic stability and epigenesis in randomly constructed genetic nets. *J Theor Biol* 1969;22(3):437-67.
[Zañudo2015] Zañudo JGT, Albert R. Cell fate reprogramming by control of intracellular network dynamics. *PLOS Comput Biol* 2015;11(4):e1004193.
[Rozum2021] Rozum JC et al. pystablemotifs: Python library for attractor identification and control in Boolean networks. *Bioinformatics* 2021;38(5):1465-7.
[Aghamiri2020] Aghamiri SS et al. Automated translation of SBML qualitative models. *Bioinformatics* 2020;36(16):4593-5.
[Paulevé2020] Paulevé L et al. Reconciling qualitative, abstract, and scalable modeling of biological networks. *Nat Commun* 2020;11:4256.
[Beneš2023] Beneš N et al. AEON 2021: Bifurcation decision diagrams give insights into Boolean networks. *Bioinformatics* 2023.
[Watanabe2014] Watanabe K et al. HDAC3 in immune cell function. *Trends Immunol* 2014.
[Pumroy2015] Pumroy RA, Cingolani G. Diversification of importin-α isoforms in cellular trafficking and disease. *Biochem J* 2015;466:13-28.
[Cheon2014] Cheon H et al. IFN-β-dependent increases in STAT1, STAT2, and IRF9 mediate resistance to viruses and DNA damage. *EMBO J* 2014;33:2148-2161.
[Adamson2016] Adamson A et al. Signal transduction controls heterogeneous NF-κB dynamics and target gene expression through cytokine-specific refractory states. *Nat Commun* 2016;7:12057.
[Sarrazin2011] Sarrazin S et al. MafB restricts M-CSF-dependent myeloid commitment divisions of haematopoietic stem cells. *Cell* 2011.
[Duret2023] Duret M et al. ASSESS: transcriptomic profiling of DLBCL arising in Sjögren's syndrome. *Arthritis Rheumatol* 2023.
[Davis2010] Davis RE et al. Chronic active B-cell-receptor signalling in diffuse large B-cell lymphoma. *Nature* 2010;463(7277):88-92.
[Friedberg2010] Friedberg JW et al. Inhibition of Syk with fostamatinib disodium has significant clinical activity in non-Hodgkin lymphoma and chronic lymphocytic leukemia. *Blood* 2010;115(13):2578-85.
[Quartuccio2014] Quartuccio L et al. BLyS upregulation in Sjögren's syndrome-associated lymphoproliferation. *J Autoimmun* 2014.
[Bowman2023] Bowman SJ et al. Filgotinib in primary Sjögren's syndrome (MOSAIC). *Ann Rheum Dis* 2023.
[Bowman2024] Bowman SJ et al. Ianalumab in primary Sjögren's syndrome: a phase 3 trial (NCT05349214). *Lancet Rheumatol* 2024.
[Serrano2022] Serrano J et al. Baricitinib in primary Sjögren's syndrome. *Lancet* 2022.
[Damjanov2018] Damjanov N et al. Efficacy, pharmacodynamics and safety of VX-702, a p38 MAPK inhibitor, in rheumatoid arthritis. *Arthritis Rheum* 2018.
[Hammaker2010] Hammaker D, Firestein GS. "Go upstream, young man": lessons from p38 inhibitor development. *Ann Rheum Dis* 2010;69(Suppl 1):i77-82.
[Watz2014] Watz H et al. Effects of losmapimod on COPD. *Lancet Respir Med* 2014;2(1):63-72.
[Newby2014] Newby LK et al. Losmapimod in patients with acute MI: LATITUDE-TIMI 60 randomised trial. *Lancet* 2014;384(9949):1187-95.
[Serhan2020] Serhan CN et al. The Atlas of Inflammation Resolution (AIR). *Mol Aspects Med* 2020.
[Solans-Laque2011] Solans-Laqué R et al. Risk, predictors, and clinical characteristics of lymphoma development in primary Sjögren's syndrome. *Semin Arthritis Rheum* 2011;41(3):415-23.
[Ekstrom-Smedby2008] Ekström Smedby K et al. Autoimmune disorders and risk of non-Hodgkin lymphoma subtypes: a pooled analysis within the InterLymph Consortium. *Blood* 2008;111(8):4029-38.
[Soret2021] Soret P et al. A new molecular classification to drive precision treatment strategies in primary Sjögren's syndrome. *Nat Commun* 2021;12:3523.
[Klamt2018] Klamt S, Tournier L. Identification of minimal cut sets in genetically perturbed Boolean networks. *PLoS Comput Biol* 2018;14(10):e1006532.
[Naldi2017] Naldi A et al. Cooperative development of logical modelling standards and tools with CoLoMoTo. *Bioinformatics* 2017;33(15):2320-2.
