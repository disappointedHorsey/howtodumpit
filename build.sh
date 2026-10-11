#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
[ -d .venv ] || { python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt; }
.venv/bin/python build.py
# preview: (cd public && python3 -m http.server 8000)
