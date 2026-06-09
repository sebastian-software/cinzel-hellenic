#!/bin/sh
set -e

SOURCE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT_DIR=$(CDPATH= cd -- "$SOURCE_DIR/.." && pwd)
UFO="CinzelHellenic-Regular.ufo"
FONT_BASENAME="CinzelHellenic-Regular"
TTF_DIR="$ROOT_DIR/fonts/ttf"
WOFF2_DIR="$ROOT_DIR/fonts/woff2"
TTF_PATH="$TTF_DIR/$FONT_BASENAME.ttf"
WOFF2_PATH="$WOFF2_DIR/$FONT_BASENAME.woff2"

cd "$SOURCE_DIR"

rm -rf "$TTF_DIR" "$WOFF2_DIR"
mkdir -p "$TTF_DIR" "$WOFF2_DIR"

echo "Building $FONT_BASENAME.ttf"
fontmake -u "$UFO" -o ttf --output-dir "$TTF_DIR"

if [ ! -f "$TTF_PATH" ]; then
  echo "Expected $TTF_PATH but fontmake did not create it" >&2
  exit 1
fi

echo "Building $FONT_BASENAME.woff2"
python3 - "$TTF_PATH" "$WOFF2_PATH" <<'PY'
import sys
from fontTools.ttLib import TTFont

source, target = sys.argv[1], sys.argv[2]
font = TTFont(source)
font.flavor = "woff2"
font.save(target)
PY

rm -rf master_ufo instance_ufo instance_ufos

echo "Done"
