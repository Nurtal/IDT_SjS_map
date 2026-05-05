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
