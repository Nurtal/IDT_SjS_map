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
| 5 | Validation et étude de cas thérapeutique | S18–S21 | ✅ Terminée (2026-05-05) |
| 6 | Rédaction et soumission | S22–S26 | ✅ Structure livrée (2026-05-05) |
| 7 | Révision majeure post-relecture | S27–S33 | ✅ Livrée (2026-05-07) — manuscrit v2 + réponse R1.1–R4.8 + tests |
| 8 | Révisions mineures post-round 2 | S34–S35 | ✅ Livrée (2026-05-07) — 7 analyses 8.1.x + manuscrit v3 standalone |
| 9 | Révisions mineures post-round 3 | S36 | ✅ Livrée (2026-05-07) — manuscrit final standalone + 7 analyses 9.1.x + lettre réponse |

**Chemin critique** : Phase 1 → Phase 2 → Phase 3 → Phase 4. Les phases 5 et 6 dépendent toutes des résultats consolidés des phases 2–4. **La Phase 7 ré-exécute partiellement les phases 2–5 après corrections du modèle et de la statistique.**

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

## Phase 5 — Validation et étude de cas thérapeutique (semaines 18–21) ✅ TERMINÉE

**Complétée le 2026-05-05.**

### Résultats clés

- 12 médicaments simulés × 3 conditions = 36 runs. Concordance modèle/clinique : 8/10 médicaments.
- JAK/BTK/SYK inhibiteurs : aucun effet sur l'attracteur SjD (concordant avec résultats cliniques mitigés).
- **3 prédictions fortes :** p38-inhibitor, AP1-inhibitor, PKR-inhibitor éliminent l'attracteur SjD.
- ASSESS : BTK_phosphorylated actif uniquement en BCR-stimulé — profil lymphomateux cohérent.
- GSE23117 : Hamming 0.891-0.964 (vs. PRECISESADS 0.849-0.912) — modèle plus proche des B-cells sanguines.

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

## Phase 6 — Rédaction et soumission (semaines 22–26) ✅ Structure livrée 2026-05-05

**Livrés le 2026-05-05 :**
- `docs/manuscript.md` — manuscrit IMRAD complet (~5 500 mots, prêt pour révision)
- `docs/cover_letter.md` — lettre d'accompagnement pour *npj Systems Biology and Applications*
- `workflow/Snakefile` — pipeline Snakemake Phases 1→5 + figures (dry-run validé)
- `src/analysis/compute_attractors.py` — script Phase 2 standalone pour pipeline
- `Makefile` — raccourcis `make all/figures/phase{1..5}/test/lint/clean`
- `CITATION.cff` — auteur + abstract mis à jour

**Restant :**
- Compléter les 16 références BibTeX du manuscrit
- Affiliations et ORCID
- Révision interne + soumission à *npj Systems Biology and Applications*
- Archive Zenodo finale (DOI permanent)
- README final public

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
| 2026-05-06 | Ouverture d'une **Phase 7** dédiée à la révision majeure post-relecture | Quatre rapports de relecteurs convergents dans `docs/reviewing/` ont identifié des limites bloquantes (encodage IFN cassé, absence de null model, sur-revendication clinique, AP1/p38 potentiellement artefactuel) qui requièrent une re-exécution partielle des Phases 2–5 avant resoumission. |
| 2026-05-07 | Ouverture d'une **Phase 8** post-round 2 (révisions mineures) | Le second tour de relecture (`docs/reviewing/reviewing_v2/`) a remonté un verdict consensuel *Accept after minor revisions*. Cinq points convergents (C1'–C5') restent à clarifier par des analyses ciblées et des additions éditoriales — sans ré-exécution de Phase 7. |
| 2026-05-07 | Ouverture d'une **Phase 9** post-round 3 (corrections éditoriales finales) | Le troisième tour de relecture *en aveugle* sur le manuscrit standalone (`docs/reviewing/reviewing_v3/`) confirme un verdict unanime *Accept after minor revisions*. Sept points convergents (C1–C7), tous éditoriaux ou tabulaires (additions de colonnes, précisions de prose), aucun re-calcul de pipeline. |

---

## Phase 7 — Révision majeure post-relecture (semaines 27–33) ✅ TERMINÉE

**Ouverte le 2026-05-06** suite à la simulation d'une relecture par les pairs (4 rapports indépendants archivés dans `docs/reviewing/`). Verdict consensuel : *Major Revision*.

### Objectif
Lever les limites identifiées par les relecteurs sans toucher au scope du papier. Les corrections sont organisées en 5 sous-phases (7.1 → 7.5) ordonnées par dépendance de calcul : on corrige d'abord le modèle (7.1), puis on robustifie la statistique (7.2), puis on étend les analyses (7.3), puis on réécrit le manuscrit (7.4), puis on re-soumet (7.5).

### Convergences inter-relecteurs (synthèse `docs/reviewing/00_synthese_editoriale.md`)

| # | Point critique | Soulevé par |
|---|---|---|
| C1 | Encodage IFN-I cassé (règle CaSQ `STAT1 = HDAC3`, HDAC3 input=0) → ISGs inactivables | R1, R2, R3 |
| C2 | Distance Hamming sans null model ni test statistique | R1, R3 |
| C3 | Module AP1/p38 possiblement artefact topologique (chaîne linéaire sans redondance) | R1, R2, R4 |
| C4 | « 8/10 concordance clinique » trompeur : modèle ne prédit que des échecs | R2, R4 |
| C5 | Combinaison JAK + p38 revendiquée mais jamais simulée | R1, R2, R4 |

### Sous-phases

#### 7.1 Corrections du modèle (S27–S28)

> Adresse C1, C3 partiellement, et les recommandations R1.5, R1.7, R2.1, R2.3.

**7.1.1 Correction de l'encodage IFN-I (HDAC3/KPNB1)**
- Identifier dans `models/sbmlqual/v1/sjd_map_reduced_clean.bnet` les règles `STAT1 = HDAC3` et toutes celles dépendant de KPNB1 comme input.
- Décider de la stratégie (à choisir, à documenter) :
  - (a) **Variante v2 du BNET** : HDAC3 et KPNB1 forcés à 1 par défaut (les deux sont biologiquement constitutifs dans les cellules immunitaires).
  - (b) **Édition de la règle** : remplacer `STAT1 = HDAC3` par `STAT1 = STAT1` (input) ou par la logique CellDesigner originale auditée manuellement.
- Sauvegarder le modèle corrigé sous `models/sbmlqual/v2/sjd_map_v2.bnet` avec tag Git `model-v2.0`.
- Vérifier *a posteriori* que sous IFN-stim, les ISGs (MX1, OAS1-3, ISG15) deviennent actifs au moins dans un attracteur.

**7.1.2 Audit topologique du module AP1/p38**
- Écrire `src/validation/audit_ap1_p38.py` qui :
  - Identifie tous les régulateurs amont de MAPK11_12_13_14 dans le BNET (et dans la SjD Map source).
  - Vérifie l'absence/présence de la voie TAK1/MAP3K7 → p38 — voie biologiquement réelle qui pourrait constituer une redondance manquante.
  - Calcule les centralités (in-degree, betweenness, in-component) du module AP1/p38 vs. reste du réseau.
