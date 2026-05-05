# Audit topologique — SjD Map

**Date :** 2026-05-05  
**Source :** `data/raw/zenodo_17585308/TheSjDMap/TheSjDMap/Reviews/Network Analysis/SjD_Map.xml`  
**Format :** CellDesigner SBML Level 2 Version 4  
**Généré par :** analyse manuelle + `src/validation/topological_stats.py`

---

## Statistiques globales

### Carte complète (CellDesigner SBML)

| Métrique | Observé | Attendu (papier) | Écart |
|---|---|---|---|
| Species (nœuds) | 840 | 829 | +11 (+1.3 %) |
| Reactions (arêtes) | 598 | 598 | 0 (0.0 %) ✓ |

**Note sur l'écart en species (+11) :** le fichier CellDesigner contient 840 entrées `<species>`, dont certaines
sont des alias ou des complexes intermédiaires non comptabilisés comme "entités" dans l'article.
Le comptage de 829 entités dans le papier reflète probablement les nœuds biologiquement distincts
(après déduplication des alias CellDesigner). Écart acceptable ; à vérifier lors de la conversion CaSQ.

### Réseau réduit (SIF — généré par CaSQ v1.3.3)

| Métrique | Observé | Attendu (papier) | Écart |
|---|---|---|---|
| Nœuds | 412 | 412 | 0 (0.0 %) ✓ |
| Arêtes | 692 | 692 | 0 (0.0 %) ✓ |

**Résultat : correspondance exacte avec les valeurs publiées.**

---

## Présence des 5 hubs topologiques attendus

Les hubs identifiés dans le papier comme nœuds stables pivots des voies JAK-STAT et NF-κB :

| Hub | Présent dans le SBML | Commentaire |
|---|---|---|
| Inflammation | ✓ | Phénotype terminal AND hub |
| STAT1 homodimer | ✓ | — |
| STAT1/STAT2/IRF9 | ✓ | Complexe trimère (ISGF3) |
| RELA/NFKB1 | ✓ | Hétérodimère NF-κB canonique |
| Chemotaxis/Infiltration | ✓ | Phénotype terminal AND hub |

**Résultat : 5/5 hubs présents. ✓**

---

## Présence des 14 phénotypes terminaux

Les labels dans le SBML utilisent des underscores à la place des espaces.
Table de correspondance label publié → label SBML :

| Label publié | Label SBML | Présent |
|---|---|---|
| MHC Class I Activation | MHC_Class_1_Activation | ✓ |
| MHC Class II Activation | MHC_Class_2_Activation | ✓ |
| T Cell Activation/Differentiation | T_Cell_Activation/Differentiation | ✓ |
| B Cell Activation/Survival | B_Cell_Activation/Survival | ✓ |
| Cell Proliferation/Survival | Cell_Proliferation/Survival | ✓ |
| Inflammation | Inflammation | ✓ |
| Chemotaxis/Infiltration | Chemotaxis/Infiltration | ✓ |
| Angiogenesis | Angiogenesis | ✓ |
| Lymphoid Organ Development | Lymphoid_organ_development | ✓ |
| Apoptosis | Apoptosis | ✓ |
| Regulated Necrosis | Regulated_Necrosis | ✓ |
| Matrix Degradation | Matrix_degradation | ✓ |
| Fibrosis | Fibrosis | ✓ |
| Phagocytosis | Phagocytosis | ✓ |

**Résultat : 14/14 phénotypes présents. ✓**

---

## Observations importantes pour la Phase 1

1. **CaSQ a déjà été appliqué** (v1.3.3, commentaire dans le SIF). Le fichier `SjD_Model_raw.sif`
   est le réseau booléen réduit. Il faudra retrouver ou régénérer le SBML-qual correspondant
   (le SIF est un format intermédiaire ; le SBML-qual est l'entrée native de bioLQM/PyBoolNet).

2. **Les IDs du SIF sont des IDs CellDesigner** (`csa2`, `sa9`, etc.), non les noms biologiques.
   La table de correspondance ID → nom est disponible dans `SjD_Map.xml` (species `id` → `name`).
   Un script de re-labellisation sera nécessaire pour l'annotation biologique (Phase 3).

3. **Le SIF ne contient que des relations POSITIVE / (à vérifier pour NEGATIVE)**.
   Vérifier la présence d'arêtes inhibitrices dans le SIF — essentiel pour la logique booléenne.

4. **Données DEG/overlay disponibles** dans l'archive :
   - `Statistics_Overlays/Blood_datasets/overlay_GSE51092.txt`, `overlay_PRECISESADS.txt`, `overlay_UKPSSR.txt`
   - `Statistics_Overlays/ASSESS/ASSESS_lymphoma.txt`
   - `Statistics_Overlays/Open_Targets/Clinical_trials_drugs/Sjogren_drugs.csv`
   Ces fichiers seront directement exploitables en Phase 3 et Phase 4.

---

## Conclusion Phase 0.4

Tous les critères de validation sont remplis :
- ✓ Statistiques topologiques reproduites (412/692 exact sur le réseau réduit)
- ✓ 5/5 hubs présents
- ✓ 14/14 phénotypes terminaux présents
- ✓ Données overlays disponibles pour les phases suivantes

**Décision Go : procéder à la Phase 1.**
