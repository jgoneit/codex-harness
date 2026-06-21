#!/bin/sh
set -eu

REPO_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
DIST_DIR="$REPO_ROOT/dist"
ZIP_PATH="$DIST_DIR/harness.zip"
MANIFEST=$(mktemp "${TMPDIR:-/tmp}/harness-package.XXXXXX")

cleanup() {
    rm -f "$MANIFEST"
}
trap cleanup EXIT HUP INT TERM

require_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "error: $1 is required" >&2
        exit 1
    fi
}

require_command zip
require_command unzip
require_command git

cd "$REPO_ROOT"
mkdir -p "$DIST_DIR"
rm -f "$ZIP_PATH"

git ls-files --cached --others --exclude-standard \
    | grep -Ev '(^|/)(\.git|__MACOSX|__pycache__)(/|$)|(^|/)\.DS_Store$|\.pyc$|(^|/)dist(/|$)' \
    | LC_ALL=C sort > "$MANIFEST"

if [ ! -s "$MANIFEST" ]; then
    echo "error: package manifest is empty" >&2
    exit 1
fi

zip -q "$ZIP_PATH" -@ < "$MANIFEST"

excluded_paths=$(
    unzip -Z1 "$ZIP_PATH" \
        | grep -E '(^|/)(\.git|__MACOSX|__pycache__)(/|$)|(^|/)\.DS_Store$|\.pyc$|(^|/)dist(/|$)' \
        || true
)

if [ -n "$excluded_paths" ]; then
    echo "error: harness.zip contains excluded paths:" >&2
    echo "$excluded_paths" >&2
    exit 1
fi

echo "created $ZIP_PATH"
echo "verified excluded paths are absent"
