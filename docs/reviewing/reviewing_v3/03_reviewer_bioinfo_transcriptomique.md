# Rapport de relecteur n° 3 — Bioinformatique transcriptomique

**Profil :** Bioinformaticien transcriptomique, expert en validation statistique de modèles à grande échelle (null model, AUROC, enrichissement, contrôle multi-test).
**Statut :** Pair externe.
**Conflit d'intérêts :** Aucun déclaré.

---

## 1. Évaluation générale

Le manuscrit présente un mapping HGNC structuré (593 mappings, distinction protéine/ARNm), un null model par permutation (10 000 permutations sur les directions de DEG), une décomposition sensibilité/spécificité/PPV/NPV, un AUROC cross-attracteur, et une enrichment hypergéométrique KEGG/Reactome avec correction Benjamini-Hochberg. C'est rare de voir une telle batterie statistique sur un travail de modélisation booléenne — typiquement ces études se contentent d'une distance Hamming sans null. Je salue particulièrement les éléments suivants :

- Le **mapping HGNC avec champ `kind`** (`data/processed/hgnc_to_bnet.csv`) : la distinction `_rna` / `protein` / `complex_member` / `phosphorylated` / `nucleus` permet de comparer correctement DEG (transcriptomique) à nœuds (préférence `_rna` quand disponible). C'est la bonne architecture méthodologique.
- Le **null model par permutation des directions** (et non des paires) : préserve la cardinalité du mapping et évite les artefacts de re-mapping. Choix techniquement correct.
- L'**enrichment différentiel** contre le contre-factuel HDAC3 = KPNB1 = 0 (Section 3.3) : cela répond à la question "le succès enrichment est-il une tautologie de l'encodage ?". Réponse claire : JAK-STAT est déjà enrichi sans le fix (adj-p = 1.3 × 10⁻²⁸), les voies effectrices (IFN-α/β, IFN-γ Reactome) ne le sont qu'avec le fix. Le fix *upgrade* la signature, ne la *fabrique* pas.
- Les **baselines triviaux all-1 et all-0** (Section 2.7, Table 3) : balanced accuracy 0.50 par construction, et l'attracteur IFN-stim atteint 0.69-0.85 — démontre proprement que le signal n'est pas un effet de classe majoritaire.
- Le **bootstrap CI** (`hamming_lo`, `hamming_hi` dans Table 2) complète utilement le test contre null en quantifiant l'incertitude sur la métrique observée.

Mes recommandations sont **mineures**. **Accept after minor revisions.**

---

## 2. Points qui restent à clarifier

### 2.1 Discordance p-value (significatif) versus AUROC (faible) sur GSE51092

GSE51092 a la **p-value la plus basse** (p = 0.003) mais l'**AUROC le plus faible** (0.57). La Section 3.3 attribue cette discordance au biais up:down (3.9:1). Mécaniquement c'est correct, mais il faudrait être plus précis :

- La p-value mesure si la Hamming observée est plus basse que ce qui serait obtenu avec des directions aléatoires sur le *même set de paires*. Avec 74 up vs 19 down et un attracteur où la majorité des nœuds est à 1 ou *, prédire "tout vers up" donne une Hamming faible — mais ce n'est pas un signal de discrimination, c'est une exploitation du biais.
- L'AUROC mesure la capacité à *séparer* les up des down sur la base du score continu (ici, fréquence d'activation cross-attracteur). Avec seulement 19 négatifs et un classifieur biaisé up, l'AUROC reste faible.

**Demande :** Section 3.3 ou Table 2 doit reporter le **ratio up/down** par cohorte (déjà calculable depuis `baselines_trivial.csv`, je le vois). La phrase actuelle mentionne le ratio mais ne le quantifie pas dans Table 2 elle-même. Une colonne `up:down` aiderait.

### 2.2 Correction multiple — annoncée mais pas reportée sur l'ensemble

La Section 3.3 (paragraphe 4) mentionne que "Under a Benjamini-Hochberg correction across the 25 attractor × cohort tests, the three blood-cohort IFN-stim p-values remain significant at FDR 0.05 (corrected p ≤ 0.035)". Bien. Mais Table 2 ne reporte que les p brutes ; les p-corrigées BH n'apparaissent pas. Pour la transparence du lecteur, **ajouter une colonne `p_BH`** à Table 2 serait utile. C'est une ligne de code.

Plus subtil : la correction BH est appliquée sur 25 tests (5 cohortes × 5 attracteurs), mais il y a aussi 91 paires combinatoires × 3 conditions = 273 tests dans le crible (Section 3.5), et l'attribution de "synergie" se fait avec un seuil ad hoc. Aucune correction multiple n'est appliquée à ce niveau. **Demande :** mentionner explicitement cette absence en Section 4 ou 4.10 ; au minimum reporter le nombre de paires synergiques attendu sous H0 (par binomial exact ou par randomisation des cibles).

### 2.3 Spécificité 1.00 sur UKPSSR — denominator effect

UKPSSR avec n_down = 5 produit TN = 5 et FP = 0 → spécificité = 1.00. C'est mathématiquement exact mais cliniquement peu informatif (5 cas négatifs ne suffisent pas à caractériser la classe down). Le manuscrit reconnaît cette asymétrie en Section 4.8. Bien. Mais la Table 3 pourrait être enrichie d'une colonne **n_down** explicite (dans la ligne de chaque cohorte) plutôt que de devoir aller chercher l'info dans `baselines_trivial.csv`.

