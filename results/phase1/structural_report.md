# Rapport de validation structurelle — Phase 1.2

**Date :** 2026-05-05
**Modèle :** `models/sbmlqual/v1/sjd_map_reduced.sbml`

## Statistiques globales

| Métrique | SBML-qual (notre) | Référence publiée | Δ |
|---|---|---|---|
| Nœuds | 508 | 412 | +96 |
| Arêtes (transitions) | 819 | 692 | +127 |
| Arêtes POSITIVE | 751 | — | — |
| Arêtes NEGATIVE | 68 | — | — |

## Présence des phénotypes terminaux

| Phénotype | ID SBML-qual (nom) | Statut |
|---|---|---|
| Inflammation | sa105 (Inflammation_phenotype) | ✓ |
| Apoptosis | sa671 (Apoptosis_phenotype) | ✓ |
| Angiogenesis | sa1703 (Angiogenesis_phenotype) | ✓ |
| Fibrosis | sa1377 (Fibrosis_phenotype) | ✓ |
| Phagocytosis | sa1050 (Phagocytosis_phenotype) | ✓ |
| Chemotaxis/Infiltration | sa1184 (Chemotaxis/Infiltration_phenotype) | ✓ |
| Cell Proliferation | sa1281 (Cell_Proliferation/Survival_phenotype) | ✓ |
| Regulated Necrosis | sa664 (Regulated_Necrosis_phenotype) | ✓ |
| Matrix degradation | sa1700 (Matrix_degradation_phenotype) | ✓ |
| Lymphoid organ | sa179 (Lymphoid_organ_development_phenotype) | ✓ |
| MHC | csa128 (MHC1/B2M/TCR_complex) | ✓ |
| T Cell Activation | sa301 (T_Cell_Activation/Differentiation_phenotype) | ✓ |
| B Cell Activation | sa373 (B_Cell_Activation/Survival_phenotype) | ✓ |

## Décision

- Écart structurel documenté dans `conversion.log` et `audit_logique.md`.
- Tous les phénotypes terminaux présents → ✅ Go Phase 2.

