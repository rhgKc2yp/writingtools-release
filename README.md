# Writing Tools — Fedora 45 Podman builds

Builds [theJayTea/WritingTools](https://github.com/theJayTea/WritingTools) for
Linux x86_64 using **Podman** and **Fedora 45** in GitHub Actions.
This is an independent build repository. The application remains upstream's work.

The build follows upstream's [source instructions](https://github.com/theJayTea/WritingTools/blob/main/README%27s%20Linked%20Content/To%20Run%20Writing%20Tools%20Directly%20from%20the%20Source%20Code.md),
installs `Windows_and_Linux/requirements.txt`, and packages `main.py` with PyInstaller.
The GitHub runner is Ubuntu; all application dependencies, packaging, and the
frozen application smoke check run inside a Fedora 45 container.

## Build on GitHub

Create an empty GitHub repository named `writingtools-fedora`, then upload this
repository's contents, including `.github/workflows/build.yml`, to its `main` branch.
The first push starts the build. You can also select **Actions → Build Writing
Tools with Podman (Fedora 45) → Run workflow**.

Alternatively, with authenticated GitHub CLI, from this directory:

```bash
gh repo create writingtools-fedora --private --source=. --remote=origin --push
```

After a successful run, download the `writing-tools-fedora45-x86_64` artifact
from the run summary. It includes:

- `writing-tools-fedora45-x86_64.tar.gz`: executable, Python/Qt libraries and assets.
- `writing-tools-source.tar.gz`: exact upstream application source.
- `upstream-commit.txt` and `python-packages.txt`: build provenance.
- `SHA256SUMS`: archive checksums.

No API keys or GitHub secrets are needed to build. Configure your AI provider in
Writing Tools after launching it.

## Run the bundle on Fedora 45

Install the host libraries and clipboard helper:

```bash
sudo dnf install mesa-libGL mesa-libEGL libxkbcommon-x11 xcb-util-cursor xcb-util-wm \
  xcb-util-image xcb-util-keysyms xcb-util-renderutil libX11 libXext \
  libXrender libXi fontconfig freetype dbus-libs xclip
sha256sum -c SHA256SUMS
tar -xzf writing-tools-fedora45-x86_64.tar.gz
./writing-tools/writing-tools
```

Extract to a writable directory under your home folder: upstream saves
`config.json` and edited `options.json` beside the executable. Keep the complete
`writing-tools` directory together. Builds target Fedora 45; older distributions
may lack the required glibc version.

Upstream uses `pynput` for global shortcuts and keyboard simulation. Use an X11
desktop session for these features. Wayland/XWayland can restrict global keyboard
access; this build does not change those upstream limitations.

## Build locally

Install Podman, then run:

```bash
bash scripts/build.sh
```

Results appear in `dist/`. No GUI access or privileged container is needed. The
container uses Xvfb to check the frozen imports, Qt initialization and assets;
this does not test real desktop shortcuts, clipboard interaction or AI requests.

The default upstream commit is pinned in `upstream-ref.txt`. Update it to select
a newer revision. A manual Actions run accepts an optional commit, tag or branch;
the corresponding local override is:

```bash
UPSTREAM_REF=main bash scripts/build.sh
```

Python 3.13 is selected explicitly for compatibility with binary Qt wheels.
Fedora packages and upstream's Python dependencies are resolved at build time;
the recorded versions describe each build, but dependencies are not locked.

## License

Build files use GPL-3.0, as does the upstream application; see `LICENSE`.
Upstream notices are preserved in the source archive. Bundled dependencies retain
their respective licenses and notices.
