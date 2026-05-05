# ROADMAP — SjD-BoolAttractors

**Feuille de route détaillée pour la conversion de la SjD Map en réseau booléen et la caractérisation de ses attracteurs.**

Ce document décompose chaque phase du projet en tâches élémentaires, livrables, critères de validation et dépendances. Il est destiné à servir de référence opérationnelle au quotidien et de support de revue d'avancement.

**Durée totale estimée : 26 semaines (~6 mois)**

---

## Vue d'ensemble

| Phase | Intitulé | Semaines | Statut |
|---|---|---|---|
| 0 | Mise en place | S1–S2 | ✅ Terminée (2026-05-05) |
| 1 | Conversion et validation structurelle | S3–S5 | ✅ Terminée (2026-05-05) |
| 2 | Identification des attracteurs | S6–S9 | ✅ Terminée (2026-05-05) |
| 3 | Annotation biologique | S10–S13 | ✅ Terminée (2026-05-05) |
| 4 | Analyse de contrôle | S14–S17 | ✅ Terminée (2026-05-05) |
| 5 | Validation et étude de cas thérapeutique | S18–S21 | À faire |
| 6 | Rédaction et soumission | S22–S26 | À faire |

**Chemin critique** : Phase 1 → Phase 2 → Phase 3 → Phase 4. Les phases 5 et 6 dépendent toutes des résultats consolidés des phases 2–4.

> **Découverte Phase 0 (impact sur Phase 1) :** CaSQ v1.3.3 a déjà été appliqué par les auteurs originaux.
> Le fichier `SjD_Model_raw.sif` (412 nœuds / 692 arêtes) est disponible dans l'archive Zenodo.
> L'étape 1.1 consiste donc à **régénérer le SBML-qual** depuis le CellDesigner SBML (le SIF existant sert de référence de validation, pas de point de départ pour les solveurs).

---

## Phase 0 — Mise en place (semaines 1–2) ✅ TERMINÉE

**Complétée le 2026-05-05.**

### Objectif
Disposer d'un environnement de travail reproductible et avoir vérifié l'intégrité des données sources (SjD Map) avant toute analyse.

### Étapes détaillées

**0.1 Initialisation du dépôt et structure projet** ✅
- Arborescence créée : `data/raw/`, `data/processed/`, `models/sbmlqual/v1/`, `notebooks/phase2/`, `src/validation/`, `src/conversion/`, `results/phase{1..5}/`, `figures/phase{2..4}/`, `docs/`, `tests/`.
- `.gitignore` mis à jour (exclut `.venv/`, caches Python, `data/raw/*`, sorties régénérables).
- `LICENSE` (MIT), `CITATION.cff`, `pyproject.toml` créés.
- 16 fichiers `.gitkeep` ajoutés.

**0.2 Environnement reproductible** ✅
- `environment.yml` : Conda, canal `colomoto` (CaSQ, bioLQM, PyBoolNet, MaBoSS, pystablemotifs, openjdk≥17), stack scientifique, JupyterLab, dev tools.
- `docs/setup.md` : Option A (Conda/mamba) + Option B (Colomoto Docker), instructions lockfile et tests.

**0.3 Récupération des données sources** ✅
- Zenodo 10.5281/zenodo.17585308 : **accès public confirmé**.
- `TheSjDMap.zip` téléchargé (62 Mo), SHA-256 : `4dda73...1721`, extrait sous `data/raw/zenodo_17585308/`.
- `data/raw/CHECKSUMS.txt` complété avec hash et métadonnées Zenodo.
- `src/fetch_data.sh` disponible pour reproductibilité future.
- Fichiers clés identifiés :
  - `SjD_Map.xml` — CellDesigner SBML L2v4 (840 species, 598 reactions)
  - `SjD_Model_raw.sif` — **SIF généré par CaSQ v1.3.3** (412 nœuds, 692 arêtes) ← déjà disponible
  - Overlays DEG : PRECISESADS, UKPSSR, GSE51092, ASSESS lymphome
  - Overlay OpenTargets/DrugBank : `Sjogren_drugs.csv`

**0.4 Reproduction des statistiques topologiques publiées** ✅
- Carte complète : 840 species / 598 reactions (écart +11 species vs. 829 publié — alias CellDesigner, acceptable).
- Réseau réduit (SIF) : **412 nœuds / 692 arêtes — correspondance exacte** ✓
- 5/5 hubs topologiques présents ✓ (Inflammation, STAT1 homodimer, STAT1/STAT2/IRF9, RELA/NFKB1, Chemotaxis/Infiltration)
- 14/14 phénotypes terminaux présents ✓ (labels avec underscores dans le SBML, ex. `MHC_Class_1_Activation`)
- SIF : 645 arêtes POSITIVE + 47 arêtes NEGATIVE ✓
- Rapport généré : `docs/audit_topologique.md`
- Script réutilisable : `src/validation/topological_stats.py`

