#!/usr/bin/env bash
# bowser-ai-lite · Instala el kit en esta máquina (Linux, macOS o WSL) y deja el comando `bowser` en el PATH.
#
#   curl -fsSL https://raw.githubusercontent.com/orestesmedina/bowser-spec-ai-lite/main/install.sh | bash
#   curl -fsSL …/install.sh | bash -s -- v0.9.0      (una versión concreta)
#
# Variables opcionales: BOWSER_REPO (de dónde clonar), BOWSER_HOME (dónde queda el kit, por defecto
# ~/.bowser-ai-lite) y BOWSER_BIN (dónde queda el comando, por defecto ~/.local/bin).
set -euo pipefail

REPO="${BOWSER_REPO:-https://github.com/orestesmedina/bowser-spec-ai-lite.git}"
DIR="${BOWSER_HOME:-$HOME/.bowser-ai-lite}"
BIN="${BOWSER_BIN:-$HOME/.local/bin}"
PEDIDA="${1:-}"

falla() { echo "✗ $1" >&2; exit 1; }
for programa in git python3; do
  command -v "$programa" >/dev/null 2>&1 || falla "Falta '$programa'. Instálalo y vuelve a correr este comando."
done
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' || falla "Hace falta Python 3.9 o más nuevo."

if [ -d "$DIR/.git" ]; then
  git -C "$DIR" fetch -q --tags origin || falla "No pude actualizar $DIR desde $REPO."
else
  [ -e "$DIR" ] && falla "$DIR ya existe y no es una copia del kit. Bórrala o usa BOWSER_HOME=otra/ruta."
  git clone -q "$REPO" "$DIR" || falla "No pude clonar $REPO."
fi
# El permiso de ejecución que se da abajo no cuenta como un cambio local de la copia.
git -C "$DIR" config core.fileMode false

VERSION="$PEDIDA"
[ -z "$VERSION" ] && VERSION="$(git -C "$DIR" tag -l 'v*' --sort=-v:refname | head -1)"
if [ -n "$VERSION" ]; then
  git -C "$DIR" -c advice.detachedHead=false checkout -q "$VERSION" || falla "No existe la versión $VERSION."
else
  # Sin versiones publicadas todavía: la rama principal.
  git -C "$DIR" checkout -q main 2>/dev/null || git -C "$DIR" checkout -q master
  git -C "$DIR" pull -q --ff-only
fi

mkdir -p "$BIN"
chmod +x "$DIR/bin/bowser"
ln -sf "$DIR/bin/bowser" "$BIN/bowser"

echo "✓ bowser-ai-lite $(cat "$DIR/VERSION") instalado en $DIR"
case ":$PATH:" in
  *":$BIN:"*) ;;
  *) echo "⚠ $BIN no está en tu PATH. Agrega esta línea a ~/.bashrc (o ~/.zshrc) y abre otra terminal:"
     echo "    export PATH=\"$BIN:\$PATH\"" ;;
esac
echo
echo "En la carpeta de un proyecto:  bowser init     (o: bowser init --skills go,react,postgres)"
echo "Para actualizar después:       bowser update"
