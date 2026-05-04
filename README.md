# SjD-BoolAttractors

**Identification et caractérisation des attracteurs du réseau booléen dérivé de la Sjögren's Disease Map (SjD Map) — fondations pour une analyse multi-échelle de la physiopathologie et des cibles thérapeutiques**

---

## 1. Contexte

La Sjögren's Disease Map (Silva-Saffar et al., *npj Systems Biology and Applications*, 2026) est la première carte d'interactions moléculaires (MIM) dédiée à la maladie de Sjögren. Elle intègre 829 entités moléculaires reliées par 598 interactions, construites à partir de l'analyse différentielle de trois cohortes transcriptomiques (GSE51092, UKPSSR, PRECISESADS), de l'enrichissement de pathways (KEGG, Reactome, WikiPathways) et d'une curation manuelle de la littérature (216 références PubMed). La carte est librement accessible via la plateforme MINERVA (https://sjdmap.elixir-luxembourg.org/) et son dépôt GitLab (https://gitlab.com/genhotel/TheSjDMap).

La carte se termine sur **14 phénotypes terminaux** représentant les "cell-fate decisions" :
MHC Class I Activation, MHC Class II Activation, T Cell Activation/Differentiation, B Cell Activation/Survival, Cell Proliferation/Survival, Inflammation, Chemotaxis/Infiltration, Angiogenesis, Lymphoid Organ Development, Apoptosis, Regulated Necrosis, Matrix Degradation, Fibrosis, Phagocytosis.

L'analyse topologique réalisée par les auteurs identifie cinq nœuds-hubs stables : Inflammation, STAT1 homodimer, STAT1/STAT2/IRF9, RELA/NFKB1, Chemotaxis/Infiltration — soulignant le rôle pivot des voies JAK-STAT et NF-κB.

Cependant, la carte reste à ce jour une représentation **statique** : elle décrit les interactions sans permettre de simuler la dynamique du système, d'identifier les états stables (attracteurs) auxquels il converge, ni de prédire l'effet de perturbations (traitements, mutations, signaux) sur les phénotypes finaux.

## 2. Objectif du projet

Convertir la SjD Map en un **réseau booléen exécutable** et caractériser ses attracteurs afin de :

1. Identifier les états stables du système et les associer aux phénotypes biologiques observés cliniquement (sain, IFN-high, B-cell hyperactivé, pré-lymphomateux, etc.).
2. Établir une correspondance entre attracteurs *in silico* et signatures transcriptomiques *in vivo* issues des cohortes PRECISESADS, UKPSSR, GSE51092 et ASSESS.
3. Caractériser les bassins d'attraction et identifier les nœuds critiques dont la perturbation reroute le système vers un attracteur "homéostatique".
4. Fournir un cadre validé et reproductible servant de fondation à des extensions ultérieures (analyse de combinaisons thérapeutiques, méthodes quantiques, médecine de précision).

## 3. Question scientifique principale

> Les attracteurs du modèle booléen dérivé de la SjD Map correspondent-ils aux phénotypes cliniques et aux clusters moléculaires observés chez les patients atteints de Sjögren ? Quels sont les nœuds dont la perturbation contrôle le mieux la transition entre attracteurs pathologiques et homéostatiques ?

## 4. Hypothèses de travail

