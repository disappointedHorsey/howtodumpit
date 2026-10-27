#!/usr/bin/env bash
# Pre-push gate: build, then the comms/rationality check and the mobile check. Both must exit 0.
# Usage: scripts/prepush.sh [--shots DIR]   (runs automatically as the git pre-push hook, see .githooks/pre-push)
set -euo pipefail
cd "$(dirname "$0")/.."
./build.sh
echo "== consistency_check =="
python3 scripts/consistency_check.py
echo "== mobile_check =="
/workspace/.mobile-venv/bin/python scripts/mobile_check.py "$@"
echo "prepush: all checks passed"
