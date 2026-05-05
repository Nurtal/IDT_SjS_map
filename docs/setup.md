# Installation et mise en place de l'environnement

## Prérequis

- Linux ou macOS (recommandé)
- Conda / Mamba (https://docs.conda.io/)
- Java ≥ 17 (géré automatiquement par le fichier `environment.yml`)
- Git

## Option A — Conda (recommandé)

```bash
# Cloner le dépôt
git clone https://gitlab.com/<votre-fork>/SjD-BoolAttractors.git
cd SjD-BoolAttractors

# Créer l'environnement (utiliser mamba pour accélérer la résolution)
mamba env create -f environment.yml
conda activate sjd-boolattractors

# Vérifier les installations clés
python -c "import casq; print('CaSQ OK')"
python -c "import biolqm; print('bioLQM OK')"
python -c "import PyBoolNet; print('PyBoolNet OK')"
python -c "import pystablemotifs; print('pystablemotifs OK')"
```

## Option B — Colomoto Docker notebook (alternative officielle)

Le conteneur Colomoto est maintenu par les auteurs des outils (Naldi et al.) et embarque
CaSQ, bioLQM, PyBoolNet, MaBoSS, pystablemotifs dans un notebook Jupyter pré-configuré.

```bash
# Installer Docker (https://docs.docker.com/engine/install/)
docker pull colomoto/colomoto-docker:latest

# Lancer le notebook (monter le répertoire courant)
docker run -v "$(pwd):/notebook" -p 8888:8888 colomoto/colomoto-docker:latest
```

## Mise à jour du lockfile

Pour reproduire l'environnement exact (avec versions figées) :

```bash
conda env export --no-builds > environment.lock.yml
```

Ce fichier `environment.lock.yml` doit être versionné à chaque changement significatif
des dépendances et joint à toute archive Zenodo.

## Données brutes

Les données SjD Map ne sont pas incluses dans le dépôt Git (fichiers > 50 Mo).
Voir la Phase 0.3 de la ROADMAP.md et les instructions dans `data/raw/CHECKSUMS.txt`
une fois les fichiers téléchargés.

## Lancer les tests

```bash
pytest tests/ -v
```
