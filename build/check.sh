#!/bin/bash
# 用法: build/check.sh <build_script.py> <slug> [svg names to screenshot...]
set -e
cd "$(dirname "$0")"
python3 -I "$1" | tail -2
cd ..
export NODE_PATH=/opt/node22/lib/node_modules:/usr/local/lib/node_modules_global
OUT=${OUT:-/tmp/shots}; mkdir -p $OUT
node build/render_check.js docs/$2.html | tr -d '\n '; echo
shift 2
files=(); for f in "$@"; do files+=("docs/svg/${SLUGDIR}/$f.svg"); done
[ ${#files[@]} -gt 0 ] && OUT=$OUT timeout 120 node $SHOT "${files[@]}" || true
