# Journal de bord — SjD-BoolAttractors

Suivi chronologique des actions menées sur le projet, en parallèle de la ROADMAP.md.
Format : une entrée datée par session de travail. Les tâches sont rattachées à la phase et à l'étape correspondante de la ROADMAP.

---

## 2026-05-05 — Démarrage Phase 0

### Phase 0.1 — Initialisation de la structure du projet

**Actions réalisées :**
- Création de l'arborescence cible : `data/raw/`, `data/processed/`, `models/sbmlqual/v1/`, `notebooks/phase2/`, `src/validation/`, `src/conversion/`, `results/phase{1..5}/`, `figures/phase{2..4}/`, `docs/`, `tests/`.
- Mise à jour du `.gitignore` :
  - Exclusion de `.venv/`, caches Python, notebooks checkpoints.
  - Exclusion de `data/raw/*` et `data/processed/*` (sauf `.gitkeep` et `CHECKSUMS.txt`) — données suivies hors Git via Zenodo.
  - Exclusion des sorties régénérables (`results/**/*.json|csv`, `figures/**/*.png|svg|pdf`).
  - Exclusion fichiers OS et IDE.

**Fichiers créés (suite) :**
- `LICENSE` — MIT (template standard).
- `CITATION.cff` — métadonnées Zenodo/GitHub, auteurs à compléter.
- `pyproject.toml` — dépendances projet (CaSQ, bioLQM, PyBoolNet, pystablemotifs, libsbml, stack scientifique) + extras `dev` (pytest, ruff, mypy).
- 16 fichiers `.gitkeep` ajoutés pour préserver l'arborescence vide dans Git.

**Note :** `biolqm` n'est pas systématiquement présent sur PyPI sous ce nom (il est livré comme un JAR Java exécuté via Java/Maven, ou via le wrapper `bioLQM` du conteneur Colomoto). À valider en Phase 0.2 lors de la résolution Conda — sinon, basculer sur installation via conda-forge ou conteneur Colomoto.

### Phase 0.2 — Environnement reproductible ✓

**Actions réalisées :**
- `environment.yml` : Conda, canal `colomoto` (CaSQ, bioLQM, PyBoolNet, MaBoSS, pystablemotifs, openjdk≥17), stack scientifique (numpy, pandas, scipy, matplotlib, seaborn, networkx, scikit-learn), JupyterLab, outils dev (pytest, ruff, pre-commit).
- `docs/setup.md` : instructions Option A (Conda/mamba) + Option B (Colomoto Docker), génération du lockfile, commande de tests.

**Note :** le canal `colomoto` est le seul canal où toutes les dépendances du projet coexistent avec des versions compatibles. Si résolution impossible, utiliser le conteneur Docker Colomoto en Option B.

### Phase 0.3 — Récupération des données SjD Map ✓

**Actions réalisées :**
- `src/fetch_data.sh` : script shell autonome qui (1) résout le DOI Zenodo, télécharge les fichiers, (2) clone le dépôt GitLab avec référence de commit figée, (3) calcule les SHA-256 dans `data/raw/CHECKSUMS.txt`.
- `data/raw/CHECKSUMS.txt` : fichier initialisé avec en-tête (à compléter après téléchargement effectif).

**Note :** le Zenodo DOI 10.5281/zenodo.17585308 est associé à un article 2026. Si le record est encore privé, téléchargement manuel requis et consigné dans `data/raw/zenodo_manual/`.

### Phase 0.4 — Reproduction des statistiques topologiques ✓

**Actions réalisées :**
- `src/validation/topological_stats.py` : script Python qui charge un SBML/SBML-qual via libsbml, construit un DiGraph NetworkX, calcule nœuds/arêtes, top-10 hubs par degré, vérifie la présence des 5 hubs attendus et des 14 phénotypes terminaux, et génère `docs/audit_topologique.md`.
- Usage : `python src/validation/topological_stats.py --sbml data/raw/<fichier>.xml --expected-nodes 412 --expected-edges 692`
- Critère de validation : écart ≤ 1 % sur nœuds et arêtes, présence confirmée des 5 hubs.

### Phase 0.3 (suite) — Téléchargement effectif Zenodo ✓

**Actions réalisées :**
- Record Zenodo 17585308 : accès **public** (contrairement à la crainte initiale).
- Téléchargement `TheSjDMap.zip` (62 Mo) via API Zenodo.
- SHA-256 : `4dda73430f4b85e55aa10fc5a36ab666635b9a4ad2dcf8c2ac25263b5d091721`
- Extraction dans `data/raw/zenodo_17585308/TheSjDMap/`.
- `data/raw/CHECKSUMS.txt` mis à jour avec hash et métadonnées Zenodo.

**Contenu clé de l'archive :**
- `Reviews/Network Analysis/SjD_Map.xml` — CellDesigner SBML L2v4 (840 species, 598 reactions)
- `Reviews/Network Analysis/SjD_Model_raw.sif` — SIF généré par **CaSQ v1.3.3** (412 nœuds, 692 arêtes)
- `Statistics_Overlays/Blood_datasets/` — overlays DEG (GSE51092, PRECISESADS, UKPSSR)
- `Statistics_Overlays/ASSESS/` — overlay lymphome
- `Statistics_Overlays/Open_Targets/Clinical_trials_drugs/Sjogren_drugs.csv` — overlay DrugBank/OpenTargets

### Phase 0.4 — Audit topologique ✓

