# Publishing on Flatpark

The workflow follows Flatpark's [publish-action integration](https://github.com/flatpark/flatpark/blob/main/docs/developers/publish-action.md).
Use its [packaging playbook](https://github.com/flatpark/flatpark/blob/main/docs/packagers/playbook.md)
for the initial listing. Publishing a GitHub release and notifying Flatpark does
not create a catalog listing.

## Initial listing

1. Push these changes to `rhgKc2yp/writingtools-release`.
2. Run **Release for Flatpark** with a new tag, such as `v2026.11.06-1`.
   Wait for the public GitHub release and binary asset.
3. Obtain a Flatpark maintainer's agreement to use this independent build
   repository, as required by its build-repository policy.
4. Clone `flatpark/flatpark`, start at `docs/README.md`, then generate a pinned
   package directory from the published release:

   ```bash
   python3 scripts/prepare-flatpark.py --tag v2026.11.06-1 \
     --output /path/to/flatpark/registry/io.github.theJayTea.WritingTools
   ```

   The generator downloads the public release, verifies its published checksum,
   and supplies the URL, size, checksum, version and date. Templates are in
   `flatpark/`; they contain no fabricated release pins.
5. Follow Flatpark's testing playbook on a build installed from a local repository.
   Check first launch, drawing, settings/options across restarts, home-folder
   changes, window class, tray, hotkeys, selection capture, a real AI request and
   replacement in another X11 app. Use an AI provider you can actually access.
   The runtime smoke check is not this review.
6. Prepare the Flatpark PR with test evidence and the independent-build disclosure.
   Its playbook requires human approval before an agent opens the PR. Do not
   claim upstream approval; the template leaves the shield off.
7. After the reviewed listing is live, set repository Actions variable
   `FLATPARK_PUBLISH_ENABLED` to `true`. The catalog's `source_url` must be
   `https://github.com/rhgKc2yp/writingtools-release`; its id must match
   `io.github.theJayTea.WritingTools`. If review changes the id, update the
   workflow and templates together before enabling notifications.

Subsequent releases notify Flatpark after uploading all assets. Notification
failure does not fail the GitHub release. To retry a notification, run
`flatpark/publish-action@v1` with the existing tag; do not rebuild or replace
published files under that tag.

## Package behavior

The catalog downloads the binary tarball as extra-data and unpacks it offline.
It uses Freedesktop Platform 26.08 because the bundle ships Python and Qt.
The release launcher provides a writable portable layout in private app data
and preserves existing config and options.

Permissions are X11 and IPC for global shortcuts and text replacement, network
for AI endpoints, DRI for Qt drawing and narrow tray D-Bus names. No host
filesystem access or host command execution is granted. Clipboard support is
part of the release, not compiled by Flatpark.

The package description discloses the independent build and native Wayland
limitation. Homepage links upstream; source and support links point here.
Check Flathub by application name and upstream's Flatpak discussions before
submitting, as required by the current playbook.
