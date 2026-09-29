#!/usr/bin/env python3
"""Extract and verify Android boot v1 kernel/ramdisk payloads.

This host tool validates the page-aligned section layout and emits a JSON
manifest. It does not model Samsung signing/footer acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct


def parse_boot_header(data: bytes) -> dict:
    if len(data) < 48 or data[:8] != b"ANDROID!":
        raise ValueError("not an Android boot image")
    fields = struct.unpack_from("<10I", data, 8)
    (kernel_size, kernel_addr, ramdisk_size, ramdisk_addr, second_size,
     second_addr, tags_addr, page_size, version, os_version) = fields
    if version < 1:
        raise ValueError("only Android boot header v1 is supported")
    if len(data) < 1648:
        raise ValueError("truncated boot header v1 extension")
    recovery_size = struct.unpack_from("<I", data, 1632)[0]
    recovery_off = struct.unpack_from("<Q", data, 1636)[0]
    header_size = struct.unpack_from("<I", data, 1644)[0]
    return {"header_version": version, "page_size": page_size,
            "kernel_size": kernel_size, "kernel_load_address": kernel_addr,
            "ramdisk_size": ramdisk_size, "ramdisk_load_address": ramdisk_addr,
            "second_size": second_size, "second_load_address": second_addr,
            "tags_load_address": tags_addr, "os_version_raw": os_version,
            "recovery_dtbo_size": recovery_size,
            "recovery_dtbo_offset": recovery_off, "header_size": header_size,
            "cmdline": " ".join(part.split(b"\0", 1)[0].decode("ascii", "replace")
                                 for part in (data[64:576], data[608:1632])
                                 if part.split(b"\0", 1)[0])}


def align(value: int, page: int) -> int:
    return (value + page - 1) // page * page


def extract(data: bytes) -> tuple[dict, dict[str, bytes]]:
    header = parse_boot_header(data)
    if header["header_version"] != 1:
        raise ValueError("only Android boot header v1 is supported")
    page = header["page_size"]
    if page < 512 or page & (page - 1):
        raise ValueError("page size must be a power of two")
    if not 1648 <= header["header_size"] <= page:
        raise ValueError("boot header size is outside the first page")
    if len(data) < page:
        raise ValueError("truncated first boot page")
    if header["kernel_size"] == 0:
        raise ValueError("kernel section is empty")

    sections: dict[str, tuple[int, int]] = {}
    kernel_off = page
    kernel_end = kernel_off + header["kernel_size"]
    ramdisk_off = align(kernel_end, page)
    ramdisk_end = ramdisk_off + header["ramdisk_size"]
    second_off = align(ramdisk_end, page)
    second_end = second_off + header["second_size"]
    sections["kernel"] = (kernel_off, kernel_end)
    sections["ramdisk"] = (ramdisk_off, ramdisk_end)
    if header["second_size"]:
        sections["second"] = (second_off, second_end)

    recovery_size = header.get("recovery_dtbo_size", 0)
    recovery_off = header.get("recovery_dtbo_offset", 0)
    if recovery_size:
        if recovery_off % page:
            raise ValueError("recovery_dtbo_offset is not page aligned")
        if recovery_off < align(second_end, page):
            raise ValueError("recovery DTBO overlaps preceding section")
        sections["recovery_dtbo"] = (recovery_off, recovery_off + recovery_size)

    payloads: dict[str, bytes] = {}
    previous_end = page
    for name, (start, end) in sections.items():
        if start < previous_end or end < start or end > len(data):
            raise ValueError(f"{name} section is truncated, overlapping, or out of bounds")
        if start % page:
            raise ValueError(f"{name} section offset is not page aligned")
        payloads[name] = data[start:end]
        previous_end = end

    manifest = {
        "image_size": len(data),
        "header_version": 1,
        "page_size": page,
        "kernel_load_address": header["kernel_load_address"],
        "ramdisk_load_address": header["ramdisk_load_address"],
        "tags_load_address": header["tags_load_address"],
        "cmdline": header["cmdline"],
        "sections": {
            name: {"offset": sections[name][0], "size": len(payload),
                   "sha256": hashlib.sha256(payload).hexdigest()}
            for name, payload in payloads.items()
        },
        "trailing_bytes_after_last_payload": len(data) - previous_end,
    }
    return manifest, payloads


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("boot", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--expected-kernel", type=Path)
    parser.add_argument("--expected-ramdisk", type=Path)
    parser.add_argument("--expect-page-size", type=lambda v: int(v, 0))
    parser.add_argument("--expect-kernel-address", type=lambda v: int(v, 0))
    parser.add_argument("--expect-ramdisk-address", type=lambda v: int(v, 0))
    parser.add_argument("--expect-tags-address", type=lambda v: int(v, 0))
    args = parser.parse_args()
    manifest, payloads = extract(args.boot.read_bytes())
    for label, expected in (("kernel", args.expected_kernel),
                            ("ramdisk", args.expected_ramdisk)):
        if expected is not None:
            got = manifest["sections"].get(label, {}).get("sha256")
            if got != sha(expected):
                raise SystemExit(f"{label} payload does not match {expected}")
    for argument, key in (("expect_page_size", "page_size"),
                          ("expect_kernel_address", "kernel_load_address"),
                          ("expect_ramdisk_address", "ramdisk_load_address"),
                          ("expect_tags_address", "tags_load_address")):
        expected = getattr(args, argument)
        if expected is not None and manifest[key] != expected:
            raise SystemExit(f"{key} is 0x{manifest[key]:x}; expected 0x{expected:x}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in payloads.items():
        (args.output_dir / f"{name}.bin").write_bytes(payload)
    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
