# ROADMAP — SjD-BoolAttractors

**Feuille de route détaillée pour la conversion de la SjD Map en réseau booléen et la caractérisation de ses attracteurs.**

Ce document décompose chaque phase du projet en tâches élémentaires, livrables, critères de validation et dépendances. Il est destiné à servir de référence opérationnelle au quotidien et de support de revue d'avancement.

**Durée totale estimée : 26 semaines (~6 mois)**

---

## Vue d'ensemble

| Phase | Intitulé | Semaines | Statut |
|---|---|---|---|
| 0 | Mise en place | S1–S2 | À faire |
| 1 | Conversion et validation structurelle | S3–S5 | À faire |
| 2 | Identification des attracteurs | S6–S9 | À faire |
| 3 | Annotation biologique | S10–S13 | À faire |
| 4 | Analyse de contrôle | S14–S17 | À faire |
| 5 | Validation et étude de cas thérapeutique | S18–S21 | À faire |
| 6 | Rédaction et soumission | S22–S26 | À faire |

**Chemin critique** : Phase 1 → Phase 2 → Phase 3 → Phase 4. Les phases 5 et 6 dépendent toutes des résultats consolidés des phases 2–4.

---

## Phase 0 — Mise en place (semaines 1–2)

### Objectif
Disposer d'un environnement de travail reproductible et avoir vérifié l'intégrité des données sources (SjD Map) avant toute analyse.

### Étapes détaillées

**0.1 Initialisation du dépôt et structure projet**
- Définir l'arborescence cible : `data/raw/`, `data/processed/`, `models/`, `notebooks/`, `src/`, `results/`, `figures/`, `docs/`, `tests/`.
- Créer un `.gitignore` adapté (exclure `.venv/`, `data/raw/`, fichiers volumineux > 50 Mo, fichiers temporaires des solveurs).
- Initialiser un `pyproject.toml` (ou `requirements.txt`) listant les dépendances de la section 11 du README.
- Mettre en place un `LICENSE` (MIT pour le code) et un `CITATION.cff`.

**0.2 Environnement reproductible**
- Construire un environnement Conda `environment.yml` couvrant Python ≥ 3.10, CaSQ, bioLQM, PyBoolNet, MaBoSS, pystablemotifs.
- Évaluer l'usage du conteneur **Colomoto Docker notebook** comme alternative officielle (déjà packagée par les auteurs des outils).
- Documenter dans `docs/setup.md` les étapes d'installation sur Linux/macOS, ainsi que les versions exactes utilisées (lockfile).

**0.3 Récupération des données sources**
- Télécharger l'archive Zenodo (DOI 10.5281/zenodo.17585308) et stocker sous `data/raw/zenodo_<date>/`.
- Cloner le dépôt GitLab `genhotel/TheSjDMap` (référence figée par commit hash).
- Récupérer manuellement la version réduite (412 nœuds, 692 arêtes) si fournie séparément.
- Vérifier les checksums SHA-256 et les consigner dans `data/raw/CHECKSUMS.txt`.

**0.4 Reproduction des statistiques topologiques publiées**
- Importer le SBML/SBGN-PD dans Cytoscape ≥ 3.10.
- Lancer NetworkAnalyzer et confirmer : 829 entités, 598 interactions (carte complète) ; 412 nœuds, 692 arêtes (version réduite).
- Comparer la distribution des degrés et identifier les hubs ; vérifier que STAT1, NF-κB, STAT1/STAT2/IRF9, Inflammation, Chemotaxis ressortent comme top-5.
- Documenter tout écart dans `docs/audit_topologique.md`.

### Livrables
- Dépôt Git initialisé avec arborescence et licence.
- `environment.yml` (ou Dockerfile) gelé.
- Données SjD Map versionnées avec checksums.
- Rapport de reproduction des statistiques topologiques.

### Critères de validation
- L'environnement s'installe sans intervention manuelle sur une machine vierge.
- Les statistiques topologiques publiées sont retrouvées à ±1 %.
- Le dépôt passe une revue interne (lisibilité du README, scripts exécutables).

### Dépendances
Aucune (phase initiale).

---

## Phase 1 — Conversion et validation structurelle (semaines 3–5)

### Objectif
Obtenir un modèle SBML-qual exécutable, fidèle à la SjD Map réduite, et validé sur sa sémantique biologique.

### Étapes détaillées

