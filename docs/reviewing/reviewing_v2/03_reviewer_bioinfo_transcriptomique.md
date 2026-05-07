# Rapport de relecture — Bioinformatique transcriptomique (round 2)

**Manuscrit :** v2 (Foulquier, 2026)
**Relecteur :** Dr. T. — Bioinformatique transcriptomique, validation statistique des modèles à grande échelle
**Date :** 2026-05-07
**Recommandation :** **Accept after minor revisions** — toutes mes recommandations majeures (R3.1 null model, R3.3 AUROC, R3.7 enrichissement) sont traitées avec sérieux. Le manuscrit est passé d'une étude statistiquement faible à une étude qui pose les bonnes questions et y répond avec les bons outils. Restent quelques points d'interprétation à serrer.

---

## 1. Avis global

Le travail de révision est exemplaire sur le volet statistique. Les trois piliers que je demandais — null model, AUROC, enrichissement KEGG/Reactome — sont implémentés correctement, leurs outputs sont versionnés (`results/phase7/*.csv`), et leurs interprétations sont prudentes. Le mapping HGNC propre (Phase 7.2.1) donne une couverture de nœuds élevée (97.8 %) ; la couverture côté DEG reste limitée (12.6 % blood, 3.3 % tissue) mais l'auteur reconnaît honnêtement que c'est un plafond structurel de la SjD Map, pas un défaut de la procédure.

L'axe d'amélioration restant porte sur **trois questions d'interprétation statistique** :

1. La p-value du null model et l'AUROC racontent-ils la même histoire ?
2. Le succès de l'enrichissement KEGG/Reactome est-il une conséquence triviale de la correction v2 ?
3. La spécificité élevée (0.74–1.00) reflète-t-elle un signal prédictif réel ou un effet de classe majoritaire ?

---

## 2. Points traités au round 2 — évaluation détaillée

| Reco | Statut | Évaluation |
|---|---|---|
| R3.1 — Null model Hamming | 10 000 perms, p-values reportées par cohorte × attracteur | ✅ Exécuté correctement |
| R3.2 — Mapping HGNC officiel | `hgnc_to_bnet.csv` (593 mappings, kind annotated) | ✅ Bien architecturé |
| R3.3 — Sens / spec / AUROC | `sensitivity_specificity_auroc.csv` | ✅ Décomposition complète |
| R3.4 — Sensibilité aux seuils DEG | Non applicable (DEG sont catégoriques dans les overlays) ; seuil attracteur traité (R4.5) | ⚠ Acceptable mais à mentionner |
| R3.5 — Distinction protéine / ARNm | `RNA_PREF_ORDER` privilégie `_rna` | ✅ Correct |
| R3.6 — Re-cadrage GSE23117 | Section 3.8 : "insufficiently powered" | ✅ Honnête |
| R3.7 — Enrichissement KEGG/Reactome | 4 voies canoniques avec adj-p < 1e-26 | ✅ Spectaculaire (mais voir §3.2) |
| R3.8 — Discussion asymétrie up/down | Section 4.6 | ⚠ Un peu rapide — voir §3.3 |

---

## 3. Points qui restent à clarifier

### 3.1 Discordance p-value (significatif) versus AUROC (faible) sur GSE51092

Dans la Table 2, GSE51092 a la **p-value la plus basse** (0.003) mais l'**AUROC le plus faible** (0.57). Cette discordance n'est pas commentée dans le manuscrit. Mécaniquement :

