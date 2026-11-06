#!/usr/bin/env bash
# Run under xvfb-run; requires Freedesktop Platform 26.08 already installed.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
test -n "${DISPLAY:-}" || { echo 'Run with xvfb-run -a bash scripts/check-flatpak.sh' >&2; exit 1; }
scratch=$(mktemp -d "$PWD/.flatpak-check.XXXXXX")
trap 'rm -rf "$scratch"' EXIT
tar -xzf dist/writing-tools-fedora45-x86_64.tar.gz -C "$scratch"

run_check() {
    flatpak run --user --socket=x11 --share=ipc \
      --filesystem="$scratch" \
      --env=QT_QPA_PLATFORM=xcb --env=WRITING_TOOLS_SMOKE_TEST=1 \
      --env=XDG_DATA_HOME="$scratch/data" \
      --command=sh org.freedesktop.Platform//26.08 \
      -c 'exec "$1/writing-tools/writing-tools-launcher"' sh "$scratch"
}
run_check
# A second launch must keep user options rather than copying defaults over them.
printf '\n' >> "$scratch/data/writing-tools/options.json"
before=$(sha256sum "$scratch/data/writing-tools/options.json")
run_check
test "$before" = "$(sha256sum "$scratch/data/writing-tools/options.json")"
printf 'Freedesktop 26.08 compatibility and options persistence passed.\n'