**1.1 Conversion automatisée via CaSQ**
- Étudier la documentation CaSQ et les options pertinentes (gestion des complexes, des phénotypes, des modifications post-traductionnelles).
- Lancer la conversion sur la SjD Map complète et sur la version réduite.
- Sauvegarder les fichiers d'entrée et de sortie sous `models/sbmlqual/v1/`.
- Capturer les logs de conversion dans `models/sbmlqual/v1/conversion.log`.

**1.2 Validation structurelle automatique**
- Écrire un script `src/validation/structural_check.py` qui :
  - Charge le SBML-qual et compte nœuds/arêtes.
  - Compare ces compteurs aux valeurs attendues (412/692).
  - Liste les nœuds présents/absents par rapport à la version originale.
  - Génère un rapport CSV sous `results/phase1/structural_diff.csv`.

**1.3 Audit manuel des nœuds critiques**
- Établir une checklist manuelle ciblant :
  - Les 5 hubs topologiques (STAT1, NFKB1/RELA, STAT1/STAT2/IRF9, Inflammation, Chemotaxis).
  - Les 14 phénotypes terminaux.
  - Les complexes multi-protéines (vérification que CaSQ a bien introduit la conjonction logique).
- Pour chaque nœud, vérifier ses régulateurs entrants et la fonction logique inférée par CaSQ.
- Documenter les corrections manuelles éventuelles dans `docs/audit_logique.md` avec justification (référence PubMed quand pertinent).

**1.4 Versionnage du modèle**
- Tag Git `model-v1.0` pointant le SBML-qual validé.
- Snapshot Zenodo (sandbox) pour disposer d'un DOI temporaire utilisable dans les phases suivantes.

### Livrables
- Modèle SBML-qual versionné (`models/sbmlqual/v1/sjd_map_reduced.sbml`).
- Rapport d'audit structurel (`docs/audit_topologique.md`).
- Rapport d'audit logique (`docs/audit_logique.md`).

### Critères de validation
- Écart structurel < 5 % en nœuds et arêtes (et écart documenté quand non négligeable).
- Audit manuel signé sur les 5 hubs et 14 phénotypes.
- Le SBML-qual se charge sans erreur dans bioLQM, PyBoolNet et MaBoSS.

### Dépendances
- Phase 0 (données et environnement disponibles).

### Risques spécifiques
- **Divergence importante carte→qual** : prévoir 3–5 jours buffer pour corrections manuelles.
- **Complexes mal interprétés par CaSQ** : tester explicitement quelques complexes connus (ex. STAT1/STAT2/IRF9) en simulation manuelle.

---

## Phase 2 — Identification des attracteurs (semaines 6–9)

### Objectif
Cataloguer l'ensemble des attracteurs du modèle sous différents schémas de mise à jour, avec quantification de leurs bassins.

### Étapes détaillées

**2.1 Calcul exact via bioLQM (synchrone)**
- Configurer bioLQM en ligne de commande ou via API Python.
- Lancer le calcul d'attracteurs en mode synchrone.
- Sauvegarder la sortie sous `results/phase2/attractors_biolqm_sync.json`.
- Mesurer les ressources (RAM, temps) — point d'attention pour anticiper les limites de calcul exact.

**2.2 Calcul exact via PyBoolNet (asynchrone)**
- Charger le SBML-qual dans PyBoolNet.
- Calculer les attracteurs en mise à jour asynchrone (model-checking sur les SCC terminaux).
- Identifier les **stable states** vs. **cycliques** ; sauvegarder sous `results/phase2/attractors_pyboolnet_async.json`.

**2.3 Simulation stochastique via MaBoSS**
- Préparer le fichier `.bnd` (réseau) et `.cfg` (conditions initiales, taux) à partir du SBML-qual (script de conversion à écrire dans `src/conversion/sbmlqual_to_maboss.py`).
- Lancer N = 10 000 trajectoires depuis 3 conditions initiales représentatives :
  - "Naïf homéostatique" (tous les ligands inflammatoires off).
  - "IFN-stimulé" (IFN-α, IFN-γ on).
  - "BCR-stimulé" (BAFF, BCR signal on).
- Estimer les probabilités d'atteinte de chaque attracteur ; sauvegarder sous `results/phase2/maboss_probas.csv`.

