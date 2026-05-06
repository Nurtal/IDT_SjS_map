# Rapport de relecteur n° 3 — Bioinformatique transcriptomique et statistique

**Profil :** Bioinformaticien ; expertise en analyses différentielles (limma, DESeq2), enrichissement, intégration multi-cohortes, et méta-analyses transcriptomiques sur cohortes auto-immunes.
**Statut :** Pair externe.
**Conflit d'intérêts :** Aucun déclaré.

---

## 1. Évaluation générale

Le manuscrit propose de confronter les états binaires d'attracteurs booléens à des listes de DEG issues de cinq cohortes (PRECISESADS, UKPSSR, GSE51092, ASSESS, GSE23117). C'est l'aspect du travail qui prétend faire le pont entre le modèle dynamique et la biologie observée.

Malheureusement, **la statistique de validation est faible** et les conclusions tirées des « distances de Hamming » ne tiennent pas la route quantitativement. Les remarques qui suivent sont les plus importantes du rapport.

---

## 2. La distance de Hamming est mal calibrée

### 2.1 Pas de null model

Les valeurs reportées (cf. Tableau 2 du manuscrit) sont :

| Cohorte | Best Hamming (IFN-stim FP1) |
|---|---|
| PRECISESADS | 0.849 |
| UKPSSR | 0.755 |
| GSE51092 | 0.791 |

Le manuscrit affirme (§3.3) qu'« une distance de 0.755 indique 24.5 % de nœuds correctement prédits — significant enrichment compared to random expectation (0.5) ». **Cette affirmation est statistiquement infondée :**

- L'expectation aléatoire n'est PAS 0.5. Avec 149 DEGs up sur 159 mappés en PRECISESADS (94 % up), un modèle qui dirait « tout actif » obtiendrait une distance de 0.06. Un modèle qui dirait « tout inactif » obtiendrait 0.94.
- Le modèle prédit la majorité des nœuds inactifs. La distance observée (0.85–0.96) reflète donc essentiellement la proportion d'up-DEGs *non capturés* par les attracteurs.
- L'« enrichment vs 0.5 » est donc dans le mauvais sens : la distance attendue sous H0 *aléatoire conditionné aux marges* est très différente de 0.5.

**Demande :** calculer un null model par permutation (1) des DEGs entre nœuds mappés, ou (2) des états des attracteurs. Reporter une p-value empirique.

### 2.2 Le score Hamming ne distingue pas les types d'erreur

Une mismatche peut venir de :
- DEG up + nœud à 0 (faux négatif modèle) ;
- DEG down + nœud à 1 (faux positif modèle) ;
- ou les deux symétriques.

Le manuscrit ne distingue pas ces cas. Or pour un papier sur SjD où la signature montre une forte asymétrie (94 % up dans PRECISESADS), l'analyse devrait :

- Reporter sensibilité et spécificité séparément ;
- Calculer un AUROC en utilisant le rang d'activation (ou la fréquence d'activité dans les attracteurs si plusieurs);
- Idéalement faire un test hypergéométrique sur l'enrichissement des nœuds à 1 dans la liste up-DEG.

### 2.3 Couverture du mapping très faible

Couverture nœuds BNET / DEG total :

| Cohorte | DEGs | Nœuds mappés | Couverture |
|---|---|---|---|
| PRECISESADS | 725 | 159 | 22 % |
| UKPSSR | 239 | 53 | 22 % |
| GSE51092 | 1161 | 163 | 14 % |
| ASSESS | 1735 | 61 | 3.5 % |
| GSE23117 | 840 | 55 | 6.5 % |

Sur ASSESS et GSE23117, on ne valide quasi rien — 3.5 et 6.5 % de couverture. Tirer des conclusions sur l'attracteur lymphome (Phase 5.2) à partir de 61 nœuds dont 30 up, 31 down est sous-puissant.

---

## 3. Le mapping gène→nœud est hasardeux

L'auteur utilise (cf. `annotate_attractors.py:147-152`) une regex de substring case-insensitive sur les noms biologiques des nœuds (avec `_` remplacé par espace). Plusieurs problèmes :

### 3.1 Faux positifs

- Le gène `FOS` matchera `FOS_phosphorylated` mais aussi tout nœud contenant la chaîne « FOS » : `FOSL1`, `FOSL2`, `c-FOS`, `FOSB`. Sur le BNET, à vérifier mais probable.
- Le gène `IL2` matchera `IL2`, `IL2_RA`, `IL2_RB`, `IL21`, `IL22`, `IL23A`. La regex avec word-boundaries (`\b`) atténue mais n'élimine pas (`IL2_RA` contient `IL2` à la frontière).
- `STAT1` matche `STAT1`, `STAT1_phosphorylated`, `STAT1_homodimer`, `STAT1_STAT2_IRF9_complex`, etc. Il faut décider si c'est désirable (transitivité du gène vers ses formes) ou bruit.

### 3.2 Faux négatifs

- Les noms standards HGNC ne sont pas toujours utilisés dans la SjD Map. Exemple : `MAPK11_12_13_14_phosphorylated` n'aura pas de correspondance simple si le DEG est listé `MAPK11`, `MAPK12`, etc. — l'auteur traite les MAPKs comme un complexe agrégé, ce qui force le mapping à perdre 3 gènes sur 4.
- Les complexes (`AP1_complex`, `IFNAR_complex`, `MHC_class_2_complex`) ne sont matchables que si le DEG est nommé identiquement, ce qui n'est jamais le cas dans une liste DEG.