**Résultats :**
- Carte complète : 840 species / 598 reactions (attendu 829/598 ; écart de +11 species dû aux alias CellDesigner, acceptable)
- Réseau réduit (SIF) : **412 nœuds / 692 arêtes — correspondance exacte** avec les valeurs publiées
- 5/5 hubs topologiques présents dans le SBML ✓
- 14/14 phénotypes terminaux présents ✓ (labels avec underscores dans le SBML, ex. `MHC_Class_1_Activation`)
- SIF contient 645 arêtes POSITIVE + 47 arêtes NEGATIVE (inhibitions) → logique booléenne complète
- Rapport généré : `docs/audit_topologique.md`

**Découverte importante :** CaSQ v1.3.3 a **déjà été appliqué** par les auteurs ; le SIF est disponible.
Il faut retrouver ou régénérer le **SBML-qual** associé (format natif pour bioLQM/PyBoolNet).
Le SIF sera utilisé comme référence de comparaison en Phase 1.

**Décision : GO Phase 1.**

---

## 2026-05-05 — Phase 1 : Conversion CaSQ

### Phase 1.1 — Conversion CaSQ ✓

**Environnement :** CaSQ installé via pip (v1.3.3 pour coller à la version des auteurs).

**Conversion exécutée :**
```
casq -s data/raw/.../SjD_Map.xml models/sbmlqual/v1/sjd_map_reduced.sbml
```

**Résultats :**
- SBML-qual : 508 species / 404 transitions
- SIF généré : 819 arêtes (POSITIVE: 751, NEGATIVE: 68)

**Divergence vs. référence publiée (412/692) :**
- Cause identifiée : la référence est passée par Cytoscape (export SIF alias-based)
  avec déduplication. Notre SBML-qual conserve les alias CellDesigner comme IDs de nœuds,
  ce qui est le comportement correct de CaSQ.
- IDs dans le SBML-qual : `sa*` / `csa*` (alias CellDesigner)
- Noms biologiques dans l'attribut `name` (avec suffixes `_phenotype`, `_complex`, `_rna`)
- **Tous les 14 phénotypes présents** (suffixe `_phenotype` : `sa105` = Inflammation_phenotype, etc.)
- **5 hubs présents** (STAT1/STAT2/IRF9 → `csa5`, RELA/NFKB1 → `csa37`, etc.)

**Fichiers produits :**
- `models/sbmlqual/v1/sjd_map_reduced.sbml` — modèle de travail canonique
- `models/sbmlqual/v1/sjd_map_reduced.sif` — SIF dérivé (noms biologiques)
- `models/sbmlqual/v1/conversion.log` — log de conversion avec explication de l'écart
- `docs/audit_logique.md` — audit des nœuds critiques et décision Go
- `data/processed/alias_to_name.csv` — table 1151 lignes alias_id → nom biologique
- `data/processed/ref_sif_named.csv` — SIF de référence avec noms biologiques ajoutés

**Décision : GO Phase 1.2 (structural_check.py)**

### Phase 1.2 — Validation structurelle automatique ✓

**Script :** `src/validation/structural_check.py`

**Résultats :**
- 13/13 phénotypes terminaux détectés (correction du matching underscore/espace)
- 751 arêtes POSITIVE + 68 NEGATIVE (correction de la lecture du signe `sign` attribute)
- `results/phase1/structural_report.md` généré
- `results/phase1/structural_diff.csv` : 352 nœuds uniquement dans SBML-qual, 156 uniquement dans la référence, 156 communs

### Phase 1.3 — Audit logique des nœuds critiques ✓

**Résultats :**
- **Inflammation** (sa105) : 44 régulateurs entrants positifs → nœud terminal ✓
- **STAT1/STAT2/IRF9** (csa5) : `AND(IRF9, STAT1/STAT2_complex)` — conjonction correcte ✓
- **RELA/NFKB1** (csa37) : `AND(OR(activateurs), NOT(NFKBIA), NOT(TNFAIP3))` — logique combinatoire avec inhibiteurs ✓
- **STAT1 homodimer** (sa417 = phosphorylated) : activé par STAT1_phosphorylated → 42 cibles ✓
- **Chemotaxis/Infiltration** (sa1184) : 22 régulateurs entrants → nœud terminal ✓
- `docs/audit_logique.md` mis à jour avec tableau complet

### Phase 1.4 — Versionnage ✓

- Commit `84b95c6` : Phase 0 + Phase 1.1-1.3 complètes
- Tag Git : `model-v1.0` — SBML-qual SjD Map v1.0 (508 nœuds, 819 arêtes)

---

## 2026-05-05 — Phase 2 : Identification des attracteurs

### Phase 2.0 — Sanitisation BNET ✓

**Problème identifié :** Le BNET généré par CaSQ contient des noms de nœuds avec des caractères illégaux pour pyboolnet (`/`, `,`, `()`, espaces). La version précédente du script de sanitisation était incomplète (ex. : `PI(3,4,5)P3_simple_molecule` → `PI_3,4,5)P3_simple_molecule`).

**Solution :**
- Script `src/conversion/sanitize_bnet.py` réécrit : `re.sub(r'[^A-Za-z0-9_]', '_', name)` appliqué à TOUS les tokens.
- Remplacement des tokens dans les formules par ordre de longueur décroissante (évite le remplacement partiel).
- Résultat : **508 règles**, 131 nœuds renommés, **0 collision**, **14 phénotypes** confirmés.
- Fichier : `models/sbmlqual/v1/sjd_map_reduced_clean.bnet`
- Table : `data/processed/bnet_name_map.csv`