**2.4 Analyse comparée des solveurs**
- Écrire `notebooks/phase2/compare_solvers.ipynb` qui :
  - Aligne les attracteurs des trois solveurs (table de correspondance basée sur les états des hubs).
  - Quantifie la concordance (matrice de Jaccard sur les états des nœuds-clés).
  - Discute les écarts (typiquement, oscillations vues uniquement en asynchrone).

**2.5 Catalogue annoté des attracteurs**
- Construire un tableau maître `results/phase2/attractor_catalog.csv` avec colonnes :
  `id, type (point/cycle), taille, hubs_actifs, phenotypes_actifs, probabilite_MaBoSS, source_solveur`.
- Visualiser la distribution sous forme de heatmap (attracteurs × nœuds) dans `figures/phase2/heatmap_attractors.png`.

### Livrables
- Catalogue annoté des attracteurs (CSV + heatmap).
- Notebook de comparaison inter-solveurs.
- Logs de performance des calculs.

### Critères de validation
- Au moins deux solveurs concordent sur les attracteurs ponctuels majeurs.
- Le nombre d'attracteurs est interprétable (ordre de grandeur attendu : 5–50 d'après H1 du README).
- Les probabilités MaBoSS somment à 1 par condition initiale.

### Dépendances
- Phase 1 (modèle SBML-qual validé).

### Risques spécifiques
- **Explosion combinatoire en synchrone exact** : si bioLQM ne finit pas en < 24 h, basculer sur décomposition modulaire (sous-réseaux centrés sur phénotypes).
- **Attracteurs cycliques massifs** : agréger par classes d'équivalence sur les nœuds-clés plutôt que d'énumérer.

---

## Phase 3 — Annotation biologique (semaines 10–13)

### Objectif
Établir une correspondance interprétable entre attracteurs *in silico* et phénotypes/clusters cliniques observés.

### Étapes détaillées

**3.1 Profils phénotypiques des attracteurs**
- Pour chaque attracteur, extraire l'état des 14 phénotypes terminaux.
- Définir un score par phénotype (binaire pour attracteurs ponctuels ; fréquence pour cycliques).
- Visualiser sous forme de barplot empilé `figures/phase3/phenotype_profile.png`.

