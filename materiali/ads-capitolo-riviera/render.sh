#!/usr/bin/env bash
# Rasterizza gli HTML di una cartella con Chrome headless: *_916* a 1080x1920, il resto a 1080x1350.
set -euo pipefail
C="${CHROME_BIN:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
cd "$1"
for f in *.html; do
  S=1080,1350; if [[ "$f" == *_916* ]]; then S=1080,1920; fi
  "$C" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --virtual-time-budget=2500 --window-size=$S --screenshot="${f%.html}.png" "file://$PWD/$f" 2>/dev/null
done
echo "render ok"