- **H1.** Le réseau booléen dérivé de la SjD Map admet un nombre fini d'attracteurs (de l'ordre de quelques unités à quelques dizaines), interprétables comme phénotypes biologiques distincts.
- **H2.** Au moins un attracteur est compatible avec la signature IFN-high décrite dans Soret et al. (2021) et Trutschel et al. (2022).
- **H3.** Les nœuds-hubs identifiés topologiquement par les auteurs (STAT1, NF-κB, etc.) sont également des points de contrôle dynamique au sens des stable motifs et des minimum intervention sets.
- **H4.** Des cibles thérapeutiques actuellement testées en essais cliniques (déjà identifiées dans la SjD Map via l'overlay DrugBank/OpenTargets) figurent parmi les nœuds de contrôle minimaux pour rerouter le système hors d'un attracteur pathologique.

## 5. Méthodologie

### 5.1 Conversion MIM → réseau booléen

- Récupération de la SjD Map au format SBML/SBGN-PD depuis le dépôt GitLab et la plateforme MINERVA.
- Conversion automatisée via **CaSQ** (Aghamiri et al., 2020) — outil développé par la même équipe de recherche que la SjD Map et déjà mentionné dans l'article. Output : un modèle au format SBML-qual exécutable.
- Vérification de cohérence de la version réduite (412 nœuds, 692 arêtes) annoncée dans le papier.

### 5.2 Identification des attracteurs

Plusieurs solveurs complémentaires seront comparés :

- **bioLQM / Colomoto** (Naldi et al.) — calcul exact d'attracteurs via décision diagrammes binaires (BDDs).
- **PyBoolNet** (Klarner et al.) — model-checking et analyse de stable motifs.
- **MaBoSS** (Stoll et al.) — simulation stochastique continue-en-temps pour estimer les probabilités d'attracteurs et la dynamique transitoire.
- **pystablemotifs** (Rozum et al.) — pour l'identification des stable motifs et des intervention sets minimaux.

Schémas de mise à jour évalués : synchrone, asynchrone, et stochastique (MaBoSS).

### 5.3 Annotation biologique des attracteurs

Pour chaque attracteur identifié, caractériser :
- Le profil d'activation des 14 phénotypes terminaux.
- Le profil d'activation des hubs (STAT1, NFKB, JAK-STAT, voies BAFF/APRIL).
- La distance Hamming aux signatures transcriptomiques moyennes des cohortes (PRECISESADS, UKPSSR, GSE51092).
- La correspondance avec les sous-groupes moléculaires de Soret et al. (2021).

### 5.4 Analyse de contrôle

- Identification des **stable motifs** et calcul des **minimum intervention sets** (MIS) pour piloter le système d'un attracteur "inflammatoire" vers un attracteur "homéostatique".
- Comparaison avec les hubs topologiques pour évaluer si centralité dynamique et centralité structurelle convergent.
- Confrontation des MIS aux cibles thérapeutiques connues via l'overlay OpenTargets/DrugBank fourni par les auteurs.

### 5.5 Validation

- **Validation interne** : simulations de perturbations correspondant à des traitements en essais cliniques (filgotinib → JAK3, tirabrutinib → BTK, deucravacitinib → TYK2, ianalumab → BAFF-R) et vérification que le système est dévié vers des attracteurs cohérents avec les résultats cliniques connus.
- **Validation externe** : projection des DEGs ASSESS lymphoma (overlay déjà disponible dans la carte) et vérification que les attracteurs reproduisent l'upregulation observée de BTK et TNFSF13 (APRIL) — résultat attendu d'après Duret et al. (2023).

## 6. Roadmap

### Phase 0 — Mise en place (semaines 1-2)
- Mise en place du dépôt Git, environnement Conda/Docker reproductible.
- Récupération de la SjD Map (SBML/SBGN-PD) depuis Zenodo (DOI 10.5281/zenodo.17585308) et GitLab.
- Vérification de l'intégrité du fichier et reproduction des statistiques topologiques publiées (Cytoscape NetworkAnalyzer).

### Phase 1 — Conversion et validation structurelle (semaines 3-5)
- Application de CaSQ pour obtenir le modèle SBML-qual.
- Comparaison node-à-node et arête-à-arête avec la version réduite décrite dans le papier (412 nœuds, 692 arêtes).
- Audit manuel des nœuds critiques (hubs, phénotypes, complexes) pour s'assurer que la sémantique biologique est préservée.
- **Livrable** : modèle booléen versionné + rapport d'audit structurel.

### Phase 2 — Identification des attracteurs (semaines 6-9)
- Calcul des attracteurs en synchrone et asynchrone via bioLQM et PyBoolNet.
- Simulations stochastiques avec MaBoSS pour estimer les probabilités d'atteinte des attracteurs depuis différents états initiaux.
- Comparaison croisée des résultats entre solveurs.
- **Livrable** : catalogue annoté des attracteurs (CSV + visualisations).

### Phase 3 — Annotation biologique (semaines 10-13)
- Caractérisation de chaque attracteur en termes de profils phénotypiques et d'expression.
- Confrontation aux signatures transcriptomiques des cohortes (overlays PRECISESADS, UKPSSR, GSE51092 déjà fournis avec la carte).
- Confrontation aux clusters moléculaires définis par Soret et al. (2021) sur la cohorte PRECISESADS.
- **Livrable** : table de correspondance attracteurs ↔ phénotypes cliniques + analyse statistique.

### Phase 4 — Analyse de contrôle (semaines 14-17)
- Calcul des stable motifs avec pystablemotifs.
- Identification des minimum intervention sets pour les transitions phénotypiques d'intérêt (notamment vers/depuis l'attracteur "lymphome").
- Comparaison avec les hubs topologiques et les cibles thérapeutiques connues.
- **Livrable** : liste priorisée de cibles candidates avec justification mécaniste.

### Phase 5 — Validation et étude de cas thérapeutique (semaines 18-21)
- Simulation des traitements connus (filgotinib, tirabrutinib, deucravacitinib, iscalimab, ianalumab) et confrontation aux résultats des essais cliniques.
- Étude de cas approfondie : prédiction de l'effet d'un knock-out BTK et d'un knock-out APRIL, comparaison aux DEGs lymphoma de la cohorte ASSESS.
- **Livrable** : rapport de validation et figures principales du papier.

