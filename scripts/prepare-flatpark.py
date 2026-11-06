"""Generate a catalog package from an existing public, checksum-verified release."""
import argparse
import hashlib
import json
import re
import shutil
import tempfile
import urllib.request
from pathlib import Path

APP_ID = "io.github.theJayTea.WritingTools"
REPO = "rhgKc2yp/writingtools-release"
ASSET = "writing-tools-fedora45-x86_64.tar.gz"


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "writingtools-flatpark-packager"})
    return urllib.request.urlopen(request, timeout=120)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not re.fullmatch(r"v[0-9][A-Za-z0-9._-]*", args.tag):
        parser.error("Tag must start with v and a digit")
    if args.output.exists():
        parser.error("Output already exists; generate separately and review changes")
    with fetch(f"https://api.github.com/repos/{REPO}/releases/tags/{args.tag}") as response:
        release = json.load(response)
    if release["draft"] or release["prerelease"] or not release["published_at"]:
        raise ValueError("Release must be published and stable")
    assets = {asset["name"]: asset for asset in release["assets"]}
    asset = assets[ASSET]
    expected_url = f"https://github.com/{REPO}/releases/download/{args.tag}/{ASSET}"
    if asset["browser_download_url"] != expected_url:
        raise ValueError("Unexpected release asset URL")
    with fetch(assets["SHA256SUMS"]["browser_download_url"]) as response:
        entries = response.read().decode().splitlines()
    checksums = {line.split()[1].removeprefix("./"): line.split()[0] for line in entries}
    digest = hashlib.sha256()
    size = 0
    with fetch(expected_url) as response:
        while chunk := response.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    if size != asset["size"] or digest.hexdigest() != checksums[ASSET]:
        raise ValueError("Release asset size/checksum mismatch")

    values = {
        "URL": expected_url, "SHA256": digest.hexdigest(), "SIZE": str(size),
        "VERSION": args.tag.removeprefix("v"), "DATE": release["published_at"][:10],
    }
    templates = Path(__file__).resolve().parent.parent / "flatpark"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.output.parent) as temporary:
        staged = Path(temporary) / APP_ID
        staged.mkdir()
        for source in templates.iterdir():
            if source.suffix == ".in":
                contents = source.read_text()
                for key, value in values.items():
                    contents = contents.replace(f"@{key}@", value)
                (staged / source.stem).write_text(contents)
            else:
                shutil.copy2(source, staged / source.name)
        staged.rename(args.output)
    print(f"Prepared {args.output} from {args.tag}; follow Flatpark's testing playbook before submission.")


if __name__ == "__main__":
    main()
