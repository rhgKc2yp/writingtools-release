#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
upstream_ref=${UPSTREAM_REF:-$(cat upstream-ref.txt)}
image=localhost/writingtools-fedora45:build
podman build --build-arg "UPSTREAM_REF=$upstream_ref" -t "$image" -f Containerfile .
mkdir -p dist
podman run --rm --network=none -v "$PWD/dist:/output:Z" "$image"
printf 'Build artifacts: %s/dist\n' "$PWD"