**Demande :** utiliser un mapping basé sur HGNC officiel (ou Ensembl ID) avec une table de correspondance manuelle pour les complexes/formes phosphorylées. La couverture doublera probablement, et les distances de Hamming se rapprocheront de leur vraie valeur informative.

### 3.3 Pas de gestion des isoformes / ARNm

Le BNET contient à la fois `STAT1` (protéine) et `STAT1_rna` (ARNm). Un DEG matche les deux. Or seul l'ARNm est mesuré en transcriptomique. Le score Hamming agrège donc deux niveaux d'information sans distinction. Ce point n'est pas discuté.

---

## 4. Cohortes utilisées : reproductibilité

L'auteur réutilise les overlays Cytoscape fournis avec la SjD Map (Zenodo 17585308). Ces overlays sont déjà pré-traités par l'équipe SjD Map (DEG seuils, couleur up/down). Le manuscrit n'a **pas re-fait l'analyse différentielle from raw**, ce qui pose deux problèmes :

1. Les seuils retenus par les auteurs SjD Map sont opaques pour le lecteur de ce manuscrit (logFC, FDR, méthode ?). Une variation de FDR 0.05 → 0.01 changerait significativement les listes.
2. La méta-analyse cross-cohorte est quasi impossible avec des overlays binarisés différemment ; le manuscrit ne peut pas évaluer la concordance inter-cohorte des DEGs originaux.

Pour un journal de méthodologie, je suggère d'au moins rapporter les seuils utilisés par chaque overlay (en se référant à Silva-Saffar 2026 méthodes) et de discuter la sensibilité des conclusions à ces seuils.

---

## 5. La cohorte GSE23117 est mal exploitée

Phase 5.3 affirme « le modèle reflète mieux la biologie sanguine que salivaire » à partir de Hamming 0.89–0.96 vs 0.85–0.91. Or :

- 55 nœuds mappés sur 840 DEGs (6.5 % couverture).
- Différence Hamming : 0.04 — au sein du bruit attendu.
- Aucun test statistique de significativité.
- 53 up / 2 down sur GSE23117 : le mapping est *extrêmement* déséquilibré.

**Cette section ne soutient pas l'affirmation et devrait être marquée comme « insuffisamment puissante » ou retirée.**

---

## 6. Tests d'enrichissement fonctionnel manquants

Pour confronter un attracteur (=état binaire de 64–79 nœuds) à une signature transcriptomique, l'approche standard serait :

1. **Pathway-level enrichment** : pour chaque attracteur, agréger les nœuds actifs par voie KEGG/Reactome. Comparer aux pathways enrichis dans les DEG up.
2. **Gene-set enrichment (GSEA)** : utiliser le rang transcriptomique des cohortes avec une signature « nœuds actifs en FP1 ».
3. **AUROC node ranking** : si plusieurs attracteurs existent, calculer la fréquence d'activation de chaque nœud à travers les attracteurs et la comparer aux fold-changes DEG.

L'auteur fait un *pathway profile* (Phase 3.1) mais sur des keyword sets très grossiers (« STAT1, STAT2, … » pour JAK-STAT) ; l'agrégation est fragile. Il manque un véritable test d'enrichissement *vs* un référentiel canonique.

---

## 7. Points positifs

- Les overlays Zenodo sont correctement référencés et leur SHA-256 calculé (`CHECKSUMS.txt`) — bonne pratique.
- Le code de mapping et de calcul Hamming est lisible et modulaire (`annotate_attractors.py`).
- Le tableau de mapping `deg_mapping.csv` est exporté et réutilisable.
- L'auteur reconnaît la couverture limitée (§4.4 manuscrit).

---

## 8. Recommandations

| Priorité | Action |
|---|---|
| **R3.1** | Calculer un null model par permutation pour chaque distance de Hamming reportée. Reporter p-values empiriques (n=10 000 permutations recommandé). |
| **R3.2** | Remplacer le mapping substring par un mapping HGNC officiel + table manuelle pour complexes/phosphorylés. Reporter le gain en couverture. |
| **R3.3** | Décomposer la distance Hamming en sensibilité / spécificité ; ajouter un AUROC sur le ranking des nœuds. |
| **R3.4** | Rapporter les seuils DEG des overlays originaux (FDR, logFC) et faire une analyse de sensibilité au seuil. |
| **R3.5** | Distinguer protéine vs ARNm dans le mapping et dans le score (pondération différente). |
| **R3.6** | Retirer ou re-cadrer la section GSE23117 (§5.3 manuscrit) : les chiffres ne soutiennent pas l'interprétation cross-tissulaire. |
| **R3.7** | Ajouter un test d'enrichissement de pathways KEGG/Reactome au lieu des keyword-sets ad hoc. |
| **R3.8** | Discuter explicitement le problème de l'asymétrie up/down des DEGs et son effet sur la métrique Hamming. |

---

## 9. Verdict du relecteur

**Recommandation : Major Revision.**

L'aspect bioinformatique du manuscrit, en particulier la confrontation aux DEGs, est l'aspect le plus faible du travail. Sans null model et sans test d'enrichissement, les conclusions transcriptomiques (« IFN-stim FP1 = best match aux cohortes blood ») ne peuvent pas être appuyées. C'est d'autant plus dommage que la modélisation booléenne, elle, est solide.

Les corrections demandées sont relativement légères en termes de code (~1–2 semaines de travail) et auront un impact disproportionné sur la crédibilité du papier.
