#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

required_files=(
  README.md
  AGENTS.md
  index.md
  docs/catalog.md
  docs/architecture.md
  docs/examples/pi/README.md
  docs/templates/pattern.md
  docs/templates/case-study.md
  docs/templates/adoption-worksheet.md
)

for file in "${required_files[@]}"; do
  test -f "$repo_root/$file" || {
    printf 'missing required file: %s\n' "$file" >&2
    exit 1
  }
done

for file in "$repo_root"/docs/patterns/*.md; do
  [[ "$(basename -- "$file")" == "README.md" ]] && continue
  grep -q '^## Use when' "$file" || { printf 'missing Use when section: %s\n' "$file" >&2; exit 1; }
  grep -q '^## Trade-offs' "$file" || { printf 'missing Trade-offs section: %s\n' "$file" >&2; exit 1; }
  grep -q '^## Poor fit signals' "$file" || { printf 'missing Poor fit section: %s\n' "$file" >&2; exit 1; }
done

grep -q 'Observed' "$repo_root/docs/examples/pi/README.md"
grep -q 'Recommendation' "$repo_root/docs/examples/pi/README.md"
grep -q 'Important limit' "$repo_root/docs/examples/pi/README.md"

printf 'documentation checks passed\n'
