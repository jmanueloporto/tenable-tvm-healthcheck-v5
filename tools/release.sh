#!/bin/bash
NEW_VERSION=$1
if [ -z "$NEW_VERSION" ]; then
    echo "[!] Uso: ./tools/release.sh <version>"
    exit 1
fi
echo "[*] Actualizando sistema a v$NEW_VERSION..."
# Actualizar versiones en cabeceras .py
find . -name "*.py" -not -path "./.venv/*" -exec sed -i "s/VERSION: .*/VERSION: $NEW_VERSION/" {} +
# Actualizar README
sed -i "s/Current Version:.*/Current Version: $NEW_VERSION/" README.md
# Git Flow & Push
git add .
git commit -m "Release version v$NEW_VERSION"
git tag -a "v$NEW_VERSION" -m "Stable release v$NEW_VERSION"
git push origin main --tags
echo "============================================================"
echo "[SUCCESS] Proyecto publicado en GitHub como v$NEW_VERSION"
echo "============================================================"
