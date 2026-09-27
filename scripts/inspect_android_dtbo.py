#!/usr/bin/env python3
"""Inspect Android DT table images without modifying them."""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path
from typing import Any


DT_TABLE_MAGIC = 0xD7B7AB1E
FDT_MAGIC = 0xD00DFEED
HEADER = struct.Struct(">8I")
ENTRY_V0 = struct.Struct(">8I")


class DtboError(ValueError):
    """Raised when an Android DT table is malformed or truncated."""


def inspect_dtbo(data: bytes) -> dict[str, Any]:
    """Return validated Android DT table header and entry metadata.

    The parser reads Android's big-endian DT table format. It checks table,
    entry, and FDT bounds, but does not decide which overlay matches a device.
    """
    if len(data) < HEADER.size:
        raise DtboError(f"file is shorter than the {HEADER.size}-byte DT table header")

    (magic, total_size, header_size, entry_size, entry_count,
     entries_offset, page_size, version) = HEADER.unpack_from(data)

    if magic != DT_TABLE_MAGIC:
        raise DtboError(f"bad DT table magic 0x{magic:08x}")
    if total_size < HEADER.size or total_size > len(data):
        raise DtboError(f"invalid table size {total_size} for {len(data)} input bytes")
    if header_size < HEADER.size or header_size > total_size:
        raise DtboError(f"invalid header size {header_size}")
    if entry_size < ENTRY_V0.size:
        raise DtboError(f"entry size {entry_size} is smaller than the v0 entry size")
    if entry_count == 0:
        raise DtboError("DT table contains no entries")
    if page_size == 0 or page_size & (page_size - 1):
        raise DtboError(f"page size {page_size} is not a positive power of two")

    entries_end = entries_offset + entry_count * entry_size
    if entries_offset < header_size or entries_end > total_size:
        raise DtboError("DT table entries lie outside the declared table bounds")

    entries: list[dict[str, Any]] = []
    payload_ranges: list[tuple[int, int]] = []
    for index in range(entry_count):
        offset = entries_offset + index * entry_size
        size, dt_offset, board_id, revision, c0, c1, c2, c3 = ENTRY_V0.unpack_from(data, offset)
        end = dt_offset + size
        if size < 4 or dt_offset < entries_end or end > total_size:
            raise DtboError(f"entry {index} payload is outside the declared table bounds")
        if struct.unpack_from(">I", data, dt_offset)[0] != FDT_MAGIC:
            raise DtboError(f"entry {index} payload does not begin with FDT magic")
        payload_ranges.append((dt_offset, end))
        entries.append({
            "index": index,
            "dt_size": size,
            "dt_offset": dt_offset,
            "id": board_id,
            "rev": revision,
            "custom": [c0, c1, c2, c3],
            "entry_extra_bytes": entry_size - ENTRY_V0.size,
        })

    payload_ranges.sort()
    for previous, current in zip(payload_ranges, payload_ranges[1:]):
        if current[0] < previous[1]:
            raise DtboError("DT table payload entries overlap")

    return {
        "magic": f"0x{magic:08x}",
        "file_size": len(data),
        "table_size": total_size,
        "trailing_bytes": len(data) - total_size,
        "header_size": header_size,
        "entry_size": entry_size,
        "entry_count": entry_count,
        "entries_offset": entries_offset,
        "page_size": page_size,
        "version": version,
        "entries": entries,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path, help="Android dtbo.img or DT table file")
    args = parser.parse_args(argv)
    try:
        result = inspect_dtbo(args.image.read_bytes())
    except (OSError, DtboError) as exc:
        print(f"{args.image}: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
