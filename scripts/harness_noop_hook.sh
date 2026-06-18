#!/usr/bin/env bash
set -u

event="${1:-unknown}"
printf 'harness no-op hook: %s\n' "$event" >&2
exit 0
