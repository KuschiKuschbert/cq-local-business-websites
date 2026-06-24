#!/bin/bash
# Wrapper to execute run-audit.py and enforce exit codes

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/run-audit.py"
exit $?