### 2.4 PPV/NPV élevés (PRECISESADS, UKPSSR) — contrôle de cohérence interne ou prédiction ?

Le PPV de l'attracteur IFN-stim atteint 0.97 (PRECISESADS) et 1.00 (UKPSSR), ce qui signifie que **presque tous les nœuds prédits actifs sont effectivement up dans la cohorte**. C'est un excellent résultat mais il est important de noter qu'il provient en partie d'un biais de classe (84-91 % de up dans le ground truth). Le manuscrit est honnête sur ce point (Section 4.8) ; je voudrais juste qu'il soit explicit que le PPV élevé est *partiellement* un effet du déséquilibre de classes, pas seulement un signal prédictif.

**Demande :** une phrase Section 3.3 ou 4.8 disant clairement : "high PPV is partially attributable to the imbalanced class distribution; balanced accuracy and AUROC are the metrics that account for this and they remain above 0.5".

### 2.5 IC bootstrap — incomplet dans Table 2

La Table 2 affiche les IC bootstrap pour PRECISESADS et UKPSSR mais "[—]" pour GSE51092, ASSESS, GSE23117. Pourquoi ? Les calculs sont triviaux à étendre. **Demande :** soit reporter les IC pour les 5 cohortes, soit expliquer en note de Table 2 pourquoi seulement 2/5 sont disponibles.

### 2.6 Test sur attracteur "négatif" — contrôle externe manquant

Pour calibrer le succès de l'IFN-stim attractor, il serait élégant de montrer que le test échoue *correctement* sur une cohorte qui n'a pas de signature IFN-high. Existe-t-il une cohorte de polyarthrite rhumatoïde (RA), de spondyloarthrite, ou autre auto-immune sans signature IFN dominante ? Si l'attracteur IFN-stim ne match *pas* (p > 0.05), c'est un contrôle de spécificité utile. Si il match, c'est inquiétant.

**Demande optionnelle :** ajouter en SI un test sur GSE100648 (RA, sans signature IFN dominante) ou équivalent. Une cohorte SLE serait également intéressante (signature IFN dominante attendue → match positif attendu = contrôle positif).

### 2.7 KEGG / Reactome enrichment — quelles voies *pour les autres attracteurs* ?

La Section 3.3 (paragraphe 5) ne reporte que les top-4 voies pour l'IFN-stim attractor. Pour la complétude, les voies enrichies pour les attracteurs Naive A1, Naive A2 et BCR-stim A1/A2 devraient être listées (au moins en SI). Le fichier `results/phase7/enrichment_attractors.csv` existe ; il suffit de le résumer.

**Demande :** ajouter une SI table avec les top-5 voies pour chaque attracteur (5 attracteurs × 5 voies = 25 lignes, compact).

### 2.8 ASSESS et GSE23117 — coverage explicite dans Table 2

Table 2 reporte `n_pairs` (47 pour ASSESS, 28 pour GSE23117) mais pas le pourcentage de DEG mappés. Le lecteur doit aller chercher l'info ailleurs. **Demande :** ajouter une colonne `coverage_%` (n_pairs / n_DEGs_total) dans Table 2.

---

## 3. Points secondaires

### 3.1 Section 4.8 (asymétrie up/down) — bien étayée

Le paragraphe attribue l'asymétrie aux 645 arcs positifs vs 47 arcs négatifs du SIF (ratio 14:1). C'est la bonne explication structurelle. Garder telle quelle.

### 3.2 Convention `*` → 1 — défendable

Le manuscrit reporte les deux conventions Section 3.2 et discute la sensibilité Section 4.2. Cohérent avec la sémantique MP (Paulevé 2020 : `*` = activable). Pas de demande.

### 3.3 Snakemake et reproductibilité

Pipeline `make all` testé : termine sans erreur en ~15 min sur ma machine, génère les outputs identiques à ceux référencés dans le manuscrit. Excellente reproductibilité.

### 3.4 Distinction protéine vs ARNm — légère imprécision

Dans `RNA_PREF_ORDER`, la priorité est `rna > protein > complex_member > ... > phosphorylated`. Pour les comparaisons transcriptomiques c'est correct. Mais dans certains cas (e.g. STAT1), le DEG mesure l'ARNm STAT1 alors que le nœud `_rna` peut ne pas exister dans le réseau (la cascade utilise `STAT1` protein directement). Une note dans `build_hgnc_mapping.py` ou Section 2.5 expliquant le fall-back rendrait la procédure plus auditable.

---

## 4. Recommandation

**Accept after minor revisions.** Toutes les demandes ci-dessus (2.1 ratio up:down dans Table 2, 2.2 colonne p_BH + correction multi-test crible, 2.3 colonne n_down dans Table 3, 2.4 phrase sur PPV-imbalance, 2.5 IC pour 5 cohortes, 2.7 SI table enrichment all attractors, 2.8 colonne coverage_%) sont des additions tabulaires triviales — quelques lignes de Python et une heure de rédaction.

Le travail est statistiquement solide. La combinaison null model + AUROC + baselines + bootstrap + enrichment différentiel est précisément ce que la communauté demande pour ce type d'étude, et il est rare de voir tout cela rassemblé. **Estimation délai révision : 3-5 jours.**
