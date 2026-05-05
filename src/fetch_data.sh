#!/usr/bin/env bash
# Télécharge les données SjD Map depuis Zenodo et le dépôt GitLab,
# vérifie les checksums, et place les fichiers sous data/raw/.
#
# Usage :  bash src/fetch_data.sh
# Prérequis : curl, git, sha256sum

set -euo pipefail

ZENODO_DOI="10.5281/zenodo.17585308"
ZENODO_BASE="https://zenodo.org/api/records"
GITLAB_REPO="https://gitlab.com/genhotel/TheSjDMap.git"

RAW_DIR="data/raw"
CHECKSUMS_FILE="$RAW_DIR/CHECKSUMS.txt"

echo "=== Phase 0.3 — Récupération SjD Map ==="

# --- Zenodo ------------------------------------------------------------------
echo "[1/3] Résolution du DOI Zenodo : $ZENODO_DOI"
RECORD_ID=$(curl -fsSL "https://doi.org/${ZENODO_DOI}" -o /dev/null -w '%{url_effective}' \
  | grep -oP 'records/\K[0-9]+' || true)

if [[ -z "$RECORD_ID" ]]; then
  echo "WARN : impossible de résoudre automatiquement l'ID Zenodo."
  echo "       Le dépôt est peut-être encore privé (article 2026 pré-publication)."
  echo "       Télécharger manuellement depuis https://doi.org/${ZENODO_DOI}"
  echo "       et placer les fichiers dans $RAW_DIR/zenodo_manual/"
else
  echo "       ID Zenodo résolu : $RECORD_ID"
  DEST="$RAW_DIR/zenodo_${RECORD_ID}"
  mkdir -p "$DEST"

  METADATA=$(curl -fsSL "${ZENODO_BASE}/${RECORD_ID}")
  FILES=$(echo "$METADATA" | python3 -c \
    "import sys, json; [print(f['links']['self'], f['key']) for f in json.load(sys.stdin)['files']]")

  while IFS=' ' read -r url filename; do
    echo "       Téléchargement : $filename"
    curl -fsSL "$url" -o "$DEST/$filename"
  done <<< "$FILES"

  echo "[2/3] Calcul des checksums SHA-256"
  (cd "$DEST" && sha256sum -- * >> "../../$CHECKSUMS_FILE")
  echo "       Checksums écrits dans $CHECKSUMS_FILE"
fi

# --- GitLab ------------------------------------------------------------------
echo "[3/3] Clonage du dépôt GitLab (référence HEAD figée par commit)"
GITLAB_DEST="$RAW_DIR/TheSjDMap_git"

if [[ -d "$GITLAB_DEST/.git" ]]; then
  echo "       Dépôt déjà présent, mise à jour..."
  git -C "$GITLAB_DEST" pull --ff-only
else
  git clone --depth=1 "$GITLAB_REPO" "$GITLAB_DEST"
fi

COMMIT_HASH=$(git -C "$GITLAB_DEST" rev-parse HEAD)
echo "       Commit figé : $COMMIT_HASH"
echo "GitLab TheSjDMap HEAD $COMMIT_HASH" >> "$CHECKSUMS_FILE"

echo ""
echo "=== Terminé. Contenu de $RAW_DIR : ==="
ls -lh "$RAW_DIR/"
