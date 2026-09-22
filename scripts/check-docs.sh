#!/usr/bin/env bash
set -euo pipefail

# Entry point kept for humans and agents; the rules live in check_docs.py.
exec python3 "$(dirname -- "${BASH_SOURCE[0]}")/check_docs.py" "$@"
