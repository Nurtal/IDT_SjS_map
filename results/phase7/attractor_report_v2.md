# Rapport attracteurs v2 — Phase 7.1.4

**Modèle :** `models/sbmlqual/v2/sjd_map_v2.bnet` (HDAC3=1, KPNB1=1)

Sous semantique MP, les trap-spaces minimaux sont les attracteurs ;
une coordonnée à `*` indique un nœud oscillant dans l'attracteur.
Pour le décompte des phénotypes et des ISGs, `*` est traité comme
*activable* (= 1 dans au moins une trajectoire de l'attracteur).

## Phénotypes actifs / activables par attracteur

| Condition | Attracteur | Type | n_dyn | n_actifs | Phénotypes actifs |
|---|---|---|---|---|---|
| Naive (homeostatic) | A1 | fixed_point | 79 | 7 | B Cell Activation Survival|Cell Proliferation Survival|Chemotaxis Infiltration|Inflammation|MHC Class 2 Activation|Regulated Necrosis|T Cell Activation Differentiation |
| Naive (homeostatic) | A2 | fixed_point | 79 | 2 | Chemotaxis Infiltration|Regulated Necrosis |
| IFN-stimulated | A1 | trap_space | 253 | 9 | B Cell Activation Survival|Cell Proliferation Survival|Chemotaxis Infiltration|Inflammation|MHC Class 1 Activation|MHC Class 2 Activation|Matrix degradation|Regulated Necrosis|T Cell Activation Differentiation |
| BCR-stimulated | A1 | fixed_point | 64 | 7 | B Cell Activation Survival|Cell Proliferation Survival|Chemotaxis Infiltration|Inflammation|MHC Class 2 Activation|Regulated Necrosis|T Cell Activation Differentiation |
| BCR-stimulated | A2 | fixed_point | 64 | 7 | B Cell Activation Survival|Cell Proliferation Survival|Chemotaxis Infiltration|Inflammation|MHC Class 2 Activation|Regulated Necrosis|T Cell Activation Differentiation |

## Audit ISG (validation correction IFN-I)

| Condition | Attracteur | n_ISGs activables | STAT1 | STAT1_p | ISGF3_nucleus | MX1 | OAS1 | ISG15 | IRF7_Cell |
|---|---|---|---|---|---|---|---|---|---|
| Naive (homeostatic) | A1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| Naive (homeostatic) | A2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| IFN-stimulated | A1 | 17 | 1 | * | * | * | * | * | * |
| BCR-stimulated | A1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| BCR-stimulated | A2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

### Critère 7.1.1 : ≥ 3 ISGs canoniques activables sous IFN-stim → **✅ ATTEINT** (max observé : 17 ISGs)

*Le critère utilise les coordonnées de trap-space MP : `1` ou `*` = activable.*