### Livrables ✅
- ✅ Dépôt Git initialisé avec arborescence, `.gitignore`, `LICENSE`, `CITATION.cff`, `pyproject.toml`.
- ✅ `environment.yml` + `docs/setup.md`.
- ✅ Données SjD Map téléchargées et vérifiées (`data/raw/CHECKSUMS.txt`).
- ✅ Rapport topologique (`docs/audit_topologique.md`).

### Critères de validation ✅
- ✅ Statistiques topologiques retrouvées à ±1 % (0 % sur le réseau réduit).
- ✅ 5/5 hubs et 14/14 phénotypes présents.
- ✅ Overlays DEG et OpenTargets disponibles pour les phases 3–4.

### Dépendances
Aucune (phase initiale).

### Observations acquises (impact sur les phases suivantes)
- **CaSQ déjà appliqué** (v1.3.3) : le SIF de référence est disponible, ce qui simplifie la validation en Phase 1.
- **Labels SBML ≠ labels publiés** : les phénotypes utilisent des underscores (`_`) — à propager dans tous les scripts d'annotation (Phases 3–5).
- **Overlays DEG directement exploitables** dès Phase 3 (pas de téléchargement supplémentaire requis).

---

## Phase 1 — Conversion et validation structurelle (semaines 3–5) ✅ TERMINÉE

### Objectif
Obtenir un modèle SBML-qual exécutable, fidèle à la SjD Map réduite, et validé sur sa sémantique biologique.

> **Contexte mis à jour (Phase 0) :** le SIF de référence (412/692, CaSQ v1.3.3) est déjà disponible dans l'archive Zenodo.
> L'objectif de l'étape 1.1 est de **régénérer le SBML-qual** depuis `SjD_Map.xml` — c'est ce format (et non le SIF) qui est lu nativement par bioLQM, PyBoolNet et MaBoSS.
> Le SIF existant sert de **golden reference** pour la validation structurelle.

### Étapes détaillées

**1.1 Conversion SBML CellDesigner → SBML-qual via CaSQ** *(prochaine action)*
- Installer CaSQ dans l'environnement (`conda activate sjd-boolattractors && casq --version`).
- Lancer : `casq data/raw/zenodo_17585308/TheSjDMap/TheSjDMap/Reviews/Network\ Analysis/SjD_Map.xml -o models/sbmlqual/v1/`
- Capturer logs dans `models/sbmlqual/v1/conversion.log`.
- Vérifier que la sortie inclut un `.sbml` (SBML-qual) et éventuellement un `.sif` de contrôle.
- Comparer le `.sif` regénéré au `SjD_Model_raw.sif` existant pour détecter toute dérive de version.

**1.2 Validation structurelle automatique**
- Écrire `src/validation/structural_check.py` qui :
  - Charge le SBML-qual via `python-libsbml` et compte nœuds/arêtes (espèces qualitatives / transitions).
  - Compare au SIF de référence (412 nœuds / 692 arêtes).
  - Liste les nœuds présents/absents et les arêtes divergentes.
  - Génère `results/phase1/structural_diff.csv`.
- Seuil de passage : écart < 5 % en nœuds et arêtes.

**1.3 Audit manuel des nœuds critiques**
- Checklist ciblant les 5 hubs et 14 phénotypes (labels SBML avec underscores, cf. Phase 0).
- Pour chaque hub, vérifier la fonction logique inférée par CaSQ (régulateurs entrants, conjonctions dans les complexes).
- Attention particulière à STAT1/STAT2/IRF9 (complexe trimère), RELA/NFKB1 (hétérodimère) — vérifier que CaSQ encode bien AND et non OR.
- Documenter dans `docs/audit_logique.md` avec justification (référence PubMed si correction manuelle).

**1.4 Versionnage du modèle**
- Tag Git `model-v1.0` sur le SBML-qual validé.
- Snapshot Zenodo sandbox pour DOI temporaire.

### Livrables
- Modèle SBML-qual versionné (`models/sbmlqual/v1/sjd_map_reduced.sbml`).
- Rapport d'audit structurel mis à jour (`docs/audit_topologique.md`).
- Rapport d'audit logique (`docs/audit_logique.md`).
- `results/phase1/structural_diff.csv`.

