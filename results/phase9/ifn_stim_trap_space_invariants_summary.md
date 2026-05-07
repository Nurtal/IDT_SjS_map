# IFN-stimulated trap-space attractor — invariants


- 1-invariants (always active): **50**
- 0-invariants (always inactive): **277**
- oscillating (`*`, reachable both states): **181**
- total: **508**

## 1-invariants — examples (first 30 sorted)

AP1_complex, B_Cell_Activation_Survival_phenotype, CASP3, CD82_rna, CDKN1A_rna, CSF2, Cell_Proliferation_Survival_phenotype, Chemotaxis_Infiltration_phenotype, EIF2AK2_homodimer, FAS, FAS_rna, FOS_phosphorylated, GADD45B_rna, HDAC3, IFNAR_complex, IFNA_Extracellular_ligands, IFNA_IFNAR_complex, IFNB1_Extracellular_ligands, IFNB_IFNAR_complex, IFNG, IFNG_IFNGR_complex, IKBIP, IKBIP_rna, IL10, IL2, IL4, IL5, Inflammation_phenotype, JUN_phosphorylated, KPNB1 ...

## 0-invariants — examples (first 30 sorted)

AKT, Ag_IgG_FCGR1A_complex, Ag_IgG_FCGR2A_complex, Ag_IgG_FCGR3A_complex, Ag_IgG_complex, Allergen_IgE_FCERI_complex, Angiogenesis_phenotype, Apoptosis_phenotype, BAD, BAFF_APRIL_BCMA_complex, BAFF_APRIL_TACI_complex, BAFF_BAFFR_complex, BCL2A1_rna, BCR_complex, BIRC2_Cell, BIRC2_Cell_1, BIRC2_rna, BLNK_phosphorylated, BTK_phosphorylated, C3a, C3a_CA3R1_complex, C5a, C5a_C5AR1_complex, CALM1, CAMKMT, CARD11_BCL10_MALT1_complex, CCL11, CCL11_CCR3_complex, CCL13, CCL16 ...

## Interpretation

The IFN-stim attractor's invariant skeleton — nodes whose value 
is determined for the entire attractor — defines the *stable* 
part of the IFN response. The oscillating coordinates form the 
*envelope* of states reachable under sustained IFN stimulation 
with active SOCS / USP18 / PIAS feedback. The downstream ISGs 
(MX1, OAS1-3, ISG15, IFIT1/3, IFITM1) and the ISGF3 nuclear 
complex fall in the oscillating set: they are *activable* in 
every attractor trajectory but not pinned to a single value at 
all times — an MP-formal expression of the refractory dynamic 
produced by negative feedback.

Per-node table: `results/phase9/ifn_stim_trap_space_invariants.csv`.