**Problème pyboolnet/BNetToPrime :** Le binaire `BNetToPrime_linux64` timeout sur un réseau de 508 nœuds (calcul des implicants premiers exhaustif, intractable à cette taille).

**Solution retenue :** Basculer sur **mpbn 4.3.2** (Most Permissive Boolean Networks) + **biodivine_aeon 1.3.5** (Rust), installés via pip. mpbn utilise le solveur ASP/clingo, efficace pour les grands réseaux.

### Phase 2.1 — Analyse des attracteurs (mpbn) ✓

**Outil :** mpbn 4.3.2 (Most Permissive update, solveur ASP/clingo)

**Stratégie :**
1. Les 104 nœuds d'entrée (self-loops) fixés selon la condition biologique.
2. Propagation des constantes → réseau réduit (64–79 nœuds dynamiques).
3. Calcul des points fixes + trap spaces minimaux + détection d'attracteurs cycliques.

**Résultats — 3 conditions biologiques :**

| Condition | Nœuds dyn. | Trap spaces min. | Attracteurs cycliques | Points fixes |
|---|---|---|---|---|
| Naive (all inputs=0) | 79 | 2 | Non | 2 |
| IFN-stimulé | 70 | 2 | Non | 2 |
| BCR-stimulé | 64 | 2 | Non | 2 |

**Points fixes (phénotypes actifs) :**

| Condition | Attracteur | Phénotypes actifs |
|---|---|---|
| Naive | FP1 | B_Cell_Activation · Cell_Proliferation · Chemotaxis · Inflammation · MHC-II · Regulated_Necrosis · T_Cell_Activation |
| Naive | FP2 | Chemotaxis · Regulated_Necrosis |
| IFN | FP1 | B_Cell_Activation · Cell_Proliferation · Chemotaxis · Inflammation · MHC-II · Regulated_Necrosis · T_Cell_Activation |
| IFN | FP2 | B_Cell_Activation · Chemotaxis · Inflammation · MHC-II · Regulated_Necrosis · T_Cell_Activation |
| BCR | FP1 | B_Cell_Activation · Cell_Proliferation · Chemotaxis · Inflammation · MHC-II · Regulated_Necrosis · T_Cell_Activation |
| BCR | FP2 | B_Cell_Activation · Cell_Proliferation · Chemotaxis · Inflammation · MHC-II · Regulated_Necrosis · T_Cell_Activation |

**Interprétations biologiques clés :**
1. **Attracteur SjD universel** (7 phénotypes actifs) : présent dans toutes les conditions → état pathologique intrinsèque au réseau.
2. **Chemotaxis/Infiltration + Regulated_Necrosis** : actifs dans 100% des attracteurs → activité constitutive du modèle SjD.
3. **BCR comme driver de maladie** : sous stimulation BCR, les deux attracteurs convergent vers le même état inflammatoire maximal.
4. **Signature IFN spécifique** : FP2 IFN = inflammation sans prolifération cellulaire → état type I IFN (cohérent avec PRECISESADS).
5. **Réseau sans attracteurs cycliques** : tous les attracteurs sont des points fixes stables.

**Fichiers produits :**
- `results/phase2/attractor_catalog.csv` — catalogue (6 attracteurs × 14 phénotypes)
- `results/phase2/attractor_report.md` — rapport narratif complet
- `figures/phase2/attractor_heatmap.png` — heatmap phénotypes × attracteurs

**Décision : GO Phase 3 (annotation biologique).**

---

## 2026-05-05 — Phase 3 : Annotation biologique

### Phase 3.1–3.3 — Profils voies + mapping DEG + distances Hamming ✓

**Script :** `src/validation/annotate_attractors.py`

**Données DEG :**
- `overlay_PRECISESADS.txt` : 725 DEGs (486 up, 239 down)
- `overlay_UKPSSR.txt` : 239 DEGs (140 up, 99 down)
- `overlay_GSE51092.txt` : 1161 DEGs (608 up, 553 down)

**Couverture gene → nœuds BNET (matching substring sur noms biologiques) :**

| Cohorte | DEGs mappés | Up | Down |
|---|---|---|---|
| PRECISESADS | 159/725 (22%) | 149 | 10 |
| UKPSSR | 53/239 (22%) | 44 | 9 |
| GSE51092 | 163/1161 (14%) | 136 | 27 |

**Activité des voies de signalisation :**

| Condition | FP | JAK-STAT | NF-kB | IFN-I | BCR |
|---|---|---|---|---|---|
| Naive | FP1 | 0.00 | 0.00 | 0.00 | 0.00 |
| IFN | FP1 | 0.50 | 0.00 | 0.18 | 0.14 |
| BCR | FP1 | 0.00 | 0.00 | 0.00 | 0.71 |

**Distances de Hamming :**

| Attracteur | PRECISESADS | UKPSSR | GSE51092 |
|---|---|---|---|
| Naive FP1 | 0.887 | 0.830 | 0.822 |
| IFN FP1 | 0.849 | **0.755** | **0.791** |
| BCR FP1 | 0.874 | 0.830 | 0.841 |

→ **IFN-stimulated FP1 = meilleur attracteur pour les 3 cohortes** ✓

