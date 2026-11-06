# Local validation — 2026-11-06

Tested against upstream revision `0839d8c9a8b7775cce14d3b6eca0f9fe85ecd139`.

Passed:

- Full Podman/Fedora 45 build, including the unmodified upstream application.
- Frozen application imports, Qt initialization and image assets.
- Clipboard round trip using the bundled xclip on a private X11 display.
- Writable state and preservation of edited options on two runtime launches.
- Freedesktop Platform 26.08 compatibility.
- Flatpark descriptor reader and packaging audit, using its recommended builder.
- Flatpak manifest build, AppStream composition and installation from a temporary
  local repository. This fixture used a loopback HTTP asset URL, not a public pin.
- Offline extraction as uid 0 with all capabilities dropped, against the runtime.
- Installed-app smoke check and first-run onboarding window, visually inspected.
- Measured X11 window class `Writing-tools`, recorded in the desktop entry.
- Package generator tests: verified pins and rejection of corrupted downloads.
- Shell/Python syntax and workflow lint. Actionlint's runner list predates
  Ubuntu 26.04, so validation supplied that label explicitly after checking
  [GitHub's supported images](https://github.com/actions/runner-images).

Not yet verified:

- Publishing on GitHub or delivering a Flatpark notification: this workspace
  has no authenticated GitHub access, and the repository has no public releases.
- Flatpark's first catalog listing and maintainer agreement to the build repository.
- A real AI request, global hotkey selection capture and replacement in another
  X11 application, settings saved through the UI across restarts, tray behavior
  after provider setup, and the complete home-directory change audit.

The app must remain unlisted until the remaining application checks pass or an
appropriate tester confirms them, following Flatpark's testing playbook. Runtime
smoke checks are compatibility evidence, not a claim of full application testing.

The temporary test app, remote and private app data were removed. Source changes,
release artifacts and a screenshot/logs were retained for review. Existing apps,
other sessions' displays and shared runtimes/caches were left alone.
