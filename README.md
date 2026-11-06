# Writing Tools Linux releases

Independent builds of [Writing Tools](https://github.com/theJayTea/WritingTools)
using **Podman and Fedora 45**, for Linux x86_64 and Flatpark.
Upstream application source is unmodified. Packaging support belongs in
[this repository's issues](https://github.com/rhgKc2yp/writingtools-release/issues).

## Build

```bash
bash scripts/build.sh
```

The pinned revision is in `upstream-ref.txt`. Build artifacts appear in `dist/`.
The existing build workflow still builds on pushes and pull requests without
publishing a release.

## Publish

The new **Release for Flatpark** workflow runs when a `v*` tag is pushed, or from
**Actions → Release for Flatpark → Run workflow**, with a new tag such as
`v2026.11.06-1`. It builds the pinned upstream revision, checks the bundle on
Freedesktop Platform 26.08, and publishes the binary, source, build recipes,
checksums and provenance as GitHub release assets. It requires only the automatic
GitHub token; `contents: write` is confined to the release job. Use a public
repository. Choose a new tag for every rebuild; published assets are never replaced.

See [docs/flatpark.md](docs/flatpark.md) for the initial listing and notification
setup. The notification job runs after publishing in the same workflow because
releases created with `GITHUB_TOKEN` do not trigger another release workflow.

## Run

```bash
sha256sum -c SHA256SUMS
tar -xzf writing-tools-fedora45-x86_64.tar.gz
./writing-tools/writing-tools-launcher
```

Use the launcher: configuration and custom options live in
`$XDG_DATA_HOME/writing-tools` (normally `~/.local/share/writing-tools`, or
`~/.var/app/io.github.theJayTea.WritingTools/data/writing-tools` in Flatpak).
The executable is copied there unchanged; libraries and images link to the
installed bundle. Keep the bundle in place. It includes Python, Qt, `xclip`
and `libXmu`; graphics, X11 and font libraries come from the OS or Flatpak runtime.

Global shortcuts, selection capture and text replacement require an **X11
desktop session**. Native Wayland applications are not supported. Configure
your AI provider after launching; builds need no API keys.

## Verify locally

Install `flatpak`, `xvfb` and `xauth`, and install
`org.freedesktop.Platform//26.08` from Flathub. Then:

```bash
xvfb-run -a bash scripts/check-flatpak.sh
```

This checks frozen imports, Qt, assets, clipboard, writable state and options
preservation on restart inside the runtime. It does not replace Flatpark's
installed-app review or test a real AI provider.

Python 3.13 is selected for Qt wheel compatibility. Fedora and Python dependencies
are resolved at build time and recorded in each release; they are not locked.
GPL-3.0 applies to these build files and the upstream app; dependencies retain
their own licenses and notices. See `LICENSE` and release source archives.
