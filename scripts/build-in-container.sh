#!/usr/bin/env bash
set -euo pipefail
cd /build/source/Windows_and_Linux

# pynput imports its backend while PyInstaller inspects it, so analysis also
# needs a display. Include Xlib's dynamically loaded extension modules.
xvfb-run -a python -m PyInstaller --noconfirm --clean --onedir --name writing-tools \
  --collect-submodules pynput --collect-submodules Xlib \
  --add-data 'locales:locales' \
  --runtime-hook /build/scripts/smoke-hook.py main.py

bundle=dist/writing-tools
# Upstream resolves these using sys.argv[0], so keep them beside the executable.
cp -a icons options.json options_examples.json background*.png "$bundle/"
cp /build/source/LICENSE "$bundle/LICENSE"
cp /build/upstream-commit.txt "$bundle/UPSTREAM_COMMIT"
python -m pip freeze > "$bundle/python-packages.txt"
cat /etc/fedora-release > "$bundle/BUILD_PLATFORM"

# Exercise the frozen dependency graph and Qt under a virtual X server.
WRITING_TOOLS_SMOKE_TEST=1 xvfb-run -a "$bundle/writing-tools"

mkdir -p /artifacts
arch=$(uname -m)
tar -C dist -czf "/artifacts/writing-tools-fedora45-${arch}.tar.gz" writing-tools
# Ship the exact upstream source alongside the binary and build provenance.
git -C /build/source archive --format=tar.gz --output="/artifacts/writing-tools-source.tar.gz" HEAD
cp /build/upstream-commit.txt /artifacts/
cp "$bundle/python-packages.txt" /artifacts/
cd /artifacts
sha256sum ./*.tar.gz > SHA256SUMS