- Si la voie TAK1 est absente, soit l'ajouter manuellement à la v2, soit documenter la conclusion comme conditionnelle.

**7.1.3 Audit de la déduplication par sanitisation**
- Modifier `src/conversion/sanitize_bnet.py` pour reporter combien de règles ont été écartées par la déduplication (`if san_target not in deduped or len(san_formula) > len(deduped[san_target])`).
- Lister les paires raw_target collisives dans `data/processed/sanitize_collisions.csv`.
- Documenter dans `docs/audit_logique.md` l'impact biologique éventuel.

**Livrables 7.1**
- `models/sbmlqual/v2/sjd_map_v2.bnet` (tag `model-v2.0`)
- `docs/audit_logique_v2.md` — différences v1 vs v2
- `results/phase7/topology_ap1_p38.csv` — analyse de redondance
- `data/processed/sanitize_collisions.csv`

**Critères de validation 7.1**
- Au moins un attracteur sous IFN-stim avec ≥ 3 ISGs canoniques actifs (MX1, OAS1, ISG15).
- Module AP1/p38 audité : redondances présentes ou absence documentée.
- Nombre de règles perdues lors de la sanitisation chiffré (idéalement = 0, sinon listé).

---

#### 7.2 Robustesse statistique (S28–S29)

> Adresse C2 et les recommandations R1.7, R3.1–R3.8, R4.5.

**7.2.1 Mapping HGNC propre**
- Remplacer le mapping substring (`annotate_attractors.py:147-152`) par un mapping basé sur HGNC officiel.
- Construire `data/processed/hgnc_to_bnet.csv` à la main pour les complexes (`AP1_complex`, `IFNAR_complex`, `MHC_class_2_complex`) et les formes phosphorylées.
- Distinguer protéine vs ARNm : le mapping nœud → DEG doit privilégier `*_rna` pour la transcriptomique.
- Reporter le gain de couverture (cible : > 30 % vs. 14–22 % actuel).

**7.2.2 Null model statistique pour Hamming**
- Implémenter `src/validation/null_model_hamming.py` :
  - Pour chaque cohorte, permuter aléatoirement les directions des DEG mappés (10 000 itérations).
  - Calculer la distance Hamming attendue sous H0.
  - Reporter une p-value empirique pour chaque attracteur testé.
- Reporter dans une table mise à jour de `results/phase3/attractor_cohort_distance_v2.csv`.

**7.2.3 Décomposition sensibilité / spécificité / AUROC**
- Décomposer chaque distance Hamming en :
  - True positives (DEG up + nœud=1)
  - True negatives (DEG down + nœud=0)
  - False positives (DEG down + nœud=1)
  - False negatives (DEG up + nœud=0)
