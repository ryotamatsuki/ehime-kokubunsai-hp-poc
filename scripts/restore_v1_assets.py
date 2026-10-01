#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "ASSET_MANIFEST.tsv"

def load_manifest():
    rows = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines()[1:]:
        if not line.strip():
            continue
        path, size, sha = line.split("\t")
        rows[path] = (int(size), sha)
    return rows

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python scripts/restore_v1_assets.py /path/to/ehime-kokubunsai-hp.zip")
    archive = Path(sys.argv[1])
    expected = load_manifest()
    with zipfile.ZipFile(archive) as zf:
        names = set(zf.namelist())
        for rel, (size, sha) in expected.items():
            if rel == "assets/brand-mark.svg":
                continue
            candidates = [rel, f"ehime-kokubunsai-hp/{rel}"]
            member = next((x for x in candidates if x in names), None)
            if member is None:
                raise SystemExit(f"missing in archive: {rel}")
            data = zf.read(member)
            if len(data) != size or hashlib.sha256(data).hexdigest() != sha:
                raise SystemExit(f"integrity check failed: {rel}")
            out = ROOT / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
            print(f"restored {rel}")
    print("v1 raster assets restored and verified.")

if __name__ == "__main__":
    main()