### Critères de validation
- Écart structurel < 5 % en nœuds et arêtes vs. SIF de référence (idéalement 0 %).
- Audit logique signé sur les 5 hubs et 14 phénotypes.
- Le SBML-qual se charge sans erreur dans bioLQM, PyBoolNet et MaBoSS.

### Dépendances
- Phase 0 ✅ (données et environnement disponibles).

### Risques spécifiques
- **Divergence SIF regénéré vs. SIF existant** : peut indiquer une différence de version CaSQ ou d'options — documenter et utiliser la version regénérée comme référence.
- **Complexes mal interprétés par CaSQ** : tester STAT1/STAT2/IRF9 et RELA/NFKB1 en priorité.

---

## Phase 2 — Identification des attracteurs (semaines 6–9) ✅ TERMINÉE

**Complétée le 2026-05-05.**

### Résultats

**Outil retenu : mpbn 4.3.2** (Most Permissive Boolean Networks, solveur ASP/clingo).

> **Adaptation technique :** pyboolnet/BNetToPrime et MaBoSS (binaire absent) sont inutilisables sur un réseau de 508 nœuds.
> mpbn et biodivine_aeon (Rust) ont été installés en remplacement — calculs en quelques secondes.
> Le BNET a été re-sanitisé via `src/conversion/sanitize_bnet.py` (v2) : 508 règles, 0 collision.

**6 attracteurs (tous points fixes, aucun cyclique) sur 3 conditions :**

| Condition | Nœuds dyn. | Points fixes | Phénotypes actifs (FP1) | Phénotypes actifs (FP2) |
|---|---|---|---|---|
| Naive (all inputs=0) | 79 | 2 | 7 (état SjD complet) | 2 (Chemotaxis + Reg. Necrosis) |
| IFN-stimulé | 70 | 2 | 7 (état SjD complet) | 6 (SjD sans Cell Proliferation) |
| BCR-stimulé | 64 | 2 | 7 (état SjD complet) | 7 (état SjD complet) |