- La p-value mesure si la Hamming observée est plus basse que l'on s'attendrait sous direction aléatoire des DEGs (test d'enrichissement par score moyen).
- L'AUROC mesure la capacité des fréquences d'activation cross-attracteur à séparer les up-DEGs des down-DEGs (test d'ordonnancement).

GSE51092 a **n = 93 paires** et un fort biais up vs down (le manuscrit ne donne pas la décomposition exacte mais on le voit dans les fichiers). Un fort biais up/down peut donner une p-value très basse même avec un classifieur faible (la prédiction "tout est 1" suffit à égaler le biais), tandis que l'AUROC reste bas parce qu'il pénalise l'absence de discrimination *entre* up et down.

**Demande :** ajouter dans la Section 3.3 (ou en note de Table 2) un paragraphe interprétant la discordance p-value vs AUROC pour GSE51092, en pointant le biais directionnel des DEGs comme explication probable. Si l'auteur ne veut pas s'engager sur l'interprétation, au minimum reporter le ratio up/down par cohorte dans une colonne supplémentaire de Table 2.

### 3.2 L'enrichissement KEGG/Reactome de IFN-stim A1 — résultat attendu ?

Les p-values ajustées de l'ordre de 1e-26 à 1e-86 sont *énormes*. Avant de les saluer comme une validation, il faut comprendre leur origine :

- IFN-stim A1 active 133 HGNC symbols dans le set d'entrée Enrichr.
- Parmi ces 133, combien sont des ISGs *ajoutés par la correction HDAC3 = 1, KPNB1 = 1* ?
- Le différentiel "active sous v2 mais pas v1" est probablement la majeure partie du signal Enrichr.

Si oui, l'enrichissement IFN est essentiellement une *propriété mathématique* de la correction : on a forcé le pathway IFN à s'activer (HDAC3 et KPNB1 sont des nœuds en aval du fix), donc il est attendu d'enrichir les pathways IFN. Ce n'est pas une mauvaise chose — c'est un *contrôle de cohérence interne* — mais ce n'est pas une *prédiction indépendante*.

**Demande :** comparer l'enrichissement v1 vs v2 (passer le set d'actifs v1 IFN-stim FP1 dans Enrichr) et reporter le différentiel. Si v1 enrichissait déjà JAK-STAT (via STAT1 = 1 mais ISGs = 0), alors le delta v2 = ISG cluster + leur cibles. Si v1 n'enrichissait rien, alors le succès v2 est en grande partie tautologique. Cette analyse différentielle clarifie ce que la correction "ajoute" et ce qu'elle "rend testable".

### 3.3 Asymétrie sensibilité-spécificité — base-rate effect ?

L'IFN-stim A1 reaches sensitivity ~0.70 et spécificité ~0.85 (PRECISESADS) ou ~1.00 (UKPSSR). Une spécificité de 1.00 est suspecte. Examinons le détail Table 3 (UKPSSR IFN A1) : TP=16, TN=5, FP=0, FN=7. Spécificité = 5 / (5 + 0) = 1.00. Mais TN = 5 *seulement* sur 28 paires, parce que UKPSSR a très peu de DEGs down dans son overlay. La spécificité = 1.00 signifie "le modèle ne prédit aucun DEG down comme actif" — ce qui peut simplement traduire le fait que la majorité des nœuds du modèle sont à 0 par défaut, pas un signal prédictif.

L'auteur reconnaît cette asymétrie en Section 4.6 mais reste vague ("up-DEGs are well captured"). La discussion mériterait :

- Le **PPV** plutôt que la spécificité comme métrique principale (PPV = 1.00 sur UKPSSR signifie "tous les nœuds prédits actifs sont en effet up-DEGs" ; c'est le bon claim).
- Une comparaison à un baseline trivial : **modèle "tout actif"** (sensibilité 1.0, spécificité 0.0) et **modèle "tout inactif"** (sensibilité 0.0, spécificité 1.0). Reporter la balanced accuracy de ces deux baselines pour montrer que IFN-stim A1 (BA = 0.85 sur UKPSSR) bat les deux extrêmes.

**Demande :** ajouter dans Section 3.3 ou en SI la comparaison aux deux baselines triviaux. C'est une demi-page mais cela répond définitivement à la question "le signal est-il un effet de base-rate ?".

### 3.4 Bootstrap ou IC sur la Hamming observée

Comme le relecteur 1, je trouve que reporter l'IC bootstrap sur les Hamming observées (resampling des 91 paires de PRECISESADS, 28 de UKPSSR, etc., avec remplacement) compléterait utilement le test contre null. C'est trivial à implémenter (10–20 lignes Python, < 30 secondes pour 1000 bootstrap samples).

**Demande :** ajouter une colonne `hamming_95CI` à Table 2, calculée par bootstrap percentile.

### 3.5 R3.4 (sensibilité aux seuils DEG) — point réellement non traitable ?

L'auteur dit que les overlays SjD Map sont catégoriques (couleur = up / down) et qu'aucun seuil DEG n'est applicable. C'est correct pour les overlays de Silva-Saffar. Mais :

- Pour PRECISESADS, les statistiques de DEG (logFC, p-value) sont publiées (Lessard 2013) et peuvent être recalculées.
- L'analyse de sensibilité aux seuils logFC ∈ {0.5, 1.0, 1.5, 2.0} ou aux seuils p-adjusted ∈ {0.05, 0.01, 0.001} testerait si la corrélation observée est robuste à des restrictions des DEGs.

Cela peut être hors-scope révision majeure. À discuter explicitement comme limitation : "DEG list robustness to threshold variation could not be tested because the SjD Map provides categorical overlays only."

---

## 4. Points secondaires

### 4.1 Section 4.6 (asymétrie up/down) à étoffer

Le paragraphe actuel attribue l'asymétrie à la "curatorial focus on activating cascades". C'est cohérent mais légèrement post-hoc. Il y a une raison plus structurelle : la SjD Map a 645 arcs positifs et 47 arcs négatifs (ratio 14:1), donc les chemins d'activation dominent. Cette caractéristique *topologique* devrait être mentionnée explicitement.

### 4.2 Manque : test sur un attracteur "négatif"

Pour calibrer le succès de IFN-stim A1, il serait élégant de montrer que le test échoue *correctement* sur une cohorte qui n'a pas de signature IFN-high. Existe-t-il une cohorte SLE / RA / autre auto-immune où l'on s'attend à un Hamming non significatif vs IFN-stim A1 ? Si oui, l'inclure comme contrôle négatif renforcerait la spécificité du résultat.

C'est de la suggestion, pas une exigence.

---

## 5. Points positifs à conserver

- **`hgnc_to_bnet.csv` avec annotation `kind`** : structuration solide qui sera réutilisable par d'autres travaux sur la SjD Map.
- **Convention `_rna` first** : exactement le bon choix méthodologique pour comparer DEG vs nodes.
- **Null model = permutation des directions, pas des paires** : préserve la cardinalité des mappings, évite les artefacts de re-mapping. Choix techniquement correct.
- **`results/phase7/null_model_distribution.png`** : la figure (panneaux par cohorte) est lisible et donne au lecteur la distribution réelle, pas juste un scalar p-value.
- **GSE23117 retiré du corps positif** (Section 3.8) : démarche scientifique honnête, à conserver telle quelle.

---

## 6. Recommandation

**Accept after minor revisions.** Les demandes principales (3.1 discordance p/AUROC GSE51092, 3.2 enrichissement v1 vs v2 différentiel, 3.3 baselines triviaux, 3.4 IC bootstrap) sont *toutes* implémentables en quelques heures de coding et environ 1 page de prose ajoutée à la Section 3.3 / 4.6.

Estimation délai révision : 1 semaine.