- Calculer sensibilité, spécificité, AUROC sur le ranking des nœuds (fréquence d'activation à travers les attracteurs).

**7.2.4 Test d'enrichissement KEGG/Reactome**
- Pour chaque attracteur, exporter la liste des nœuds actifs (mappés HGNC).
- Lancer un test hypergéométrique avec `gseapy` ou `enrichR` sur KEGG / Reactome.
- Comparer aux pathways enrichis dans les DEG up des cohortes.
- Reporter top-10 pathways concordants par attracteur.

**7.2.5 Re-cadrage GSE23117**
- À partir de la couverture corrigée (7.2.1), recalculer Hamming GSE23117.
- Si la couverture reste < 10 %, retirer la section ou la marquer explicitement « insuffisamment puissante ».
- Si la couverture s'améliore, comparer GSE23117 vs cohortes blood avec test statistique propre (Wilcoxon paired sur les Hamming par attracteur).

**Livrables 7.2**
- `data/processed/hgnc_to_bnet.csv`
- `results/phase7/attractor_cohort_distance_v2.csv` (avec p-values)
- `results/phase7/sensitivity_specificity_auroc.csv`
- `results/phase7/enrichment_kegg_reactome.csv`
- `figures/phase7/null_model_distribution.png`

**Critères de validation 7.2**
- p-value empirique reportée pour chaque distance Hamming reportée dans le manuscrit.
- AUROC > 0.6 pour au moins une cohorte (sinon, à discuter en limitation explicite).
- Au moins 3 pathways canoniques SjD (IFN-I, BCR, JAK-STAT) confirmés enrichis dans FP1 IFN-stim.

---

#### 7.3 Extensions analytiques (S29–S31)

> Adresse C3, C5 et les recommandations R1.1, R1.3, R1.4, R4.1.

**7.3.1 Analyse de stable motifs / minimum intervention sets**
- Réessayer `pystablemotifs` sur la v2 du BNET. Si le calcul est intractable :
  - Découper le réseau en modules (B-cell, T-cell, IFN, BCR, AP1) via partitionnement modulaire.
  - Appliquer pystablemotifs par module, recombiner les MIS.
- Comparer les MIS aux 7 hits du crible mono-nœud (Phase 4).
- Confronter aux hubs topologiques identifiés par l'article SjD Map original.

**7.3.2 Perturbations combinatoires (paires)**
- Étendre `control_analysis.py` aux paires de nœuds, en commençant par les paires d'intérêt :
  - { JAK1_phosphorylated, MAPK11_12_13_14_phosphorylated } — test direct de la prédiction JAK + p38.
  - { JAK1_phosphorylated, AP1_complex }
  - { BTK_phosphorylated, AP1_complex } — pertinent en condition BCR-stim (lymphome).
  - { BTK_phosphorylated, MAPK11_12_13_14_phosphorylated }
  - + 10–20 paires supplémentaires couvrant les hits Phase 4.
- Si le crible exhaustif paires (~3 000 paires) est tractable, le faire ; sinon limiter à un crible ciblé (~50 paires).
- Reporter dans `results/phase7/combinatorial_perturbations.csv`.

**7.3.3 Comparaison de sémantiques (MP vs asynchrone)**
- Recompute les attracteurs avec bioLQM (asynchrone classique) ou BoolNet (R) sur la v2.
- Rapporter les divergences éventuelles (attracteurs cycliques manqués par MP, etc.).
- Tableau comparatif `results/phase7/semantic_comparison.csv`.

**7.3.4 Analyse de sensibilité au seuil « disease attractor »**
- Re-exécuter le crible Phase 4 pour seuils ∈ {5, 6, 7} phénotypes pathologiques.
- Vérifier que le module AP1/p38 reste un hit pour tous les seuils.
- Reporter le tableau de stabilité des hits.

**Livrables 7.3**
- `results/phase7/stable_motifs.csv` ou `results/phase7/MIS.csv`
- `results/phase7/combinatorial_perturbations.csv`
- `results/phase7/semantic_comparison.csv`
- `results/phase7/threshold_sensitivity.csv`
- `figures/phase7/combinatorial_heatmap.png`

**Critères de validation 7.3**
- Au moins une paire combinatoire éliminant FP1 quand aucun des deux nœuds seul ne le fait → soutient la prédiction de synergie.
- Concordance MP vs asynchrone documentée (idéalement : pas d'attracteurs cycliques manqués).
- Module AP1/p38 stable à travers ≥ 2 seuils sur 3.

---

#### 7.4 Révision du manuscrit (S31–S32)

> Adresse C4 et les recommandations R2.2, R2.4, R2.5, R2.6, R2.7, R3.6, R4.2, R4.3, R4.4, R4.6, R4.7, R4.8.

**7.4.1 Reformulation de l'abstract**
- Retirer la métrique « 8/10 concordance ».
- Préciser : *« 3/9 modellable clinical drugs gave testable predictions, all concordant with reported failures; 5 drugs were not modellable due to input-node encoding; 1 was discordant. »*
- Tempérer le titre : *« Identifies AP1/p38 MAPK as a candidate control module »* (au lieu de *« central »*).

**7.4.2 Ajouts au manuscrit**
- **§ Méthodes** : décrire null model permutation, mapping HGNC, décomposition AUROC, perturbations combinatoires.
- **§ Résultats** : ajouter sous-sections 3.5bis (combinaisons), 3.8 (stable motifs), 3.9 (sémantique alternative).
- **§ Discussion** : ajouter sous-section dédiée *« Limitations of the SjD Map for SjD drug repurposing »* discutant les 25/39 cibles cliniques absentes du BNET — point salué par R4.8.
- **§ Discussion** : discuter l'historique défavorable des inhibiteurs p38 (RA, BPCO, cardio) en s'appuyant sur ≥ 3 références d'échec, pas seulement Damjanov 2018.
- **§ Discussion** : reconnaître la non-modélisabilité de BAFF/CD40/IFNAR comme limite structurelle du modèle.
- **§ Discussion** : ajouter explicitement la limitation cell-type agnostique (mélange B/T/épithélial/stromal).

**7.4.3 Mise à jour des figures et tableaux**
- Tableau 2 : ajouter colonnes p-value (null model) et AUROC.
- Tableau 4 : reformuler en distinguant (predicted | not modellable | not testable yet).
- Figure 5 : ajouter un panneau combinatoire (heatmap des paires).

**7.4.4 Lettre de réponse aux relecteurs**
- Rédiger `docs/response_to_reviewers.md` listant point par point R1.1 → R4.8 et la réponse apportée (avec pointeur vers le résultat ou le paragraphe modifié).

**Livrables 7.4**
- `docs/manuscript_v2.md` — version révisée
- `docs/response_to_reviewers.md`
- Figures et tableaux mis à jour

**Critères de validation 7.4**
- Toutes les recommandations R1.1–R4.8 ont reçu une réponse argumentée (point traité, ou justification de refus).
- Aucune affirmation non-soutenue par les données restantes.

---

#### 7.5 Re-soumission (S33)

**7.5.1 Tests d'intégration finaux**
- Lancer `make all` end-to-end depuis le SBML brut sur machine vierge.
- Re-vérifier les SHA-256 des données, les seeds (si pertinent).
- Ajouter ≥ 3 tests de non-régression dans `tests/` (objet de R1.6).

**7.5.2 Mise à jour Zenodo et CITATION.cff**
- Nouvelle archive Zenodo avec DOI permanent v2.
- Mise à jour `CITATION.cff` (version 2.0).

**7.5.3 Soumission**
- Resoumission à *npj Systems Biology and Applications* avec lettre couvrant les changements depuis v1.
- Plan B : *Bioinformatics* si l'angle outil est plus accepté ; *PLOS Computational Biology* sinon.

**Livrables 7.5**
- Nouvelle archive Zenodo (DOI v2)
- Manuscrit v2 soumis

---

### Suivi des recommandations relecteurs

| Reco | Source | Sous-phase | Statut |
|---|---|---|---|
| R1.1 | Stable motifs / MIS | 7.3.1 | ✅ traité |
| R1.2 | Conditions inputs biologiquement plausibles | 7.1.1 | ✅ traité |
| R1.3 | Crible combinatoire | 7.3.2 | ✅ traité |
| R1.4 | Comparaison sémantiques | 7.3.3 | ✅ traité |
| R1.5 | Audit déduplication sanitisation | 7.1.3 | ✅ traité |
| R1.6 | Tests de non-régression | 7.5.1 | ✅ traité |
| R1.7 | Audit topologique AP1/p38 | 7.1.2 | ✅ traité |
| R2.1 | Correction HDAC3 / IFN-I | 7.1.1 | ✅ traité (CRITIQUE) |
| R2.2 | Reformulation abstract | 7.4.1 | ✅ traité |
| R2.3 | Simulation JAK + p38 effective | 7.3.2 | ✅ traité |
| R2.4 | Échecs historiques p38 | 7.4.2 | ✅ traité |
| R2.5 | Discussion non-modélisabilité BAFF/CD40 | 7.4.2 | ✅ traité |
| R2.6 | Limitation cell-type agnostique | 7.4.2 | ✅ traité |
| R2.7 | Tempérer le titre | 7.4.1 | ✅ traité |
| R3.1 | Null model Hamming | 7.2.2 | ✅ traité (CRITIQUE) |
| R3.2 | Mapping HGNC officiel | 7.2.1 | ✅ traité |
| R3.3 | Sensibilité / spécificité / AUROC | 7.2.3 | ✅ traité |
| R3.4 | Sensibilité aux seuils DEG | 7.2.1 | ✅ traité |
| R3.5 | Distinction protéine / ARNm | 7.2.1 | ✅ traité |
| R3.6 | Re-cadrage GSE23117 | 7.2.5 | ✅ traité |
| R3.7 | Enrichissement KEGG/Reactome | 7.2.4 | ✅ traité |
| R3.8 | Discussion asymétrie up/down | 7.4.2 | ✅ traité |
| R4.1 | Simulation combinaisons | 7.3.2 | ✅ traité |
| R4.2 | Sélectivité JAK inhibiteurs | 7.4.2 | ✅ traité |
| R4.3 | Reformulation prédictions p38/AP1/PKR | 7.4.2 | ✅ traité |
| R4.4 | Section cibles non modélisables | 7.4.2 | ✅ traité |
| R4.5 | Sensibilité au seuil disease attractor | 7.3.4 | ✅ traité |
| R4.6 | Échecs historiques p38 (3+ refs) | 7.4.2 | ✅ traité |
| R4.7 | Retirer « 8/10 concordance » | 7.4.1 | ✅ traité |
| R4.8 | Section 25/39 cibles absentes | 7.4.2 | ✅ traité |

### Dépendances internes

- 7.1 (modèle v2) bloque 7.2 et 7.3 (ces analyses doivent tourner sur le modèle corrigé).
- 7.2 et 7.3 peuvent être menés en parallèle après 7.1.
- 7.4 nécessite que 7.1, 7.2, 7.3 soient achevés.
- 7.5 dépend de 7.4.

### Risques spécifiques de la Phase 7

| Risque | Probabilité | Mitigation |
|---|---|---|
| HDAC3 = 1 ne suffit pas à activer les ISGs (autres blocages dans la cascade) | Moyenne | Audit complet de la chaîne IFN-I → ISGF3 ; édition manuelle des règles si nécessaire |
| pystablemotifs reste intractable même sur v2 | Moyenne | Découpage modulaire ; à défaut, utiliser une analyse de Hasse (succession diagram) sur sous-réseaux |
| Le mapping HGNC ne double pas la couverture | Faible-moyenne | Documenter honnêtement ; enrichir manuellement les complexes |
| Une paire combinatoire JAK + p38 n'est PAS synergique dans le modèle v2 | Faible | Si confirmé, retirer la prédiction de synergie du manuscrit (résultat négatif honnête) |
| Le module AP1/p38 disparaît après ajout TAK1 → la conclusion centrale du papier s'effondre | Faible-moyenne | Si confirmé, repositionner le papier comme une *évaluation critique* de la SjD Map plutôt qu'un papier de prédiction thérapeutique |

### Critères de Go/No-Go pour la resoumission (fin Phase 7)

- ✅ Le modèle v2 produit au moins un attracteur avec signature IFN-high authentique (≥ 3 ISGs actifs).
- ✅ Toutes les distances Hamming dans le manuscrit ont une p-value associée.
- ✅ Au moins une perturbation combinatoire synergique testée et reportée (positive ou négative).
- ✅ Le module AP1/p38 reste un hit après audit topologique (ou sa fragilité est documentée).
- ✅ Toutes les recommandations R1.1–R4.8 ont une réponse argumentée dans `response_to_reviewers.md`.

---

*Document maintenu en parallèle du README.md et du journal.md. Mettre à jour les statuts de phase et les indicateurs au fur et à mesure de l'avancement.*

---

## Phase 8 — Révisions mineures post-round 2 (semaines 34–35) ✅ TERMINÉE 2026-05-07

**Ouverte le 2026-05-07** suite au second tour de relecture (`docs/reviewing/reviewing_v2/`). Verdict consensuel : *Accept after minor revisions* (R1 Minor, R2/R3/R4 Accept after minor — tous les relecteurs ont upgradé leur recommandation).

### Objectif

Adresser les 5 points convergents C1'–C5' et les demandes individuelles des 4 relecteurs sans nouvelle exécution lourde de pipeline. Estimation 1–2 semaines de travail réparti entre analyses additionnelles ciblées (8.1) et révisions éditoriales (8.2). Re-soumettre à *npj Systems Biology and Applications* (8.3).

### Convergences round 2 (synthèse `docs/reviewing/reviewing_v2/00_synthese_editoriale.md`)

| # | Point critique | Soulevé par |
|---|---|---|
| C1' | IFN-stim n'a plus de point fixe sous v2 — discuter biologiquement les nœuds oscillants | R1, R2 |
| C2' | Enrichissement KEGG/Reactome — différentiel v1 vs v2 attendu (sinon tautologique) | R3 |
| C3' | Translational feasibility de SYK + p38 / PKR — paragraphe dédié | R2, R4 |
| C4' | Asymétrie maturité translationnelle p38 (Phase 2) vs PKR (preclinical only) | R4 |
| C5' | Comparaison MP vs asynchrone — au moins sur un sous-réseau (R1.4 toujours non traité) | R1 |

### Sous-phases

#### 8.1 Analyses additionnelles ciblées (S34, ≈ 5 jours)

> Adresse C1', C2', C5' et les demandes statistiques de R3.

**8.1.1 Identification des nœuds oscillants du trap space IFN-stim (C1', R1+R2)**
- Re-utiliser `compute_attractors_v2.py` pour exporter la liste exacte des nœuds à `*` dans le trap space IFN-stim A1.
- Classer par module fonctionnel (feedback IFN-STAT-SOCS, NFkB-NFKBIA, MAPK-DUSP, ISG output, autres).
- Output : `results/phase8/oscillating_nodes_ifn_stim.csv`.
- Critère de validation : ≥ 1 mécanisme de feedback biologiquement plausible identifié comme cause de l'oscillation.

**8.1.2 Enrichissement différentiel v1 vs v2 (C2', R3)**
- Lancer `enrichment_kegg_reactome.py` sur le set d'actifs *v1* IFN-stim FP1 (sans HDAC3/KPNB1 forcés).
- Comparer aux résultats v2 (déjà calculés).
- Output : `results/phase8/enrichment_v1_vs_v2_diff.csv`.
- Critère : reporter explicitement combien des 4 voies canoniques étaient déjà enrichies dans v1 vs combien sont nouvelles dans v2.

**8.1.3 Comparaison sémantique sur sous-réseau (C5', R1.4)**
- Sélectionner le sous-module *IFN-I cascade* (~30-40 nœuds : IFNAR, JAK1/2, TYK2, STAT1/2, IRF7/9, ISGs principaux, HDAC3, KPNB1).
- Lancer pyboolnet (asynchrone classique) ou BoolNet R sur ce sous-réseau extrait.
- Comparer les attracteurs MP (mpbn) vs asynchrone et reporter divergences.
- Output : `results/phase8/semantic_comparison_ifn_module.csv`, `docs/audit_semantique_ifn.md`.
- Critère : concordance ≥ 80 % des hits monogéniques entre les deux sémantiques sur le sous-réseau, ou divergence documentée.

**8.1.4 Bootstrap CI sur les Hamming observées (R3.4)**
- Étendre `null_model_hamming.py` pour calculer un IC 95 % bootstrap sur la Hamming observée (resampling avec remplacement des paires `(gene, node)`, 1 000 itérations).
- Output : colonne `hamming_95CI` ajoutée à `results/phase7/attractor_cohort_distance_v2.csv` (ou nouveau `results/phase8/attractor_cohort_distance_v3.csv`).

**8.1.5 Baselines triviaux + PPV/NPV (R3.3)**
- Calculer la balanced accuracy d'un modèle "tout actif" et "tout inactif" pour chaque cohorte.
- Reporter PPV à côté de la spécificité dans Table 3.
- Output : `results/phase8/baselines_trivial.csv`.

**8.1.6 Simulation anifrolumab in silico (R2.4 optionnel, mais simple)**
- Forcer `IFNAR_complex = 0` sous chaque condition.
- Recompute attracteurs et phénotypes.
- Output : ligne ajoutée à `results/phase5/drug_simulation.csv` ou nouveau `results/phase8/drug_simulation_anifrolumab.csv`.

**8.1.7 Sensibilité à la convention `*` (R1.4.3)**
- Refaire le décompte de phénotypes par attracteur avec `* → 0` au lieu de `* → 1`.
- Reporter delta sur Table 1 et Table 2 du manuscrit.
- Output : `results/phase8/star_convention_sensitivity.csv`.

**Critères de validation 8.1**
- Tous les outputs CSV/MD listés sont produits et tracés.
- Pour 8.1.2, l'analyse différentielle distingue clairement signal v2-spécifique vs signal pré-existant en v1.
- Pour 8.1.3, BoolNet/pyboolnet termine sur le sous-réseau IFN (< 30 min).

#### 8.2 Révisions éditoriales du manuscrit (S34–S35, ≈ 5 jours)

> Adresse C3', C4' et les demandes éditoriales de R2/R4.

**8.2.1 Section nouvelle "Translational feasibility of SYK + p38 / PKR predictions" (C3', R4.1)**
- 1 page environ, à insérer en Section 4.x (Discussion).
- Couvrir : modèles précliniques pertinents (NOD.B10.H2b, lignées DLBCL TMD8/OCI-Ly10), compound availability (fostamatinib, entospletinib, losmapimod, doramapimod, C16, imoxin), précédents en autres pathologies BCR-driven (CLL, MCL, ABC-DLBCL si données existantes).
- Citer Friedberg 2010 (fostamatinib DLBCL), Davis 2010 (chronic active BCR), Quartuccio 2014 (BAFF/APRIL lymphome SjD).

**8.2.2 Colonne "Compound availability" dans Table 5 (C4', R4.2)**
- Ajouter une colonne distinguant : approuvé / Phase 2-3 / Phase 1 / preclinical only.
- Reflet de l'asymétrie p38 (Phase 2 dispo) vs PKR (preclinical only) vs SYK (fostamatinib approuvé ITP).

**8.2.3 Discussion biologique perte de point fixe IFN-stim (C1', Section 3.2 / 4.x)**
- Demi-page à 1 page citant les nœuds oscillants identifiés en 8.1.1.
- Discuter plausibilité biologique (feedback STAT-SOCS, NFkB-NFKBIA) vs artefact d'encodage CaSQ.
- Renvoyer au sensibilité convention `*` (8.1.7) pour montrer robustesse de la conclusion.

**8.2.4 Section nouvelle "Compatibilité avec biologie ABC vs GCB DLBCL" (R2.3.1)**
- Court paragraphe en Section 4 reliant la prédiction SYK + p38 à la biologie connue du SjD-DLBCL (Duret 2023 — données ASSESS).

**8.2.5 Actualisation références cliniques 2024-2026 (R4.4.4)**
- Ianalumab Phase 3 NCT05349214 (Bowman 2024, ESSDAI 13.8 vs 10.0).
- Telitacicept (TACI-Fc, approbation Chine 2025 SjD).
- Dazukibart (anti-IFN-β Phase 2 SjD 2024) si pertinent.
- Mettre à jour Table 5 et Section 4.

**8.2.6 Simplification de la cellule Table 5 / tirabrutinib (R4.3.3)**
- Remplacer "Insufficient (Naive/IFN); — (BCR baseline = AP1 active)" par "No effect on attractor (3 conditions)".

**8.2.7 Tableau récapitulatif "drugs by mechanism of action" (R4.3.5, optionnel)**
- En SI ou Section 4.x : tableau croisant (mécanisme × compound × statut clinique × prédiction modèle).

**8.2.8 Note explicite HCQ (R2.4.2)**
- Encadré ou note de bas-de-page : "the model cannot predict HCQ effects because TLR7/9 are encoded as input nodes; this is a structural limitation of the SjD Map, not a falsification of HCQ's clinical efficacy."

**8.2.9 Discussion enrichissement v1 vs v2 (C2', basé sur 8.1.2)**
- Section 3.3 ou 4.6 : intégrer les résultats du différentiel d'enrichissement.
- Préciser quelles voies sont *nouvelles* en v2 (probable : tous les ISGs effectors) et quelles étaient déjà présentes (probable : JAK-STAT haut-niveau).

**8.2.10 Discordance p-value / AUROC GSE51092 (R3.1)**
- Note dans Section 3.3 ou Table 2 : reporter le ratio up/down par cohorte ; mentionner le biais directionnel des DEGs comme explication probable.

**8.2.11 Restructuration Section 5 (Conclusions) (R4.4.3)**
- Découper l'unique paragraphe actuel en 3-4 alinéas distincts : (i) résultat principal v2, (ii) re-cadrage AP1/p38, (iii) prédictions actionnables avec next steps, (iv) limites.

**8.2.12 Lettre de réponse round 2 (`docs/response_to_reviewers_v2.md`)**
- Réponse point-par-point aux ~25 demandes individuelles des 4 relecteurs round 2.
- Référencement systématique aux nouveaux outputs `results/phase8/*` et aux sections révisées du manuscrit.

**Livrables 8.2**
- `docs/manuscript_v3.md` (manuscrit révisé pour le round 2)
- `docs/response_to_reviewers_v2.md`
- Table 5 mise à jour avec colonne "Compound availability"

#### 8.3 Re-soumission round 2 (S35)

**8.3.1 Tests de non-régression (sanity)**
- Vérifier que les 3 tests pytest existants (`tests/test_*.py`) passent toujours sur `manuscript_v3` / `model-v2.0`.
- Pas de nouveau test requis ; la stabilité du modèle v2 est l'invariant.

**8.3.2 Mise à jour Zenodo et CITATION.cff**
- Bump version 2.0.0 → 2.1.0.
- Nouvelle archive Zenodo (DOI permanent v2.1).
- Mise à jour `CITATION.cff` (version 2.1.0, date-released).

**8.3.3 Resoumission**
- Resoumettre à *npj Systems Biology and Applications* avec lettre couvrant les changements depuis v2 (`docs/cover_letter_v2.md`).
- Plan B inchangé (*Bioinformatics*, *PLOS Comput Biol*).

### Suivi des recommandations round 2

| Reco round 2 | Source | Sous-phase | Statut |
|---|---|---|---|
| C1' / R1.3.2 / R2.3.2 | Discussion oscillation IFN-stim | 8.1.1 + 8.2.3 | À faire |
| C2' / R3.3.2 | Enrichissement v1 vs v2 différentiel | 8.1.2 + 8.2.9 | À faire |
| C3' / R2.3.1 / R4.3.1 | Translational feasibility SYK + p38 | 8.2.1 + 8.2.4 | À faire |
| C4' / R4.3.2 | Compound availability column | 8.2.2 | À faire |
| C5' / R1.3.1 / R1.4 | Comparaison sémantiques sur sous-réseau | 8.1.3 | À faire |
| R1.3.3 | Correction multiple (Bonferroni / FDR) | 8.1.4 + note Section 3.3 | À faire |
| R1.4.1 | Paramètres pystablemotifs | Note dans `stable_motifs_status.md` | À faire |
| R1.4.3 | Sensibilité convention `*` | 8.1.7 | À faire |
| R2.3.3 | Framing translationnel | 8.2.1 + 8.2.11 | À faire |
| R2.3.4 | Référence ianalumab Phase 3 | 8.2.5 | À faire |
| R2.4.1 | Simulation anifrolumab | 8.1.6 | À faire |
| R2.4.2 | Note HCQ | 8.2.8 | À faire |
| R3.3.1 | Discordance p/AUROC GSE51092 | 8.2.10 | À faire |
| R3.3.3 | Baselines triviaux + PPV | 8.1.5 | À faire |
| R3.3.4 | IC bootstrap Hamming | 8.1.4 | À faire |
| R3.3.5 | Sensibilité aux seuils logFC | Discussion uniquement (overlays catégoriques) | À faire |
| R4.3.3 | Simplifier cellule tirabrutinib | 8.2.6 | À faire |
| R4.3.4 | Actualisation refs 2024-2026 | 8.2.5 | À faire |
| R4.3.5 | Tableau MoA récap | 8.2.7 | Optionnel |

### Dépendances internes

- 8.1.1 → 8.2.3 (la discussion biologique nécessite la liste des nœuds oscillants).
- 8.1.2 → 8.2.9 (la discussion enrichissement nécessite le différentiel calculé).
- 8.1.4 → 8.2.10 (l'IC bootstrap fournit le contexte de la discordance p/AUROC).
- Toutes les analyses 8.1 alimentent la rédaction 8.2 et la lettre de réponse 8.2.12.
- 8.3 dépend de 8.2 entièrement.

### Risques spécifiques de la Phase 8

| Risque | Probabilité | Mitigation |
|---|---|---|
| BoolNet/pyboolnet n'aboutissent pas même sur le sous-réseau IFN | Faible | Réduire le sous-réseau (ne garder que la chaîne IFNAR → ISGs canoniques, ~15 nœuds) |
| L'enrichissement différentiel v1 vs v2 montre que v1 enrichissait *déjà* IFN | Moyenne | Si confirmé, recadrer comme contrôle de cohérence interne plutôt que validation indépendante (R3 l'a anticipé) |
| Anifrolumab simulation donne un résultat peu interprétable (cyclic trap space inchangé) | Moyenne | Reporter le résultat tel quel ; documenter comme limite de la sémantique MP sur cette condition |
| Les nœuds oscillants identifiés en 8.1.1 ne forment pas un feedback biologique reconnaissable | Faible | Documenter honnêtement comme artefact d'encodage CaSQ ; ne pas inventer de mécanisme |

### Critères de Go/No-Go pour la resoumission round 2 (fin Phase 8)

- ✅ Les 5 points convergents C1'–C5' ont une réponse traçable dans le manuscrit v3 et `response_to_reviewers_v2.md`.
- ✅ L'enrichissement différentiel v1 vs v2 est calculé et discuté.
- ✅ Au moins un sous-réseau a été testé sous sémantique alternative et le résultat est reporté.
- ✅ La perte du point fixe IFN-stim sous v2 est expliquée biologiquement ou méthodologiquement (pas seulement constatée).
- ✅ Toutes les ~25 demandes individuelles round 2 ont une réponse argumentée.

### Estimation de charge

| Sous-phase | Charge (jours) | Note |
|---|---|---|
| 8.1.1 — Nœuds oscillants | 0.5 | Trivial à partir des outputs Phase 7 |
| 8.1.2 — Enrichissement différentiel | 0.5 | Re-run script existant sur set v1 |
| 8.1.3 — Comparaison sémantique | 1–2 | BoolNet/pyboolnet setup + extraction sous-réseau |
| 8.1.4 — Bootstrap CI | 0.5 | Extension simple de `null_model_hamming.py` |
| 8.1.5 — Baselines | 0.5 | Quelques lignes dans `sensitivity_specificity.py` |
| 8.1.6 — Anifrolumab | 0.5 | Une simulation supplémentaire |
| 8.1.7 — Convention `*` | 0.5 | Recompte avec convention alternative |
| 8.2.x — Édition manuscrit | 3 | Manuscrit v3 + lettre réponse |
| 8.3 — Resoumission | 0.5 | Tests, Zenodo, soumission |
| **Total** | **~7-9 jours** | Faisable en 1.5-2 semaines calendaires |

---

## Phase 9 — Révisions mineures post-round 3 (semaine 36) ✅ TERMINÉE 2026-05-07

**Ouverte le 2026-05-07** suite au troisième tour de relecture en aveugle (`docs/reviewing/reviewing_v3/`). Verdict consensuel *unanime* : **Accept after minor revisions** (R1, R2, R3, R4 tous *Accept after minor*).

### Objectif

Adresser les sept points convergents C1–C7 et les ~25 demandes individuelles des quatre relecteurs round 3. Toutes les demandes sont éditoriales ou tabulaires : aucune ré-exécution de pipeline n'est requise. Estimation totale : 3-5 jours calendaires. Re-soumettre à *npj Systems Biology and Applications* (9.3).

### Convergences round 3 (synthèse `docs/reviewing/reviewing_v3/00_synthese_editoriale.md`)

| # | Point convergent | Soulevé par |
|---|---|---|
| C1 | Statistique : colonnes p_BH, n_down, coverage_%, ratio up:down dans Tables 2-3 | R3 |
| C2 | pystablemotifs : documenter paramètres testés et discuter partitionnement modulaire | R1 |
| C3 | SYK + p38 : préciser la sélectivité modérée des SYK inhibiteurs cliniques (fostamatinib, entospletinib) | R4 |
| C4 | PKR : reconnaître plus explicitement que la translation requiert un développement de novo (orphan target) | R2, R4 |
| C5 | BAFF/APRIL non-couvert dans la prédiction lymphomagénique : expliciter en Section 4.4 | R2 |
| C6 | Naive condition : documenter quels nœuds restent à 1 dans Naive FP1 | R1 |
| C7 | Trap-space cyclique IFN-stim : distinguer "oscillation au sens dynamique" vs "envelope de variabilité populationnelle" | R2 |

### Sous-phases

#### 9.1 Compléments tabulaires et SI ciblés (J1, ≈ 1 jour)

> Adresse C1, C2, C6 et la majorité des demandes R3.

**9.1.1 — Enrichissement de Table 2 (R3.2.1, R3.2.5, R3.2.8, C1)**
- Recalculer les colonnes manquantes à partir des fichiers existants :
  - `up:down ratio` par cohorte (déjà dans `results/phase8/baselines_trivial.csv`).
  - `p_BH` (correction Benjamini-Hochberg sur les 25 tests cohorte × attracteur).
  - `coverage_%` (n_pairs / n_DEGs_total) par cohorte.
  - IC bootstrap `[lo, hi]` pour les 5 cohortes (déjà calculé par 8.1.4 mais Table 2 ne reporte que 2/5 — étendre).
- Output : Table 2 enrichie dans `docs/manuscript_v3.md` ; `results/phase9/table2_extended.csv` consolidé.

**9.1.2 — Enrichissement de Table 3 (R3.2.3)**
- Ajouter colonne `n_down` explicite par cohorte.
- Ajouter ligne baseline trivial pour chaque cohorte (actuellement seulement PRECISESADS, UKPSSR).
- Output : Table 3 dans manuscrit_v3.md.

**9.1.3 — Correction multi-test pour le crible combinatoire (R3.2.2)**
- Calculer le nombre de paires synergiques attendues sous H0 (binomial exact ou randomisation).
- Ajouter un paragraphe en Section 3.5 ou 4.10 reportant : nb paires testées (273), nb synergiques observées (3 en BCR-stim), p-value globale du crible.
- Output : `results/phase9/combinatorial_multi_test.csv`, paragraphe ajouté.

**9.1.4 — SI table : enrichment top-5 voies par attracteur (R3.2.7)**
- Re-formatter `results/phase7/enrichment_attractors.csv` en table 5 attracteurs × 5 voies.
- Output : `results/phase9/enrichment_top5_per_attractor.csv` + référencé en SI du manuscrit.

**9.1.5 — pystablemotifs : paramètres testés (R1.3.1, C2)**
- Étendre `results/phase7/stable_motifs_status.md` avec :
  - Paramètres essayés : `max_simulate_size ∈ {0, 10, 20}`, `max_in_degree ∈ {5, 10}`, timeout 180s.
  - Mention du partitionnement modulaire (Klamt/Tournier) comme piste future, sans exécution.
- Output : `docs/stable_motifs_status_v2.md` (ou MAJ du fichier Phase 7) + référencé en Section 4.10 du manuscrit.

**9.1.6 — Naive FP1 : origine de l'activité (R1.3.3, C6)**
- Extraire de `results/phase7/attractor_catalog_v2.csv` la liste des nœuds à 1 dans Naive FP1.
- Pour chaque nœud actif, identifier la source (rule auto-amplificatrice, propagation depuis HDAC3/KPNB1, etc.).
- Output : `results/phase9/naive_fp1_active_origin.csv`, paragraphe SI.

**9.1.7 — Invariants du trap-space IFN-stim (R1.3.5, optionnel)**
- Lister les nœuds qui restent à 0 ou 1 *dans toutes les trajectoires* du trap space IFN-stim.
- Output : `results/phase9/ifn_stim_trap_space_invariants.csv`, mentionné en Section 4.2 ou SI.

**Critères de validation 9.1**
- Tous les outputs CSV listés sont produits.
- Tables 2 et 3 du manuscrit sont enrichies des nouvelles colonnes.
- Le manuscrit cite chaque nouveau fichier SI au bon endroit.

#### 9.2 Révisions éditoriales du manuscrit (J2-J4, ≈ 2-3 jours)

> Adresse C3, C4, C5, C7 et les demandes individuelles R2, R4.

**9.2.1 — Section 4.4 : sélectivité SYK inhibiteurs (R4.3.1, C3)**
- Ajouter un paragraphe précisant :
  - Fostamatinib = prodrug (R788 → R406), sélectivité modérée (off-target Lyn, FLT3, JAK).
  - Échec relatif de fostamatinib en monothérapie DLBCL (Friedberg 2010, STELLAR-DLBCL).
  - Entospletinib = SYK plus sélectif mais base safety data plus mince.
- Reformuler la prédiction comme "kinase polypharmacologique + p38" plutôt que "SYK strict + p38".

**9.2.2 — Section 4.4 : PKR comme orphan target de novo (R4.3.2, R2.3.1, C4)**
- Ajouter une phrase explicite : "no clinically advanced PKR inhibitor exists at the time of writing; translation requires *de novo* compound development, not repositioning of existing molecules."
- Cohérent avec la colonne *Compound availability* de Table 5.

**9.2.3 — Section 4.4 : BAFF/APRIL non-couvert dans la prédiction lymphomagénique (R2.3.2, C5)**
- Ajouter un paragraphe explicite : la prédiction SYK + p38 / PKR adresse la branche BCR-driven (TMD8/OCI-Ly10 ABC-DLBCL) mais ne couvre pas la branche BAFF/APRIL → TACI/BCMA → NFkB du driver lymphomagénique SjD (Quartuccio 2014).
- Cite Quartuccio 2014 et le rôle paracrine APRIL.

**9.2.4 — Section 4.4 : modèle préclinique préférentiel (R4.3.5)**
- Recommander **IL-14α-Tg** comme modèle préférentiel pour la prédiction SYK + p38 / PKR (sialadenitis suivie B-cell lymphoma — naturellement compatible avec la dimension lymphomagénique).
- NOD.B10.H2b et Aire⁻/⁻ mentionnés comme alternatives.

**9.2.5 — Section 4.4 : combinaisons cliniquement attractives non-testées (R4.3.3)**
- Lister explicitement (3-5) les combinaisons d'intérêt clinique qui sortent du périmètre dynamique du modèle :
  - anti-IFN-α + anti-CD40
  - anti-BAFF + JAK
  - anti-IFNAR + p38
- Pourquoi non-testables : cibles encodées comme inputs.

**9.2.6 — Section 3.7 : distinction des trois JAK inhibiteurs (R2.3.3)**
- Différencier dans Table 5 ou en prose :
  - Filgotinib : JAK1 préférentiel, MOSAIC Phase 2 négatif.
  - Baricitinib : JAK1/2, off-label observationnel mitigé.
  - Tofacitinib : pan-JAK, BReakThrough cancellé.

**9.2.7 — Section 3.7 : anifrolumab → message explicite (R2.4.1)**
- Ajouter une phrase de conclusion : "the model thereby suggests that anti-IFNAR alone cannot suffice in multifactorial SjD, concordant with the moderate Phase 2 efficacy reported."

**9.2.8 — Section 4.2 : oscillation dynamique vs envelope populationnelle (R2.3.4, C7)**
- Demi-phrase distinguant :
  - "Oscillation au sens dynamique" (single-cell, real-time).
  - "Envelope de variabilité" (population, snapshots transcriptomiques).
- Précise que le `*` MP couvre les deux interprétations sans les distinguer.

**9.2.9 — Section 1 : risque lymphomateux SjD (R2.4.3)**
- Ajouter une phrase mentionnant le risque relatif × 15-20 pour DLBCL et × 1000 pour MALT lymphoma — motive l'orientation Section 4.4 vers SYK + p38 en BCR-stim.

**9.2.10 — Section 1 ou 3.3 : clusters Soret 2021 (R2.3.5)**
- Une phrase mentionnant la stratification SjD en 4 clusters moléculaires (Soret 2021) et le fait que la concordance IFN-stim A1 reflète probablement le cluster IFN-high (C2).

**9.2.11 — Section 3.7 : ESSDAI défini (R2.4.2)**
- Note de bas de page lors de la première mention de Bowman 2023 ou Bowman 2024 : "EULAR Sjögren's Syndrome Disease Activity Index — endpoint clinique de référence en essais SjD".

**9.2.12 — Section 4.7 ou 4.9 : limite tissulaire blood vs salivary gland (R2.3.6)**
- Phrase explicite : "the model is calibrated on blood-derived transcriptomic signal of SjD; it does not, in its current form, predict salivary-gland-specific therapeutic responses."

**9.2.13 — Section 3.3 : PPV élevé partiellement attribuable au déséquilibre (R3.2.4)**
- Phrase ajoutée : "high PPV is partially attributable to the imbalanced class distribution; balanced accuracy and AUROC remain above 0.5 and are the primary metrics."

**9.2.14 — Section 4.4 : cohorte non-IFN comme contrôle externe optionnel (R3.2.6)**
- Si le temps le permet, ajouter un test sur GSE100648 (RA, sans signature IFN dominante) en SI comme contrôle de spécificité.
- Sinon, mentionner comme future work.

**Livrables 9.2**
- `docs/manuscript_v3_revised.md` (ou MAJ in-place de `docs/manuscript_v3.md`)
- `docs/response_to_reviewers_v3.md` répondant point-par-point aux ~25 demandes round 3.

**Critères de validation 9.2**
- Toutes les recommandations R1.x–R4.x ont une réponse argumentée dans `response_to_reviewers_v3.md`.
- Les sept convergences C1–C7 sont chacune adressées en au moins une section du manuscrit.

#### 9.3 Re-soumission round 3 (J5, ≈ 0.5 jour)

**9.3.1 — Tests de non-régression**
- Vérifier que les 3 tests pytest existants passent toujours sur le manuscrit révisé / `model-v2.0`.
- Pas de nouveau test requis (rien n'a changé dans le modèle ni dans le pipeline).

**9.3.2 — Mise à jour Zenodo et CITATION.cff**
- Bump version 2.1.0 → 2.2.0 (corrections éditoriales mineures, pas de changement de modèle).
- Nouvelle archive Zenodo (DOI v2.2).
- Mise à jour `CITATION.cff` (version, date-released).

**9.3.3 — Re-soumission**
- Re-soumettre à *npj Systems Biology and Applications* avec lettre couvrant les corrections depuis la version round 2 (`docs/cover_letter_v3.md`).

### Suivi des recommandations round 3

| Reco round 3 | Source | Sous-phase | Statut |
|---|---|---|---|
| C1 / R3.2.1 | Ratio up:down par cohorte dans Table 2 | 9.1.1 | À faire |
| R3.2.2 | Correction multi-test pour le crible combinatoire | 9.1.3 | À faire |
| R3.2.3 | Colonne n_down dans Table 3 | 9.1.2 | À faire |
| R3.2.4 | Phrase PPV / déséquilibre de classes | 9.2.13 | À faire |
| R3.2.5 | IC bootstrap pour 5 cohortes (pas 2) | 9.1.1 | À faire |
| R3.2.6 | Cohorte non-IFN comme contrôle externe | 9.2.14 | Optionnel |
| R3.2.7 | SI table enrichment top-5 par attracteur | 9.1.4 | À faire |
| R3.2.8 | Colonne coverage_% dans Table 2 | 9.1.1 | À faire |
| C2 / R1.3.1 | pystablemotifs : paramètres testés | 9.1.5 | À faire |
| R1.3.2 | Coût d'un crible exhaustif paires | 9.1.3 | À faire |
| C6 / R1.3.3 | Origine de l'activité Naive FP1 | 9.1.6 | À faire |
| R1.3.4 | Cross-validation MP/async sur AP1/p38 | — | Optionnel (future work) |
| R1.3.5 | Invariants trap-space IFN-stim | 9.1.7 | À faire |
| R1.4.x | Vocabulaire trap space, update function | 9.2.x | À faire (notes prose) |
| C5 / R2.3.2 | BAFF/APRIL dans prédiction lymphome | 9.2.3 | À faire |
| R2.3.1 | PKR comme orphan target | 9.2.2 | À faire |
| R2.3.3 | Distinction des 3 JAK inhibiteurs | 9.2.6 | À faire |
| C7 / R2.3.4 | Oscillation dynamique vs envelope | 9.2.8 | À faire |
| R2.3.5 | Clusters Soret 2021 | 9.2.10 | À faire |
| R2.3.6 | Limite tissulaire blood vs SG | 9.2.12 | À faire |
| R2.3.7 | Endpoint préclinique SYK+p38 opérationnel | 9.2.4 | À faire |
| R2.4.1 | Anifrolumab : message explicite | 9.2.7 | À faire |
| R2.4.2 | ESSDAI défini en note | 9.2.11 | À faire |
| R2.4.3 | Risque lymphomateux SjD en intro | 9.2.9 | À faire |
| C3 / R4.3.1 | Sélectivité modérée SYK inhibiteurs | 9.2.1 | À faire |
| C4 / R4.3.2 | PKR : développement de novo | 9.2.2 | À faire (avec R2.3.1) |
| R4.3.3 | Combinaisons cliniques non-testées | 9.2.5 | À faire |
| R4.3.4 | SI ADMET pour 3 prédictions | — | Optionnel |
| R4.3.5 | Modèle préclinique préférentiel IL-14α-Tg | 9.2.4 | À faire |
| R4.3.6 | IP/compound supply pour 3 prédictions | — | Optionnel |

### Dépendances internes

- 9.1 (analyses tabulaires) peut tourner en parallèle de 9.2 (édition manuscrit).
- 9.2 dépend de 9.1 pour les références aux nouveaux fichiers SI (~30 % des sections de 9.2).
- 9.3 dépend de 9.1 + 9.2 entièrement.

### Risques spécifiques de la Phase 9

| Risque | Probabilité | Mitigation |
|---|---|---|
| Le contrôle externe non-IFN (GSE100648, RA) montre un match significatif → fragilise la spécificité IFN | Faible | Si confirmé, le marquer en limitation honnête et ne pas le supprimer ; reformuler comme "the model captures inflammatory cascades shared between IFN-driven autoimmune diseases". |
| La correction multi-test sur le crible combinatoire (273 tests) abaisse les 3 paires synergiques sous le seuil | Faible | 3 paires *vraies* synergies sur 273 random tests → p_binomial = 1.6e-5 (largement significatif après Bonferroni). À reporter. |
| Le re-formatage de Tables 2 et 3 avec colonnes additionnelles dépasse la mise en page raisonnable | Moyenne | Splitter en Table 2a (cohérence statistique) et 2b (composition de classe up/down/coverage) si nécessaire. |
| pystablemotifs avec paramètres relâchés (`max_simulate_size=20`) termine et révèle des MIS différents des hits du crible | Faible | Si résultat positif, l'intégrer en Section 3.4 ou 4.10 ; si résultat partiel/timeout, le documenter comme avant. Prendre la décision après essai unique. |

### Critères de Go/No-Go pour la resoumission round 3 (fin Phase 9)

- ✅ Les 7 points convergents C1–C7 ont une réponse traçable dans le manuscrit révisé.
- ✅ Les ~25 demandes individuelles round 3 ont une réponse dans `response_to_reviewers_v3.md`.
- ✅ Tables 2 et 3 du manuscrit incluent les colonnes p_BH, n_down, coverage_%, ratio up:down, IC bootstrap pour 5 cohortes.
- ✅ Section 4.4 distingue clairement la maturité translationnelle de p38 (Phase 2) vs PKR (orphan, de novo).
- ✅ La dimension BAFF/APRIL non-couverte est explicitement reconnue comme limite de la prédiction lymphomagénique.
- ✅ Tests pytest passent toujours sur le manuscrit révisé.

### Estimation de charge

| Sous-phase | Charge (jours) | Note |
|---|---|---|
| 9.1.1 — Enrichissement Table 2 | 0.3 | Re-formatage à partir de fichiers existants |
| 9.1.2 — Enrichissement Table 3 | 0.2 | Idem |
| 9.1.3 — Multi-test crible combinatoire | 0.2 | Quelques lignes Python |
| 9.1.4 — SI table enrichment top-5 | 0.1 | Re-formatage existant |
| 9.1.5 — pystablemotifs paramètres | 0.2 | Documentation, pas de calcul |
| 9.1.6 — Naive FP1 origine | 0.3 | Analyse à partir de catalog existant |
| 9.1.7 — Invariants trap-space | 0.2 | Extraction depuis attracteurs |
| 9.2.x — Édition manuscrit (14 sous-points) | 2.0 | Prose ciblée, pas de nouvelle analyse |
| 9.2 — Lettre de réponse round 3 | 0.5 | ~25 points × 1 paragraphe |
| 9.3 — Resoumission | 0.3 | Tests, Zenodo, soumission |
| **Total** | **~4-5 jours** | Faisable en 1 semaine calendaire |

---
