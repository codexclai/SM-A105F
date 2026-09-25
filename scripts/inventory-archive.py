#!/usr/bin/env python3
"""Read-only inventory of a firmware ZIP or TAR; never extract members."""

import argparse
import hashlib
import json
import pathlib
import tarfile
import zipfile


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def unsafe_name(name):
    parts = pathlib.PurePosixPath(name.replace("\\", "/")).parts
    return name.startswith(("/", "\\")) or ".." in parts or not name


def inventory(path):
    result = {"file": path.name, "size_bytes": path.stat().st_size,
              "sha256": sha256_file(path), "members": [], "warnings": []}
    seen = set()
    if zipfile.is_zipfile(path):
        result["format"] = "zip"
        with zipfile.ZipFile(path) as archive:
            for member in archive.infolist():
                result["members"].append({"name": member.filename,
                                          "size_bytes": member.file_size,
                                          "stored_bytes": member.compress_size,
                                          "crc32_claimed": f"{member.CRC:08x}"})
                if unsafe_name(member.filename):
                    result["warnings"].append(f"Unsafe member name: {member.filename}")
                if member.filename in seen:
                    result["warnings"].append(f"Duplicate member name: {member.filename}")
                seen.add(member.filename)
    elif tarfile.is_tarfile(path):
        result["format"] = "tar"
        with tarfile.open(path, mode="r|*") as archive:
            for member in archive:
                result["members"].append({"name": member.name,
                                          "size_bytes": member.size,
                                          "type": "file" if member.isfile() else "other"})
                if unsafe_name(member.name):
                    result["warnings"].append(f"Unsafe member name: {member.name}")
                if not member.isfile() and not member.isdir():
                    result["warnings"].append(f"Non-regular member: {member.name}")
                if member.name in seen:
                    result["warnings"].append(f"Duplicate member name: {member.name}")
                seen.add(member.name)
    else:
        raise ValueError("not a recognized ZIP or TAR archive")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=pathlib.Path)
    args = parser.parse_args()
    try:
        result = inventory(args.archive)
    except (OSError, ValueError, tarfile.TarError, zipfile.BadZipFile) as exc:
        parser.exit(1, f"Inventory failed: {exc}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
