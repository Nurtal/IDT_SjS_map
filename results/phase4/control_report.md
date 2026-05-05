# Rapport d'analyse de contrôle — Phase 4

**Date :** 2026-05-05  
**Méthode :** Crible de perturbations mono-nœud (inhibition/activation)  
**Réseau :** Condition Naive (79 nœuds dynamiques)  
**Attracteur cible à éliminer :** FP1 (7 phénotypes actifs = état SjD)

## 1. Résumé du crible

- Perturbations testées : 158 (79 nœuds × 2 valeurs)
- Perturbations éliminant l'attracteur maladif : **7**

## 2. Perturbations éliminant l'attracteur SjD

| Nœud | Perturbation | FPs restants | Phénotypes min actifs | Meilleurs phénotypes |
|---|---|---|---|---|
| NFKB1_rna | force=1 | 0 | 0 | — |
| AP1_complex | force=0 | 2 | 2 | Chemotaxis Infiltration · Regulated Necrosis |
| EIF2AK2_homodimer | force=0 | 1 | 2 | Chemotaxis Infiltration · Regulated Necrosis |
| FOS_phosphorylated | force=0 | 2 | 2 | Chemotaxis Infiltration · Regulated Necrosis |
| JUN_phosphorylated | force=0 | 2 | 2 | Chemotaxis Infiltration · Regulated Necrosis |
| MAP2K6_phosphorylated | force=0 | 2 | 2 | Chemotaxis Infiltration · Regulated Necrosis |
| MAPK11_12_13_14_phosphorylated | force=0 | 2 | 2 | Chemotaxis Infiltration · Regulated Necrosis |

## 3. Top 20 perturbations par réduction de phénotypes

| Nœud | Perturbation | Δ phénotypes min | Maladie éliminée |
|---|---|---|---|
| NFKB1_rna | force=1 | +2 | ✓ |
| RIPK3 | force=0 | +1 | ○ |
| Regulated_Necrosis_phenotype | force=0 | +1 | ○ |
| TNFAIP3 | force=1 | +1 | ○ |
| TNFAIP3_rna | force=1 | +1 | ○ |
| AP1_complex | force=0 | +0 | ✓ |
| Angiogenesis_phenotype | force=0 | +0 | ○ |
| Apoptosis_phenotype | force=0 | +0 | ○ |
| BCL2A1_rna | force=0 | +0 | ○ |
| BCL2A1_rna | force=1 | +0 | ○ |
| BCL2L1_rna | force=0 | +0 | ○ |
| BCL2L1_rna | force=1 | +0 | ○ |
| BCL2_rna | force=0 | +0 | ○ |
| BCL2_rna | force=1 | +0 | ○ |
| BIRC2_Cell | force=0 | +0 | ○ |
| BIRC2_Cell | force=1 | +0 | ○ |
| BIRC2_rna | force=0 | +0 | ○ |
| BIRC2_rna | force=1 | +0 | ○ |
| B_Cell_Activation_Survival_phenotype | force=0 | +0 | ○ |
| CASP3 | force=0 | +0 | ○ |

## 4. Cibles thérapeutiques SjD — confrontation au crible

Phase max = phase d'essai clinique maximum atteinte. ✓ = perturbation élimine l'attracteur SjD.