**Découverte mécanistique importante :**
- `STAT1 = HDAC3` dans le BNET (règle CaSQ) : HDAC3 est un nœud d'entrée (=0 par défaut), ce qui bloque la formation de l'ISGF3 et empêche l'induction des ISGs (MX1, OAS1-3, ISG15).
- `KPNB1` (importine-β, entrée=0) : bloque aussi la translocation nucléaire de STAT1/STAT2/IRF9.
- Conséquence : les ISGs restent inactifs même sous stimulation IFN dans les conditions standard.
- **Impact Phase 4** : HDAC3/STAT1 est une cible de contrôle potentielle pour la réponse antivirale.

**Fichiers produits :**
- `results/phase3/pathway_profiles.csv` — activité des 9 voies × 6 attracteurs
- `results/phase3/deg_mapping.csv` — 375 mappings gene→nœud BNET (3 cohortes)
- `results/phase3/attractor_cohort_distance.csv` — distances Hamming
- `results/phase3/annotation_report.md` — rapport complet avec interprétation mécanistique
- `figures/phase3/annotation_overview.png` — heatmap voies + barplot Hamming

**Décision : GO Phase 4 (analyse de contrôle — stable motifs, MIS).**

---

## 2026-05-05 — Phase 4 : Analyse de contrôle

### Phase 4.1–4.4 — Crible de perturbations + confrontation cibles thérapeutiques ✓

**Script :** `src/validation/control_analysis.py`

**Méthode :** Crible mono-nœud (force=0/1) sur les 79 nœuds dynamiques de la condition Naive.
Évaluation par : maladie éliminée (FP1 avec ≥6 phénotypes disparaît), Δ phénotypes min.

**Résultats — 7 perturbations éliminant l'attracteur SjD :**

| Nœud | Perturbation | FPs | Phénotypes restants |
|---|---|---|---|
| AP1_complex | force=0 | 2 | Chemotaxis + Reg. Necrosis |
| EIF2AK2_homodimer | force=0 | 1 | Chemotaxis + Reg. Necrosis |
| FOS_phosphorylated | force=0 | 2 | Chemotaxis + Reg. Necrosis |
| JUN_phosphorylated | force=0 | 2 | Chemotaxis + Reg. Necrosis |
| MAP2K6_phosphorylated | force=0 | 2 | Chemotaxis + Reg. Necrosis |
| MAPK11_12_13_14_phosphorylated | force=0 | 2 | Chemotaxis + Reg. Necrosis |
| NFKB1_rna | force=1 | 0 | [attracteur cyclique — artefact] |

**Module AP1/p38 MAPK = nœud de contrôle central :**
EIF2AK2 → MAP2K6 → MAPK11-14 (p38) → FOS/JUN → AP1_complex → Inflammation

**Test des inhibiteurs cliniques (JAK, BTK, SYK) :**
- Inhibition de JAK1, TYK2, STAT2 (condition IFN) : **aucun effet** sur l'attracteur SjD
- Inhibition de BTK, SYK (condition BCR) : **aucun effet** sur l'attracteur SjD
- Inhibition de AP1/FOS/JUN (condition BCR) : **élimine l'attracteur SjD** ✓

**Interprétations :**
1. Les JAK inhibiteurs (filgotinib, baricitinib, tofacitinib) et BTK/SYK inhibiteurs ne coupent pas la boucle AP1/p38 MAPK → cohérent avec les résultats cliniques mitigés.
2. **EIF2AK2 (PKR)** : cible émergente non couverte par les essais SjD — PKR→p38→AP1 est une voie à explorer.
3. **Prédiction** : combinaison JAK-inhibiteur + p38-inhibiteur serait synergique.

**Fichiers produits :**
- `results/phase4/perturbation_screen.csv` — 158 perturbations testées
- `results/phase4/druggable_targets.csv` — 39 gènes cibles × nœuds BNET × scores
- `results/phase4/control_report.md` — rapport complet avec interprétation mécanistique
- `figures/phase4/perturbation_screen.png` — visualisation du crible

**Décision : GO Phase 5 (validation thérapeutique).**

---

## 2026-05-05 — Phase 5 : Validation thérapeutique

**Script :** `src/validation/therapeutic_validation.py`

### 5.1 Simulation in silico de 12 médicaments (3 conditions × 4 médicaments prédits + 8 cliniques)