**3.2 Profils des hubs et voies de signalisation**
- Caractériser l'état des voies JAK-STAT, NF-κB, BAFF/APRIL, BCR, TLR pour chaque attracteur.
- Construire des signatures synthétiques par attracteur (vecteur d'activation des sous-modules).

**3.3 Confrontation aux signatures transcriptomiques**
- Récupérer les overlays de DEGs déjà fournis avec la SjD Map (PRECISESADS, UKPSSR, GSE51092).
- Pour chaque cohorte et chaque attracteur, calculer la **distance de Hamming** entre l'état des nœuds simulés et le signe des DEGs (up=1, down=0, NS=NA).
- Identifier le ou les attracteurs minimisant la distance par cohorte.
- Sauvegarder sous `results/phase3/attractor_to_cohort_distance.csv`.

**3.4 Confrontation aux clusters de Soret et al. (2021)**
- Récupérer les signatures des 4 clusters moléculaires (C1–C4) définis sur PRECISESADS.
- Mettre en correspondance attracteurs ↔ clusters via la même métrique de Hamming, complétée par une similarité cosinus sur les voies-clés.
- Tester l'hypothèse H2 : au moins un attracteur reproduit la signature IFN-high.

**3.5 Statistiques de robustesse**
- Bootstrap (n=1000) sur les jeux de DEGs pour estimer la stabilité des associations attracteur↔cohorte.
- Test de permutation pour évaluer la significativité par rapport à un appariement aléatoire.

### Livrables
- Table de correspondance attracteurs ↔ phénotypes cliniques (`results/phase3/mapping.csv`).
- Figure principale candidate pour le manuscrit (heatmap attracteurs × cohortes/clusters).
- Rapport statistique sur la robustesse des associations.

### Critères de validation
- Au moins un attracteur associé de manière statistiquement significative (p < 0,05 corrigé) à la signature IFN-high.
- Cohérence entre les associations sur PRECISESADS et UKPSSR (réplication cross-cohorte).

### Dépendances
- Phase 2 (catalogue d'attracteurs).
- Disponibilité des overlays DEGs (vérifiée en Phase 0).

### Risques spécifiques
- **Faible recouvrement nœuds-modèle / gènes-DEG** : si < 50 % des nœuds modèle ont un mapping gène, restreindre l'analyse aux nœuds mappables et le justifier.
- **Aucun attracteur compatible IFN-high** : revisiter les règles logiques en Phase 1 (boucle de correction).

---

## Phase 4 — Analyse de contrôle (semaines 14–17)

### Objectif
Identifier les nœuds dont la perturbation reroute le système d'un attracteur pathologique vers un attracteur homéostatique, et confronter ces cibles aux thérapies existantes.

### Étapes détaillées

**4.1 Calcul des stable motifs**
- Utiliser pystablemotifs sur le SBML-qual.
- Énumérer les stable motifs et la **succession diagram** correspondante.
- Visualiser dans `figures/phase4/succession_diagram.svg`.

**4.2 Minimum Intervention Sets (MIS)**
- Définir les paires d'attracteurs d'intérêt (typiquement : attracteur "inflammatoire/IFN-high" → attracteur "homéostatique").
- Calculer les MIS pour chaque paire via pystablemotifs (algorithme de Zañudo & Albert 2015, déjà cité dans le README).
- Sauvegarder sous `results/phase4/mis_<source>_<target>.json`.

**4.3 Comparaison centralité dynamique vs. structurelle**
- Croiser les nœuds présents dans les MIS avec les hubs topologiques de la Phase 0.
- Quantifier le recouvrement (test exact de Fisher).
- Tester H3 : les hubs sont-ils sur-représentés dans les MIS ?

**4.4 Confrontation aux cibles thérapeutiques connues**
- Récupérer l'overlay DrugBank/OpenTargets fourni avec la SjD Map.
- Pour chaque nœud des MIS, lister les drogues approuvées ou en essai (avec phase clinique).
- Construire la liste priorisée `results/phase4/druggable_targets.csv`.
- Tester H4 : les cibles d'essais cliniques actuels (filgotinib, tirabrutinib, deucravacitinib, ianalumab, iscalimab) figurent-elles parmi les MIS ?

### Livrables
- Liste priorisée de cibles candidates avec justification mécaniste.
- Diagramme de succession.
- Rapport de recouvrement hubs/MIS/cibles thérapeutiques.

### Critères de validation
- Au moins 3 MIS distincts identifiés pour la transition pathologique → homéostatique.
- Au moins une des 5 cibles thérapeutiques en essai (BTK, JAK3, TYK2, BAFF-R, CD40) apparaît dans un MIS — sinon, écart à expliquer.

### Dépendances
- Phase 3 (attracteurs annotés "pathologique" vs. "homéostatique").

### Risques spécifiques
- **Coût computationnel des MIS** : restreindre au sous-réseau pertinent si nécessaire.
- **MIS triviaux dominés par phénotypes terminaux** : les exclure et focaliser sur nœuds intermédiaires actionnables.

---

## Phase 5 — Validation et étude de cas thérapeutique (semaines 18–21)

### Objectif
Vérifier que les prédictions du modèle sont cohérentes avec les résultats cliniques connus et avec des données externes (cohorte ASSESS).

### Étapes détaillées

**5.1 Simulation in silico des traitements en essais**
- Pour chaque traitement (filgotinib→JAK3, tirabrutinib→BTK, deucravacitinib→TYK2, ianalumab→BAFF-R, iscalimab→CD40) :
  - Implémenter un knock-out ou knock-down de la cible.
  - Recalculer les attracteurs (synchrone, asynchrone, stochastique).
  - Mesurer la déviation de la distribution d'attracteurs vs. baseline.
- Confronter les déviations aux résultats publiés des essais (réponse ou non, voies impactées).

**5.2 Étude de cas BTK / APRIL et lymphome**
- KO BTK : recalculer les attracteurs ; vérifier que les phénotypes B-cell hyperactivé / pré-lymphomateux sont supprimés.
- KO TNFSF13 (APRIL) : même analyse.
- Confronter à la cohorte ASSESS lymphoma (overlay disponible) — vérifier que les DEGs upregulés (BTK, TNFSF13 — Duret et al. 2023) sont effectivement actifs dans l'attracteur "lymphome" du modèle.

**5.3 Validation externe par cross-cohorte**
- Si le temps le permet, projeter une signature transcriptomique externe non utilisée en Phase 3 (par exemple GSE23117 si disponible) et tester si l'attracteur le plus proche est biologiquement cohérent.

**5.4 Préparation des figures principales du manuscrit**
- Figure 1 : pipeline méthodologique (carte → SBML-qual → attracteurs).
- Figure 2 : catalogue d'attracteurs et profils phénotypiques.
- Figure 3 : correspondance attracteurs ↔ cohortes/clusters.
- Figure 4 : MIS et cibles thérapeutiques.
- Figure 5 : étude de cas BTK/APRIL.

### Livrables
- Rapport de validation thérapeutique (`docs/validation_report.md`).
- Figures principales en version draft.
- Résultats bruts archivés sous `results/phase5/`.

### Critères de validation
- Concordance qualitative entre simulation et résultats cliniques pour ≥ 3 des 5 traitements testés.
- Reproduction in silico de l'upregulation BTK/APRIL dans l'attracteur "lymphome".

### Dépendances
- Phases 2, 3, 4 toutes complétées.

### Risques spécifiques
- **Discordance simulation/clinique** : documenter honnêtement et utiliser comme limite discutée dans le manuscrit (cf. section 9 du README).

---

## Phase 6 — Rédaction et soumission (semaines 22–26)

### Objectif
Produire un manuscrit publiable et un dépôt code/données pleinement reproductible.

### Étapes détaillées

**6.1 Rédaction du manuscrit**
- Plan IMRAD (Introduction, Méthodes, Résultats, Discussion).
- Sections inspirées du README : contexte SjD Map, conversion CaSQ, attracteurs, contrôle, validation thérapeutique.
- Utiliser un système de citations (BibTeX) ; cibler 50–80 références.
- Itérations co-auteurs internes ; envisager une relecture externe (collaboration avec auteurs SjD Map d'après section 9 du README).

**6.2 Pipeline reproductible**
- Encapsuler l'enchaînement Phase 1 → Phase 5 dans **Snakemake** ou **Nextflow**.
- Rule par phase (`rule phase1_convert`, `rule phase2_attractors`, etc.).
- Test end-to-end sur une machine vierge à partir du SBML brut.
- Inclure un `Makefile` de raccourcis usuels.

**6.3 Dépôt de données et code**
- Préparer l'archive Zenodo finale avec DOI permanent.
- Vérifier les licences (MIT pour le code, CC-BY 4.0 pour les données dérivées et figures).
- Mettre à jour le `CITATION.cff` et le README final.

**6.4 Stratégie de soumission**
- Cibler en priorité **npj Systems Biology and Applications** (continuité directe avec le papier original — section 8 du README).
- Préparer un cover letter mentionnant la continuité et les nouveautés (boolean dynamics, contrôle, validation thérapeutique).
- Plan B : *Bioinformatics* (si l'accent outil prédomine) ou *PLOS Computational Biology*.

### Livrables
- Manuscrit soumis.
- Pipeline Snakemake/Nextflow exécuté de bout en bout.
- DOI Zenodo final.
- Page projet GitLab/GitHub publique.

### Critères de validation
- Le pipeline tourne en une seule commande sur une machine vierge.
- Les figures du manuscrit sont reproductibles depuis le pipeline.
- Soumission effective avec accusé de réception du journal.

### Dépendances
- Phase 5 (résultats consolidés).

---

## Suivi et points de contrôle

### Réunions de jalon
- **Fin Phase 1** (S5) : Go/No-Go sur la qualité du modèle SBML-qual.
- **Fin Phase 2** (S9) : Go/No-Go sur la tractabilité computationnelle.
- **Fin Phase 3** (S13) : Go/No-Go sur la pertinence biologique des attracteurs.
- **Fin Phase 5** (S21) : Décision de soumission et choix du journal cible.

### Indicateurs de progression
- Couverture des nœuds-clés audités (phase 1).
- Nombre d'attracteurs catalogués (phase 2).
- Nombre d'associations attracteur↔cohorte significatives (phase 3).
- Nombre de MIS recouvrant des cibles thérapeutiques (phase 4).
- Nombre de traitements simulés cohérents avec la clinique (phase 5).

### Buffer et gestion du planning
- Chaque phase comprend une marge implicite (~20 %) en raison de l'incertitude des analyses biologiques.
- En cas de glissement supérieur à 2 semaines sur une phase, déclencher une revue de scope (par exemple, restreindre la validation à 3 traitements au lieu de 5).

---

*Document maintenu en parallèle du README.md. Mettre à jour les statuts de phase et les indicateurs au fur et à mesure de l'avancement.*