| Gène | Phase max | Médicaments | Nœud BNET | Inhib. Δmin | Activ. Δmin |
|---|---|---|---|---|---|
| CHRM1 | 4 | PILOCARPINE | — (absent BNET) | — | — |
| CHRM3 | 4 | PILOCARPINE | — (absent BNET) | — | — |
| MIF | 4 | IGURATIMOD | — (absent BNET) | — | — |
| NR3C1 | 4 | DEXAMETHASONE|PREDNISOLONE|PRE | — (absent BNET) | — | — |
| PPIA | 4 | CYCLOSPORINE | — (absent BNET) | — | — |
| PTGS2 | 4 | IGURATIMOD | PTGS2 | +0 | -1 |
| TLR7 | 4 | HYDROXYCHLOROQUINE|HYDROXYCHLO | TLR7_ssRNA_complex | — | — |
| TLR9 | 4 | HYDROXYCHLOROQUINE|HYDROXYCHLO | CpG_DNA_TLR9_complex | — | — |
| TRAF3IP2 | 4 | IGURATIMOD | — (absent BNET) | — | — |
| CD80 | 3 | ABATACEPT | CD80 | — | — |
| CD80 | 3 | ABATACEPT | CD80_86 | — | — |
| CD80 | 3 | ABATACEPT | CD80_86_CTLA4_complex | — | — |
| CD80 | 3 | ABATACEPT | CD80_86_rna | — | — |
| CD86 | 3 | ABATACEPT | CD86 | — | — |
| TNFRSF13C | 3 | IANALUMAB | — (absent BNET) | — | — |
| BTK | 2 | TIRABRUTINIB | BTK_phosphorylated | — | — |
| CD40 | 2 | ISCALIMAB | CD40 | — | — |
| CD40 | 2 | ISCALIMAB | CD40LG | — | — |
| CD40 | 2 | ISCALIMAB | CD40LG_CD40_complex | — | — |
| CD40 | 2 | ISCALIMAB | CD40_rna | — | — |
| CD40LG | 2 | RAVAGALIMAB | CD40LG | — | — |
| CD40LG | 2 | RAVAGALIMAB | CD40LG_CD40_complex | — | — |
| CTSS | 2 | PETESICATIB | — (absent BNET) | — | — |
| DHODH | 2 | LEFLUNOMIDE | — (absent BNET) | — | — |
| FCGRT | 2 | EFGARTIGIMOD ALFA|NIPOCALIMAB | — (absent BNET) | — | — |
| FKBP1A | 2 | SIROLIMUS|TACROLIMUS | — (absent BNET) | — | — |
| ICOSLG | 2 | AMG-557 | ICOSLG | — | — |
| ICOSLG | 2 | AMG-557 | ICOSLG_ICOS_complex | — | — |
| IFNAR1 | 2 | ANIFROLUMAB | — (absent BNET) | — | — |
| IL17A | 2 | TIBULIZUMAB | IL17A | +0 | -1 |
| IMPDH1 | 2 | MYCOPHENOLATE MOFETIL|MYCOPHEN | — (absent BNET) | — | — |
| IMPDH2 | 2 | MYCOPHENOLATE MOFETIL|MYCOPHEN | — (absent BNET) | — | — |
| ITGAL | 2 | EFALIZUMAB | — (absent BNET) | — | — |
| JAK1 | 2 | BARICITINIB|FILGOTINIB|TOFACIT | JAK1_phosphorylated | — | — |
| JAK2 | 2 | BARICITINIB|TOFACITINIB | JAK2_phosphorylated | — | — |
| JAK3 | 2 | TOFACITINIB | JAK3_phosphorylated | — | — |
| LTA | 2 | BAMINERCEPT | LTA | — | — |
| LTA | 2 | BAMINERCEPT | LTA_TNFR2_complex | — | — |
| LTB | 2 | BAMINERCEPT | LTB | — | — |
| LTB | 2 | BAMINERCEPT | LTBR | — | — |
| LTB | 2 | BAMINERCEPT | LTB_TNFSF14_LTBR_complex | — | — |
| MS4A1 | 2 | RITUXIMAB | — (absent BNET) | — | — |
| PIK3CD | 2 | LENIOLISIB|PARSACLISIB|SELETAL | — (absent BNET) | — | — |
| SYK | 2 | LANRAPLENIB | SYK_phosphorylated | — | — |
| TNF | 2 | ETANERCEPT | LTA_TNFR2_complex | — | — |
| TNF | 2 | ETANERCEPT | LTB_TNFSF14_LTBR_complex | — | — |
| TNF | 2 | ETANERCEPT | TNFAIP3 | +0 | +1 |
| TNF | 2 | ETANERCEPT | TNFAIP3_rna | +0 | +1 |
| TNF | 2 | ETANERCEPT | TNFRSF10A_B | +0 | +0 |
| TNF | 2 | ETANERCEPT | TNFRSF10A_rna | +0 | +0 |
| TNF | 2 | ETANERCEPT | TNFRSF13B | — | — |
| TNF | 2 | ETANERCEPT | TNFRSF17 | — | — |
| TNF | 2 | ETANERCEPT | TNFRSF1B | — | — |
| TNF | 2 | ETANERCEPT | TNFSF10 | — | — |
| TNF | 2 | ETANERCEPT | TNFSF11 | — | — |
| TNF | 2 | ETANERCEPT | TNFSF13 | — | — |
| TNF | 2 | ETANERCEPT | TNFSF13B_Extracellular_ligands | — | — |
| TNF | 2 | ETANERCEPT | TNFSF13B_Secreted_molecules | +0 | -1 |
| TNF | 2 | ETANERCEPT | TNFSF14 | — | — |
| TNF | 2 | ETANERCEPT | TNFSF15 | — | — |
| TNF | 2 | ETANERCEPT | TNFSF15_TNFRSF25_complex | — | — |
| TNF | 2 | ETANERCEPT | TNF_Extracellular_ligands | — | — |
| TNF | 2 | ETANERCEPT | TNF_Secreted_molecules | +0 | -1 |
| TNF | 2 | ETANERCEPT | TNF_TNFR1_complex | — | — |
| TNF | 2 | ETANERCEPT | TNF_TNFR2_complex | — | — |
| TNFSF13B | 2 | BELIMUMAB|TIBULIZUMAB | TNFSF13B_Extracellular_ligands | — | — |
| TNFSF13B | 2 | BELIMUMAB|TIBULIZUMAB | TNFSF13B_Secreted_molecules | +0 | -1 |
| TNFSF14 | 2 | BAMINERCEPT | LTB_TNFSF14_LTBR_complex | — | — |
| TNFSF14 | 2 | BAMINERCEPT | TNFSF14 | — | — |
| TYK2 | 2 | TOFACITINIB | TYK2_phosphorylated | — | — |
| IL2RA | 1 | ALDESLEUKIN | IL2RA | — | — |
| IL2RB | 1 | ALDESLEUKIN | — (absent BNET) | — | — |

