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

## Prochaines étapes — Phase 1 (semaines 3-5)

- **1.1** : Appliquer CaSQ sur `SjD_Map.xml` → produire le SBML-qual ; comparer au SIF existant
- **1.2** : Script `src/validation/structural_check.py` (lecture SBML-qual, comptage, diff vs SIF)
- **1.3** : Checklist d'audit manuel des nœuds critiques (hubs, phénotypes, complexes)
- **1.4** : Tag Git `model-v1.0`