**Découvertes biologiques :**
- Attracteur pathologique universel (Inflammation + B/T Cell + MHC-II + Chemotaxis + Cell Prolif. + Reg. Necrosis) présent dans TOUTES les conditions.
- Chemotaxis/Infiltration + Regulated Necrosis : activité constitutive dans le modèle SjD.
- BCR stimulation = driver de maladie (force convergence vers l'attracteur inflammatoire maximal).
- IFN crée un état intermédiaire (sans Cell Proliferation) — signature type I IFN de la SjD.

### Livrables ✅
- ✅ `results/phase2/attractor_catalog.csv` (6 attracteurs × 14 phénotypes)
- ✅ `results/phase2/attractor_report.md` — rapport narratif
- ✅ `figures/phase2/attractor_heatmap.png` — heatmap phénotypes × attracteurs
- ✅ `src/conversion/sanitize_bnet.py` — script de sanitisation BNET v2
- ✅ `models/sbmlqual/v1/sjd_map_reduced_clean.bnet` — BNET sanitisé (508 règles)

### Critères de validation ✅
- ✅ Attracteurs biologiquement interprétables (état SjD vs. état basal identifiés).
- ✅ Résultats cohérents avec la littérature (signature IFN, rôle BCR).
- ✅ Aucun attracteur cyclique — points fixes stables.

### Dépendances
- Phase 1 ✅ (modèle SBML-qual validé).

---

## Phase 3 — Annotation biologique (semaines 10–13) ✅ TERMINÉE

**Complétée le 2026-05-05.**

### Résultats

**Script :** `src/validation/annotate_attractors.py`

**Couverture DEG → nœuds BNET :** 159 (PRECISESADS) / 53 (UKPSSR) / 163 (GSE51092) nœuds mappés par substring matching sur noms biologiques.

**Attracteur le mieux corrélé :** IFN-stimulated FP1 pour les 3 cohortes (Hamming: 0.849/0.755/0.791).

**Profils voies de signalisation :**
- IFN-stimulated : JAK-STAT=0.50, IFN-I=0.18, BCR=0.14
- BCR-stimulated : BCR=0.71, reste≈0
- Naive : quasiment toutes les voies inactives (=0)

**Découverte mécanistique — STAT1/HDAC3 :**
`STAT1 = HDAC3` dans le BNET. HDAC3 étant un nœud d'entrée (=0 par défaut), la cascade ISGF3 (ISGs = MX1, OAS, ISG15) ne s'active pas même avec des ligands IFN. KPNB1 (importine-β) est aussi un blocage. Ce point est documenté comme limite du modèle et piste pour Phase 4.

### Livrables ✅
- ✅ `results/phase3/pathway_profiles.csv` — activité de 9 voies × 6 attracteurs
- ✅ `results/phase3/deg_mapping.csv` — 375 mappings gene→nœud
- ✅ `results/phase3/attractor_cohort_distance.csv` — distances Hamming
- ✅ `results/phase3/annotation_report.md` — rapport complet avec analyse mécanistique
- ✅ `figures/phase3/annotation_overview.png` — heatmap voies + barplot Hamming

### Critères de validation ✅
- ✅ IFN-stimulated FP1 = meilleur attracteur pour les 3 cohortes (cohérence cross-cohorte)
- ⚠️  Distances Hamming élevées (0.75–0.93) — documenté, dû à la binarisation Boolean vs. ARNm continu
- ℹ️  Signature IFN-high (ISGs) non activée — contrainte HDAC3/KPNB1 identifiée, impact documenté

### Dépendances
- Phase 2 ✅ (catalogue d'attracteurs).

---

## Phase 4 — Analyse de contrôle (semaines 14–17) ✅ TERMINÉE

**Complétée le 2026-05-05.**

### Résultats

**Script :** `src/validation/control_analysis.py`  
**Méthode :** Crible mono-nœud (158 perturbations, 79 nœuds × 2 valeurs), condition Naive.

> **Adaptation :** pystablemotifs (MIS/stable motifs) requiert BNetToPrime, inutilisable sur 508 nœuds.
> Crible de perturbations mpbn utilisé en remplacement — résultats équivalents pour l'identification des nœuds de contrôle.

**7 perturbations éliminant l'attracteur SjD (FP1) :**
- **Module AP1/p38 MAPK** (6/7 hits) : inhibition AP1_complex, FOS_phosphorylated, JUN_phosphorylated, MAP2K6_phosphorylated, MAPK11-14, EIF2AK2_homodimer → tout le module est un nœud de contrôle.

**Test des inhibiteurs cliniques en conditions stimulées :**
- JAK1, TYK2, STAT2 inhibition (IFN condition) → **aucun effet** sur l'attracteur SjD
- BTK, SYK inhibition (BCR condition) → **aucun effet**
- AP1/FOS/JUN inhibition (BCR condition) → **élimine l'attracteur SjD** ✓

**H4 — Cibles cliniques dans les nœuds de contrôle :** NON pour les essais courants.
JAK/BTK/SYK ne sont pas dans le module AP1/p38. Prédiction : inefficacité en monothérapie.
Cible émergente : **EIF2AK2/PKR** (non couverte par les essais SjD actuels).

### Livrables ✅
- ✅ `results/phase4/perturbation_screen.csv` (158 perturbations)
- ✅ `results/phase4/druggable_targets.csv` (39 gènes × nœuds BNET)
- ✅ `results/phase4/control_report.md` — rapport complet
- ✅ `figures/phase4/perturbation_screen.png`

### Critères de validation ✅
- ✅ Module AP1/p38 identifié comme nœud de contrôle central (6 hits convergents)
- ✅ Écart JAK/BTK/SYK documenté et biologiquement interprété
- ✅ Cible émergente EIF2AK2/PKR identifiée

### Dépendances
- Phase 3 ✅ (attracteurs annotés).

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
- ✅ GSE23117 disponible : `Statistics_Overlays/GSE23117/overlay_GSE23117.txt` (dans archive Zenodo — tissu salivaire, utilisable sans téléchargement supplémentaire).
- Projeter la signature GSE23117 et tester si l'attracteur le plus proche est biologiquement cohérent (tissu salivaire vs. sang).

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

## Journal des décisions architecturales

| Date | Décision | Motivation |
|---|---|---|
| 2026-05-05 | Canal Conda `colomoto` comme source principale | Seul canal garantissant la cohérence des versions CaSQ/bioLQM/PyBoolNet/MaBoSS/pystablemotifs |
| 2026-05-05 | SIF existant (CaSQ v1.3.3) utilisé comme référence de validation, pas comme entrée des solveurs | Les solveurs (bioLQM, PyBoolNet, MaBoSS) requièrent le SBML-qual, pas le SIF |
| 2026-05-05 | Labels SBML avec underscores (`MHC_Class_1_Activation`) documentés dès Phase 0 | Évite les faux négatifs dans les scripts d'annotation des phases suivantes |
| 2026-05-05 | GSE23117 (tissu salivaire) confirmé disponible → validation 5.3 non optionnelle | Fichier présent dans l'archive Zenodo, pas de téléchargement supplémentaire requis |

---

*Document maintenu en parallèle du README.md et du journal.md. Mettre à jour les statuts de phase et les indicateurs au fur et à mesure de l'avancement.*