## 5. Test des inhibiteurs cliniques en conditions stimulées

Les cibles des essais cliniques (JAK, BTK, SYK) ne sont pas dans les 79 nœuds dynamiques
de la condition Naive — elles sont fixées à 0 par propagation des constantes.
Test effectué en forçant leur inhibition dans les conditions IFN et BCR :

| Condition | Perturbation | FPs | Maladie éliminée | Phénotypes FP1 |
|---|---|---|---|---|
| IFN base | — | 2 | non | 7 (état SjD) |
| IFN + JAK1=0 | JAK inhibiteur | 2 | **non** | 7 (inchangé) |
| IFN + TYK2=0 | JAK/TYK inhibiteur | 2 | **non** | 7 (inchangé) |
| IFN + STAT2=0 | — | 2 | **non** | 7 (inchangé) |
| BCR base | — | 2 | non | 7 (état SjD) |
| BCR + BTK=0 | Tirabrutinib | 2 | **non** | 7 (inchangé) |
| BCR + SYK=0 | Lanraplenib | 2 | **non** | 7 (inchangé) |
| BCR + AP1=0 | — | 2 | **OUI ✓** | 2 (Chemotaxis+Reg.Necrosis) |
| BCR + FOS=0 | — | 2 | **OUI ✓** | 2 (Chemotaxis+Reg.Necrosis) |
| BCR + JUN=0 | — | 2 | **OUI ✓** | 2 (Chemotaxis+Reg.Necrosis) |

## 6. Synthèse biologique

### Nœuds de contrôle identifiés

**Module AP1/p38 MAPK** — nœud de contrôle central :
```
EIF2AK2_homodimer → MAP2K6_phosphorylated → MAPK11-14_phosphorylated
                    MAP2K3_phosphorylated ↗                         ↓
                                                      FOS_phosphorylated + JUN_phosphorylated
                                                                    ↓
                                                             AP1_complex → [Inflammation pathway]
```

6 perturbations sur 7 ciblent ce module (inhibition AP1, FOS, JUN, p38, MAP2K6, EIF2AK2).
L'inhibition de **n'importe quel nœud de ce module** élimine l'attracteur SjD.

### Résistance aux inhibiteurs cliniques actuels

Dans ce modèle, les cibles des essais cliniques Phase 2-4 (JAK1/2/3, BTK, SYK, TYK2)
**ne modifient pas l'attracteur SjD** quand inhibées seules :
- Leur activité est en amont de l'attracteur mais leur absence ne coupe pas
  la boucle AP1 (autres voies MAPK compensent)
- Cohérent avec les résultats mitigés des JAK inhibiteurs en SjD cliniquement

### Cible émergente non couverte

**EIF2AK2 (PKR)** — kinase PKR, activée par dsRNA/ISG15/LPS :
- Aucun médicament SjD en essai clinique ne cible directement PKR
- PKR→p38→AP1 est une voie peu explorée en SjD
- Des inhibiteurs PKR existent (C16, imoxin) mais pas en essai SjD

### Décision Go Phase 5

✅ **GO Phase 5** — validation thérapeutique :
- Cibles prioritaires : **AP1_complex** (FOS/JUN), **MAPK11-14** (p38), **EIF2AK2** (PKR)
- Confrontation aux données d'essais cliniques H4 : filgotinib/baricitinib insuffisants seuls
- Prédiction : combinaison JAK-inhibiteur + p38-inhibiteur serait synergique

