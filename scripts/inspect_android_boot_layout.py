#!/usr/bin/env python3
"""Inspect Android boot.img headers and Android DT table containers."""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

BOOT_MAGIC = b"ANDROID!"
DT_TABLE_MAGIC = 0xD7B7AB1E
FDT_MAGIC = 0xD00DFEED


def _cstring(data: bytes) -> str:
    return data.split(b"\0", 1)[0].decode("ascii", "replace")


def parse_boot_header(data: bytes) -> dict:
    if len(data) < 48 or data[:8] != BOOT_MAGIC:
        raise ValueError("not an Android boot image")
    (kernel_size, kernel_addr, ramdisk_size, ramdisk_addr, second_size,
     second_addr, tags_addr, page_size, header_version, os_version) = struct.unpack_from("<10I", data, 8)
    if page_size == 0:
        raise ValueError("boot image has a zero page size")
    out = {
        "file_size": len(data), "header_version": header_version,
        "page_size": page_size, "kernel_size": kernel_size,
        "kernel_load_address": kernel_addr, "ramdisk_size": ramdisk_size,
        "ramdisk_load_address": ramdisk_addr, "second_size": second_size,
        "second_load_address": second_addr, "tags_load_address": tags_addr,
        "product_name": _cstring(data[48:64]),
        "cmdline": " ".join(x for x in (_cstring(data[64:576]), _cstring(data[608:1632])) if x),
        "os_version_raw": os_version,
    }
    if header_version >= 1:
        if len(data) < 1648:
            raise ValueError("truncated boot header v1 extension")
        out.update({"recovery_dtbo_size": struct.unpack_from("<I", data, 1632)[0],
                    "recovery_dtbo_offset": struct.unpack_from("<Q", data, 1636)[0],
                    "header_size": struct.unpack_from("<I", data, 1644)[0]})
    if header_version >= 2:
        if len(data) < 1660:
            raise ValueError("truncated boot header v2 extension")
        out.update({"dtb_size": struct.unpack_from("<I", data, 1648)[0],
                    "dtb_load_address": struct.unpack_from("<Q", data, 1652)[0]})
    return out


def _fdt_summary(data: bytes) -> dict:
    if len(data) < 40:
        raise ValueError("truncated FDT header")
    (magic, total, struct_off, strings_off, _reserve_off, version,
     _last_compatible, _boot_cpuid, strings_size, struct_size) = struct.unpack_from(">10I", data)
    if magic != FDT_MAGIC or total > len(data) or total < 40:
        raise ValueError("invalid FDT blob")
    if struct_off + struct_size > total or strings_off + strings_size > total:
        raise ValueError("FDT block lies outside totalsize")
    strings = data[strings_off:strings_off + strings_size]
    pos = struct_off
    end = struct_off + struct_size
    depth = 0
    root_props = {}
    root_seen = False
    while pos + 4 <= end:
        token = struct.unpack_from(">I", data, pos)[0]
        pos += 4
        if token == 1:  # FDT_BEGIN_NODE
            node_end = data.find(b"\0", pos, end)
            if node_end < 0:
                raise ValueError("unterminated FDT node name")
            pos = (node_end + 4) & ~3
            depth += 1
            if depth == 1:
                root_seen = True
        elif token == 2:  # FDT_END_NODE
            depth -= 1
            if depth <= 0:
                break
        elif token == 3:  # FDT_PROP
            if pos + 8 > end:
                raise ValueError("truncated FDT property")
            size, name_off = struct.unpack_from(">II", data, pos)
            pos += 8
            if name_off >= len(strings) or pos + size > end:
                raise ValueError("invalid FDT property bounds")
            name_end = strings.find(b"\0", name_off)
            if name_end < 0:
                raise ValueError("unterminated FDT property name")
            name = strings[name_off:name_end].decode("ascii", "replace")
            value = data[pos:pos + size]
            if depth == 1:
                root_props[name] = value
            pos = (pos + size + 3) & ~3
        elif token == 4:  # FDT_NOP
            continue
        elif token == 9:  # FDT_END
            break
        else:
            raise ValueError(f"unknown FDT structure token {token}")
    def string_list(name: str) -> list[str]:
        raw = root_props.get(name, b"").rstrip(b"\0")
        return [v.decode("ascii", "replace") for v in raw.split(b"\0") if v]
    return {"totalsize": total, "version": version,
            "compatible": string_list("compatible"), "model": string_list("model"),
            "root_node_found": root_seen}


def parse_dt_table(data: bytes) -> dict:
    if len(data) < 32:
        raise ValueError("truncated DT table header")
    magic, total, header_size, entry_size, count, entries_off, page_size, version = struct.unpack_from(">8I", data)
    if magic != DT_TABLE_MAGIC:
        raise ValueError("not an Android DT table image")
    if header_size < 32 or entry_size < 32 or total > len(data) or total < header_size:
        raise ValueError("invalid DT table sizes")
    if entries_off < header_size or entries_off + count * entry_size > total:
        raise ValueError("DT table entries exceed total_size")
    entries = []
    furthest = entries_off + count * entry_size
    for i in range(count):
        pos = entries_off + i * entry_size
        size, off, ident, rev, *custom = struct.unpack_from(">8I", data, pos)
        if off < header_size or off + size > total:
            raise ValueError(f"DT table entry {i} exceeds total_size")
        fdt = _fdt_summary(data[off:off + size])
        furthest = max(furthest, off + size)
        entries.append({"index": i, "size": size, "offset": off, "id": ident,
                        "revision": rev, "custom": custom, "fdt": fdt})
    return {"magic": f"0x{magic:08x}", "total_size": total,
            "header_size": header_size, "entry_size": entry_size,
            "entry_count": count, "entries_offset": entries_off,
            "page_size": page_size, "version": version,
            "unreferenced_bytes_in_total_size": total - furthest,
            "entries": entries}


def inspect_file(path: Path, parser) -> dict:
    data = path.read_bytes()
    return {"file": path.name, "file_size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(), "layout": parser(data)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--boot", type=Path, required=True)
    ap.add_argument("--dt", type=Path)
    ap.add_argument("--dtbo", type=Path)
    args = ap.parse_args()
    result = {"boot": inspect_file(args.boot, parse_boot_header)}
    if args.dt:
        result["dt"] = inspect_file(args.dt, parse_dt_table)
    if args.dtbo:
        result["dtbo"] = inspect_file(args.dtbo, parse_dt_table)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
