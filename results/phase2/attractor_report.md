# Rapport attracteurs — Phase 2

**Date :** 2026-05-05  
**Outil :** mpbn 4.3.2 (Most Permissive Boolean Network, ASP/clingo)  
**Modèle :** models/sbmlqual/v1/sjd_map_reduced_clean.bnet (508 nœuds, 104 entrées)

## Méthodologie

- Les 104 nœuds entrées (self-loops) sont fixés selon la condition biologique.
- Propagation des constantes → réseau réduit dynamique.
- Points fixes calculés avec mpbn (Most Permissive update, solveur ASP/clingo).
- Vérification des attracteurs cycliques (has_cyclic_attractor).

## Résultats par condition

### Naive (homeostatic)

| Paramètre | Valeur |
|---|---|
| Nœuds dynamiques | 79 |
| Trap spaces minimaux | 2 |
| Attracteurs cycliques | Non |
| Points fixes | 2 |

| Attracteur | Phénotypes actifs |
|---|---|
| FP1 (**état inflammatoire**) | B Cell Activation Survival · Cell Proliferation Survival · Chemotaxis Infiltration · Inflammation · MHC Class 2 Activation · Regulated Necrosis · T Cell Activation Differentiation |
| FP2 (état basal) | Chemotaxis Infiltration · Regulated Necrosis |

### IFN-stimulated

| Paramètre | Valeur |
|---|---|
| Nœuds dynamiques | 70 |
| Trap spaces minimaux | 2 |
| Attracteurs cycliques | Non |
| Points fixes | 2 |

| Attracteur | Phénotypes actifs |
|---|---|
| FP1 (**état inflammatoire**) | B Cell Activation Survival · Cell Proliferation Survival · Chemotaxis Infiltration · Inflammation · MHC Class 2 Activation · Regulated Necrosis · T Cell Activation Differentiation |
| FP2 (**état inflammatoire**) | B Cell Activation Survival · Chemotaxis Infiltration · Inflammation · MHC Class 2 Activation · Regulated Necrosis · T Cell Activation Differentiation |

### BCR-stimulated

| Paramètre | Valeur |
|---|---|
| Nœuds dynamiques | 64 |
| Trap spaces minimaux | 2 |
| Attracteurs cycliques | Non |
| Points fixes | 2 |

| Attracteur | Phénotypes actifs |
|---|---|
| FP1 (**état inflammatoire**) | B Cell Activation Survival · Cell Proliferation Survival · Chemotaxis Infiltration · Inflammation · MHC Class 2 Activation · Regulated Necrosis · T Cell Activation Differentiation |
| FP2 (**état inflammatoire**) | B Cell Activation Survival · Cell Proliferation Survival · Chemotaxis Infiltration · Inflammation · MHC Class 2 Activation · Regulated Necrosis · T Cell Activation Differentiation |

## Synthèse biologique

### Observations clés

1. **Attracteur pathologique universel** : un point fixe avec 7 phénotypes actifs
   (Inflammation, B/T Cell Activation, MHC-II, Chemotaxis, Cell Proliferation, Regulated Necrosis)
   est présent dans TOUTES les conditions. Il représente l'état SjD.

2. **Activation constitutive** : Chemotaxis/Infiltration et Regulated Necrosis
   apparaissent dans TOUS les attracteurs → activité basale du modèle.

3. **Attracteur BCR** : sous stimulation BCR, les deux points fixes convergent
   vers le même état inflammatoire → le BCR est un driver de maladie.

4. **IFN crée un état intermédiaire** : FP2 IFN = inflammation sans prolifération cellulaire.
   Signature type I IFN de la SjD (cf. PRECISESADS).

5. **Absence d'attracteurs cycliques** : le réseau converge toujours vers des états stables.

## Fichiers produits

-  — catalogue complet (6 attracteurs × 14 phénotypes)