### Phase 6 — Rédaction et soumission (semaines 22-26)
- Rédaction du manuscrit.
- Préparation du dépôt de code et des données dérivées (Zenodo + GitLab).
- Soumission ciblée sur *npj Systems Biology and Applications* (continuité naturelle avec le papier original) ou *Bioinformatics* (si l'angle outil prédomine).

## 7. Livrables principaux

1. **Modèle booléen** versionné de la SjD Map au format SBML-qual, exécutable et annoté.
2. **Catalogue des attracteurs** avec annotation biologique et correspondance aux phénotypes cliniques.
3. **Liste de cibles thérapeutiques** priorisées via analyse de contrôle, avec confrontation aux essais cliniques en cours.
4. **Pipeline reproductible** (Snakemake ou Nextflow) permettant de rejouer l'ensemble des analyses depuis le SBML brut jusqu'aux figures finales.
5. **Manuscrit** soumis à un journal du domaine.

## 8. Cibles éditoriales envisagées

| Journal | Angle | Probabilité d'acceptation |
|---|---|---|
| npj Systems Biology and Applications | Continuité directe avec la SjD Map originale | Élevée si validation biologique solide |
| Bioinformatics (OUP) | Si l'accent est mis sur le pipeline outil | Élevée si reproductibilité exemplaire |
| PLOS Computational Biology | Méthodologie en biologie des systèmes | Moyenne-élevée |
| Frontiers in Systems Biology | Application thématique | Élevée mais visibilité moindre |

## 9. Risques et mitigations

| Risque | Probabilité | Mitigation |
|---|---|---|
| Le réseau réduit est trop grand pour un calcul exact d'attracteurs | Moyenne | Décomposition modulaire ; usage de MaBoSS pour échantillonnage stochastique ; analyse par sous-réseaux centrés sur les phénotypes cibles |
| Les attracteurs ne correspondent pas clairement aux phénotypes cliniques | Moyenne | Recalibrage des règles logiques par expertise clinique (collaboration avec auteurs originaux à envisager) ; documentation honnête des écarts |
| Multiplicité d'attracteurs ininterprétables | Faible-moyenne | Filtrage par pertinence biologique ; agrégation par classes d'équivalence phénotypique |
| Sensibilité des résultats au schéma de mise à jour | Élevée | Comparaison systématique synchrone/asynchrone/stochastique ; rapport transparent |

## 10. Extensions futures (out of scope ici)

- **Étape 2** : exploration d'algorithmes quantum walks et QAOA pour l'identification d'attracteurs et de transitions, en utilisant le pipeline classique de l'étape 1 comme référence (benchmark).
- **Étape 3** : optimisation combinatoire de combinaisons de traitements pour cibler des sous-groupes moléculaires de patients.
- Intégration des signatures spécifiques au tissu salivaire (GSE23117) pour une analyse multi-compartiments (sang vs glandes).

## 11. Dépendances logicielles principales

```
- Python ≥ 3.10
- CaSQ (https://github.com/sysbio-curie/CaSQ)
- bioLQM (https://github.com/colomoto/bioLQM)
- PyBoolNet (https://github.com/hklarner/PyBoolNet)
- MaBoSS (https://github.com/sysbio-curie/MaBoSS-env-2.0)
- pystablemotifs (https://github.com/jcrozum/pystablemotifs)
- Colomoto Docker notebook (https://github.com/colomoto/colomoto-docker)
- Cytoscape ≥ 3.10 (validation topologique)
- R ≥ 4.3 (limma pour la confrontation aux DEGs)
```

## 12. Références principales

- Silva-Saffar SE, Mariette X, Gottenberg JE, et al. The SjD Map: an interactive pathway tour into Sjögren's disease signalling mechanisms. *npj Syst Biol Appl*. 2026.
- Aghamiri SS, Singh V, Naldi A, Helikar T, Soliman S, Niarakis A. Automated inference of Boolean models from molecular interaction maps using CaSQ. *Bioinformatics*. 2020;36(16):4473-4482.
- Soret P, Le Dantec C, Desvaux E, et al. A new molecular classification to drive precision treatment strategies in primary Sjögren's syndrome. *Nat Commun*. 2021;12(1):3523.
- Duret PM, Schleiss C, Kawka L, et al. Association Between Bruton's Tyrosine Kinase Gene Overexpression and Risk of Lymphoma in Primary Sjögren's Syndrome. *Arthritis Rheumatol*. 2023;75(10):1798-1811.
- Zañudo JGT, Albert R. Cell fate reprogramming by control of intracellular network dynamics. *PLoS Comput Biol*. 2015;11(4):e1004193.
- Klarner H, Streck A, Siebert H. PyBoolNet: a python package for the generation, analysis and visualization of boolean networks. *Bioinformatics*. 2017;33(5):770-772.

## 13. Licence et reproductibilité

- Code : MIT.
- Données dérivées et figures : CC-BY 4.0 (cohérent avec la licence du papier original et de la SjD Map).
- Tous les scripts, configurations, et données intermédiaires seront déposés sur Zenodo avec DOI permanent au moment de la soumission.

---

*Projet maintenu par : [à compléter]. Contact : [à compléter].*
