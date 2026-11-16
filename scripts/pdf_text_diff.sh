#!/usr/bin/env bash
# Compare the text of two PDFs (e.g. old vs regenerated CV). Only intended changes should appear.
# Usage: pdf_text_diff.sh old.pdf new.pdf
set -euo pipefail
[ $# -eq 2 ] || { echo "usage: $0 old.pdf new.pdf" >&2; exit 2; }
echo "pages: $(pdfinfo "$1" | awk '/^Pages/{print $2}') -> $(pdfinfo "$2" | awk '/^Pages/{print $2}')"
diff <(pdftotext "$1" - | grep -v '^\s*$') <(pdftotext "$2" - | grep -v '^\s*$') && echo "no text differences"