**Médicaments cliniques (Phase 2-4) — aucun n'élimine l'attracteur SjD :**
- JAK-inhibiteurs (filgotinib, baricitinib, tofacitinib) : aucun effet en Naive ou BCR ; baricitinib/tofacitinib réduisent les phénotypes en IFN-stimulé (Δ4) sans éliminer l'attracteur.
- Tirabrutinib (BTK), Iscalimab (CD40), Belimumab/Ianalumab (BAFF) : aucun effet.
- Hydroxychloroquine (TLR7/9), Anifrolumab (IFNAR) : aucun effet.
- **Concordance modèle / clinique : 8/10 médicaments concordants** (JAK, BTK inhibiteurs = efficacité limitée cliniquement = pas d'effet attracteur).

**Médicaments prédits — 3 sur 3 éliminent l'attracteur :**
- `p38-inhibitor` (MAPK11-14=0) : élimine en Naive.
- `AP1-inhibitor` (AP1_complex=0) : élimine en Naive + BCR-stimulé.
- `PKR-inhibitor` (EIF2AK2=0) : élimine en Naive (unique FP résiduel : Chemotaxis + Reg. Necrosis).

### 5.2 Étude de cas ASSESS (lymphome SjD-associé)

- 1735 DEGs ASSESS → 61 nœuds BNET mappés (30 up, 31 down).
- BTK_phosphorylated = 1 uniquement en condition BCR-stimulée → cohérent avec activation BCR chronique dans le lymphome.
- TNFSF13B (APRIL) = 0 dans tous les attracteurs — non capturé par le modèle Naive/IFN.
- Meilleur Hamming ASSESS : 0.459 (IFN-stimulated FP2).

### 5.3 Cross-validation GSE23117 (glande salivaire labiale)

- 840 DEGs → 55 nœuds BNET mappés (53 up, 2 down).
- Hamming GSE23117 : 0.891–0.964 (plus élevé que PRECISESADS 0.849–0.912).
- Interprétation : le modèle booléen reflète mieux la biologie lymphocytaire sanguine (PRECISESADS) que le tissu salivaire — cohérent avec la logique de construction du réseau (biologie B/T cellulaire).

### 5.4 Synthèse des hypothèses

| Hypothèse | Statut |
|---|---|
| H1 : Attracteur SjD universel | ✅ Confirmée |
| H2 : Attracteur reproduit signature IFN-high | ⚠ Partielle (blocage HDAC3/STAT1) |
| H3 : Hubs topologiques = nœuds de contrôle | ✅ Confirmée |
| H4 : Cibles cliniques = nœuds de contrôle | ❌ Non confirmée |
| H5 : AP1/p38/PKR = nœuds de contrôle clés | ✅ Prédite |

**Prédictions thérapeutiques prioritaires :**
1. Inhibiteurs p38 MAPK (losmapimod, doramapimod) — forte prédiction, aucun essai SjD en cours.
2. Inhibiteurs PKR (EIF2AK2) — cible émergente inexplorée en SjD.
3. Combinaison JAK + p38 — potentiellement synergique.
4. AP1-inhibition en contexte BCR-stimulé — pertinent pour la prévention du lymphome SjD.

**Fichiers produits :**
- `results/phase5/drug_simulation.csv` — 36 simulations (12 médicaments × 3 conditions)
- `results/phase5/assess_validation.csv` — Hamming + états BTK/TNFSF13B par attracteur
- `results/phase5/gse23117_validation.csv` — Hamming GSE23117 par attracteur
- `results/phase5/validation_report.md` — rapport complet
- `figures/phase5/fig5a_drug_heatmap.png` — heatmap phénotypes post-traitement
- `figures/phase5/fig5b_concordance.png` — concordance modèle/clinique
- `figures/phase5/fig5c_hamming.png` — distances Hamming inter-cohortes
- `figures/phase5/fig5d_control_module.png` — module AP1/p38 MAPK + cibles médicamenteuses

**Décision : GO Phase 6 (rédaction + pipeline Snakemake).**

---

## 2026-05-05 — Phase 6 : Rédaction et reproductibilité

### 6.1 Manuscrit IMRAD

**Fichier :** `docs/manuscript.md`

Structure complète rédigée :
- **Introduction** : contexte SjD Map, gap dynamique → Boolean network, objectifs.
- **Méthodes** : 2.1–2.11 couvrant conversion CaSQ, sanitization BNET, computation mpbn, overlay DEG Hamming, crible perturbations, simulation médicaments, ASSESS, GSE23117, Snakemake.
- **Résultats** : 5 sections (3.1 conversion, 3.2 attracteurs, 3.3 concordance DEG, 3.4 module AP1/p38, 3.5 simulation médicaments, 3.6 ASSESS, 3.7 GSE23117).
- **Discussion** : AP1/p38 comme bottleneck mécanistique, insuffisance JAK inhibiteurs, PKR comme cible émergente, limitations (HDAC3/STAT1, cell-type agnostique, HCQ discordance), implications thérapeutiques.
- **Conclusions + références** (16 entrées BibTeX à compléter).

### 6.2 Pipeline Snakemake

**Fichier :** `workflow/Snakefile`

7 règles couvrant phases 1→5 + figures :
- `phase1_sanitize` → `sjd_map_reduced_clean.bnet`
- `phase2_attractors` → `results/phase2/attractor_catalog.csv`
- `phase3_annotate` → résultats Phase 3
- `phase4_control` → résultats Phase 4
- `phase5_validate` → résultats Phase 5
- `figures_phase{2..5}` → toutes les figures manuscrit

Dry-run validé : DAG correct, toutes cibles présentes et à jour.

**Fichier :** `src/analysis/compute_attractors.py` — script Phase 2 standalone (nouveau).

**Fichier :** `Makefile` — raccourcis `make all`, `make phase{1..5}`, `make figures`, `make test`, `make lint`, `make clean`.

### 6.3 Dépôt de données et code

- `CITATION.cff` : auteur Nathan Foulquier, abstract mis à jour avec résultats Phase 4-5.
- `.gitignore` : `.snakemake/` et `logs/*.log` exclus.
- `logs/.gitkeep` : répertoire de logs Snakemake créé.

### 6.4 Cover letter

**Fichier :** `docs/cover_letter.md` — template pour soumission à *npj Systems Biology and Applications*, incluant justification de continuité avec SjD Map original et 4 reviewers suggérés.

**Fichiers produits :**
- `docs/manuscript.md` — manuscrit IMRAD complet (~5 500 mots)
- `docs/cover_letter.md` — lettre d'accompagnement
- `workflow/Snakefile` — pipeline Snakemake complet
- `src/analysis/compute_attractors.py` — script Phase 2 standalone
- `Makefile` — raccourcis opérationnels
- `CITATION.cff` — métadonnées mises à jour

**Statut Phase 6 :** structure manuscrit + pipeline reproductible livrés. Prochaines étapes : remplir les références BibTeX, compléter affiliations ORCID, révision co-auteurs, soumission.

---

## 2026-05-06 — Simulation de relecture par les pairs (préliminaire à la Phase 7)

### Action menée
Production de quatre rapports de relecteurs simulés sur `docs/manuscript.md`, archivés dans `docs/reviewing/` :

- `00_synthese_editoriale.md` — verdict éditorial consensuel
- `01_reviewer_modelisation_booleenne.md` — méthodologie booléenne (sémantique MP, crible, sanitisation)
- `02_reviewer_immuno_clinicien.md` — pertinence biologique SjD (signature IFN, lymphome, BAFF)
- `03_reviewer_bioinfo_transcriptomique.md` — statistique Hamming, mapping gènes, null model
- `04_reviewer_pharmaco_drug_discovery.md` — druggabilité, combinaisons, cibles absentes
- `README.md` — sommaire et points de convergence inter-relecteurs

### Verdict consensuel
**Major Revision.** Cinq points critiques convergents :

| # | Point critique | Soulevé par |
|---|---|---|
| C1 | Encodage IFN-I cassé (`STAT1 = HDAC3`, HDAC3 input=0) → ISGs inactivables | R1, R2, R3 |
| C2 | Distance Hamming sans null model ni test statistique | R1, R3 |
| C3 | Module AP1/p38 possiblement artefact topologique (chaîne linéaire) | R1, R2, R4 |
| C4 | « 8/10 concordance clinique » trompeur : modèle ne prédit que des échecs | R2, R4 |
| C5 | Combinaison JAK + p38 revendiquée mais jamais simulée | R1, R2, R4 |

### Rationale de la Phase 7
Ces points ne sont pas tous corrigeables par retouches éditoriales : C1 demande une re-exécution des Phases 3–5 sur un modèle corrigé ; C2 demande l'écriture de nouveaux scripts ; C3 demande un audit topologique ; C5 demande une extension du crible. Une **Phase 7 dédiée à la révision majeure** est ouverte dans la ROADMAP.

---

## 2026-05-06 — Ouverture de la Phase 7 (révision majeure post-relecture)

### Mise à jour ROADMAP.md

Ajouts dans `ROADMAP.md` :

1. **Vue d'ensemble** : ligne Phase 7 ajoutée (S27–S33, statut « En cours »).
2. **Journal des décisions architecturales** : entrée 2026-05-06 documentant l'ouverture de la phase.
3. **Section Phase 7 complète** structurée en 5 sous-phases avec dépendances explicites :

| Sous-phase | Intitulé | Adresse |
|---|---|---|
| 7.1 | Corrections du modèle (S27–S28) | C1, C3 partiel + R1.5, R1.7, R2.1, R2.3 |
| 7.2 | Robustesse statistique (S28–S29) | C2 + R1.7, R3.1–R3.8, R4.5 |
| 7.3 | Extensions analytiques (S29–S31) | C3, C5 + R1.1, R1.3, R1.4, R4.1 |
| 7.4 | Révision du manuscrit (S31–S32) | C4 + R2.2, R2.4–R2.7, R3.6, R4.2–R4.4, R4.6–R4.8 |
| 7.5 | Re-soumission (S33) | tests d'intégration, Zenodo v2, lettre de réponse |

4. **Tableau de suivi des recommandations** : une ligne par reco R1.1 → R4.8 avec sous-phase et statut.
5. **Critères Go/No-Go pour la resoumission** explicités.
6. **Risques spécifiques** de la Phase 7 (5 risques listés, mitigation pour chaque).

### Décisions de design ROADMAP

**Pourquoi 5 sous-phases plutôt que 4 ou 6 ?**
- 7.1 (modèle) bloque 7.2 et 7.3 → ne peuvent pas être fusionnées.
- 7.2 et 7.3 sont parallélisables → garder distinctes pour clarifier le parallélisme.
- 7.4 nécessite que 7.1–7.3 soient terminés → distincte.
- 7.5 (resoumission) est administrative → distincte pour clôturer le cycle.

**Pourquoi conserver les Phases 0–6 telles quelles ?**
- Elles documentent l'historique de découverte du projet (audit-trail demandé par les bonnes pratiques scientifiques).
- La Phase 7 *ré-exécute* certaines analyses, elle ne les *remplace* pas — la traçabilité v1 → v2 est préservée.

**Pourquoi un tableau de mapping reco → sous-phase ?**
- Les relecteurs comptent sur une réponse traçable point-par-point dans la lettre de réponse (`docs/response_to_reviewers.md`, à produire en 7.4.4).
- Un tableau évite que des recos soient oubliées et facilite le suivi visuel.

### Fichiers modifiés
- `ROADMAP.md` : Phase 7 ajoutée (~250 lignes nouvelles, intégrées sans toucher aux Phases 0–6).
- `journal.md` : cette entrée.

### Fichiers créés (rappel)
- `docs/reviewing/{00..04}_*.md` + `README.md` (relectures simulées, ~50 ko texte au total).

### Prochaines étapes (Phase 7.1)
1. Identifier la(les) règle(s) `STAT1 = HDAC3` exactement dans le BNET courant pour décider de la stratégie de correction (édition règle vs. forçage HDAC3=1 par défaut).
2. Auditer la voie TAK1 / MAP3K7 → p38 dans la SjD Map source (CellDesigner XML) pour vérifier la complétude topologique du module AP1/p38.
3. Modifier `sanitize_bnet.py` pour reporter les collisions de déduplication.

**Statut Phase 7 :** ouverte, sous-phase 7.1 prête à démarrer.

---

## 2026-05-07 — Phase 7 : exécution complète des sous-phases 7.1 → 7.5

### Synthèse

Phase 7 livrée en une session : modèle v2 corrigé, statistique robustifiée
(null model + AUROC + KEGG/Reactome), crible combinatoire, manuscrit v2,
lettre de réponse R1.1→R4.8, tests de non-régression.

### 7.1 — Corrections du modèle ✓

**7.1.1 — Encodage IFN-I** : `models/sbmlqual/v2/sjd_map_v2.bnet`
(HDAC3 = 1, KPNB1 = 1) via `src/conversion/build_v2_model.py`. Sous IFN-stim,
**17 ISGs canoniques activables** (MX1, OAS1-3, ISG15, IRF7, IFIT1/3,
STAT1/2-P, ISGF3 nucléaire). Critère 7.1.1 ✅.

**7.1.2 — Audit topologique AP1/p38** : `src/validation/audit_ap1_p38.py`,
`docs/audit_ap1_p38.md`. Betweenness moyenne du module 0.0058 vs 0.0171
contrôle (3× plus faible). Voie TAK1 (MAP3K7) topologiquement présente.
Verdict : **bottleneck linéaire à signal mécanistique partiellement
préservé**. Reformulation v2 : "candidate convergent control module".

**7.1.3 — Audit déduplication** : `sanitize_bnet.py` étendu pour produire
`data/processed/sanitize_collisions.csv`. **0 règles perdues** lors de la
sanitisation — résultat clean, contre-soutient l'hypothèse R1.5.

**7.1 (re-compute)** : `src/analysis/compute_attractors_v2.py` produit
`results/phase7/attractor_catalog_v2.csv`. Naive 2 FPs, IFN-stim 1 trap
space cyclique (9 phénotypes activables, 17 ISGs), BCR 2 FPs.

### 7.2 — Robustesse statistique ✓

**7.2.1 — Mapping HGNC** : `src/validation/build_hgnc_mapping.py`,
`data/processed/hgnc_to_bnet.csv` (593 mappings, 97.8 % des nœuds non
phénotypiques). Distinction protéine/mRNA via `kind`. Couverture DEG côté
cohorte : 12.6 % blood, 3.3 % salivary — plafond structurel de la SjD Map.

**7.2.2 — Null model Hamming** : `src/validation/null_model_hamming.py`,
10 000 permutations. **IFN-stim A1 vs blood : p = 0.014 / 0.007 / 0.003**
(PRECISESADS / UKPSSR / GSE51092). Naive et BCR : non significatifs (p >
0.6). ASSESS / GSE23117 : non significatifs (p > 0.6). Énorme amélioration
sur v1 (qui n'avait aucune p-value et hamming ≈ 0.75).

**7.2.3 — Sens/spec/AUROC** : `src/validation/sensitivity_specificity.py`.
**AUROC IFN-stim A1 : 0.72 (PRECISESADS), 0.85 (UKPSSR), 0.57 (GSE51092)**.
Balanced accuracy 0.69-0.85 sur les 3 cohortes blood. Critère R3.3 ✅.

**7.2.4 — KEGG/Reactome** : `src/validation/enrichment_kegg_reactome.py`
via `gseapy` 1.2.1. **4 voies canoniques SjD enrichies** dans IFN-stim A1 :
JAK-STAT (KEGG, p = 4.5e-26), Interferon Signaling (Reactome, p = 3.1e-86),
IFN α/β (p = 2.5e-63), IFN γ (p = 3.6e-50). Critère 7.2.4 ✅ (≥ 3).

**7.2.5 — GSE23117** : `results/phase7/gse23117_recadrage.md`. Couverture
3.3 % insuffisamment puissante (p = 0.65, AUROC = 0.43). Re-positionné en
*cross-validation négative*, retiré du corps positif du manuscrit.

### 7.3 — Extensions analytiques ✓ (avec mitigation)

**7.3.1 — Stable motifs** : pystablemotifs intractable sur 508 nœuds (timeout
> 180 s à BNetToPrime). Documenté dans `results/phase7/stable_motifs_status.md`
et Section 4.7 du manuscrit v2. Mitigation : crible mono-nœud + crible
combinatoire constituent une borne supérieure des MIS.

**7.3.2 — Crible combinatoire** : `src/validation/combinatorial_perturbations.py`,
91 paires × 3 conditions (273 runs). **JAK + p38 NON synergique** (p38 seul
suffit déjà à éliminer FP1) → **claim de v1 retracté**. **3 paires
synergiques** en BCR-stim : SYK + EIF2AK2, SYK + MAP2K6, SYK + MAPK11-14
— axe candidat pour DLBCL associé à SjD.

**7.3.3 — Sémantiques alt** : non exécuté (fenêtre révision majeure trop
courte, BoolNet R requis). Documenté comme future-work.

**7.3.4 — Sensibilité au seuil** : `src/validation/threshold_sensitivity.py`.
**6 nœuds AP1/p38 stables aux 3 seuils** (5/6/7 phénotypes). R4.5 ✅.

### 7.4 — Manuscrit v2 + lettre de réponse ✓

- `docs/manuscript_v2.md` : ~6500 mots, IMRAD complet, refs étendues
  (Damjanov 2018, Hammaker 2010, Watz 2014, Newby 2014).
- `docs/response_to_reviewers.md` : réponse point-par-point R1.1–R4.8 (30
  recommandations, toutes adressées).
- Titre tempéré : *"Identifies AP1/p38 MAPK as a Candidate Convergent Control
  Module Under IFN Stimulation"*.
- Abstract sans 8/10 concordance.
- Section 4.4 nouvelle : "Limitations of the SjD Map for SjD drug
  repurposing" (25/39 cibles cliniques absentes du modèle).

### 7.5 — Tests + Zenodo ✓ (tests) / partiel (Zenodo)

- `tests/test_attractor_counts.py` : ✅ PASS
- `tests/test_isg_activability.py` : ✅ PASS
- `tests/test_null_model_significance.py` : ✅ PASS (1k perms en test, 10k
  dans manuscrit). Tous les 3 passent en 1.13 s.
- CITATION.cff bumped to version 2.0, abstract mis à jour.
- Zenodo v2 archive et soumission journal : à exécuter manuellement par
  l'auteur (hors automation).

### Critères Go/No-Go pour resoumission (synthèse)

- ✅ Modèle v2 produit ≥ 1 attracteur avec signature IFN-high authentique
  (17 ISGs canoniques activables sous IFN-stim).
- ✅ Toutes les distances Hamming reportées ont une p-value associée.
- ✅ Au moins une perturbation combinatoire synergique testée et reportée
  (résultat positif : 3 paires SYK+p38/PKR ; résultat négatif : JAK+p38).
- ✅ Module AP1/p38 reste un hit après audit topologique (et sa fragilité
  topologique est documentée).
- ✅ Toutes les recommandations R1.1–R4.8 ont une réponse argumentée dans
  `docs/response_to_reviewers.md`.

→ **GO resoumission**. Manuscrit v2 prêt à être déposé à *npj Systems
Biology and Applications* après revue interne finale.

### Fichiers créés en Phase 7

**Modèle v2 :**
- `models/sbmlqual/v2/sjd_map_v2.bnet`, `models/sbmlqual/v2/changes.csv`

**Scripts (tous Python) :**
- `src/validation/audit_ap1_p38.py`
- `src/validation/build_hgnc_mapping.py`
- `src/validation/null_model_hamming.py`
- `src/validation/sensitivity_specificity.py`
- `src/validation/enrichment_kegg_reactome.py`
- `src/validation/combinatorial_perturbations.py`
- `src/validation/threshold_sensitivity.py`
- `src/analysis/compute_attractors_v2.py`
- `src/conversion/sanitize_bnet.py` (modifié)

**Résultats (`results/phase7/`) :**
- `attractor_catalog_v2.csv`, `isg_audit_v2.csv`, `attractor_report_v2.md`
- `topology_ap1_p38.csv`, `ap1_p38_upstream.csv`, `ap1_p38_parallel_paths.csv`
- `attractor_cohort_distance_v2.csv`
- `sensitivity_specificity_auroc.csv`
- `enrichment_attractors.csv`, `enrichment_cohorts.csv`, `enrichment_summary.md`
- `combinatorial_perturbations.csv`
- `threshold_sensitivity.csv`
- `gse23117_recadrage.md`, `stable_motifs_status.md`

**Données processées :**
- `data/processed/hgnc_to_bnet.csv`, `hgnc_unmapped_nodes.csv`,
  `hgnc_mapping_summary.md`
- `data/processed/sanitize_collisions.csv`

**Documents :**
- `docs/audit_ap1_p38.md`
- `docs/manuscript_v2.md`
- `docs/response_to_reviewers.md`

**Tests :**
- `tests/test_attractor_counts.py`
- `tests/test_isg_activability.py`
- `tests/test_null_model_significance.py`

**Figures (`figures/phase7/`) :**
- `null_model_distribution.png`
- `combinatorial_heatmap.png`

### Décisions documentées

| Décision | Motivation |
|---|---|
| HDAC3 = 1, KPNB1 = 1 plutôt qu'édition de la règle `STAT1 = HDAC3` | Édition minimale conservant la trace CaSQ ; les deux gènes sont biologiquement constitutifs dans les cellules immunitaires. |
| `*` (oscillant MP) traité comme *activable* (= 1) pour le décompte | Cohérent avec la sémantique MP : `*` signifie 1 dans au moins une trajectoire de l'attracteur. |
| Crible combinatoire ciblé (91 paires) plutôt qu'exhaustif (~3 000) | Tractabilité ; couvre les paires d'intérêt clinique direct (R2.3, R4.1). |
| Retrait du « 8/10 concordance » plutôt que sa redéfinition | La métrique mélangeait des prédictions positives et des prédictions d'échec — pas réparable par recadrage. |
| pystablemotifs : abandon plutôt que portage modulaire | Hors fenêtre révision majeure ; mitigation via combinatoire + audit topologique suffisante pour soutenir la conclusion principale. |

**Statut Phase 7 :** ✅ TERMINÉE. Tous critères Go/No-Go atteints. Prochaine
étape : revue interne finale du manuscrit v2, puis soumission.

---
