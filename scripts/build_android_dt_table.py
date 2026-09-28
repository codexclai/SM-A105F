#!/usr/bin/env python3
"""Wrap one raw FDT in an Android DT table v0 image for host validation."""
import argparse
import struct
from pathlib import Path
from inspect_android_boot_layout import _fdt_summary

MAGIC = 0xD7B7AB1E
HEADER = struct.Struct(">8I")
ENTRY = struct.Struct(">8I")

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input_fdt", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--page-size", type=int, default=2048)
    ap.add_argument("--id", type=lambda v: int(v, 0), default=0)
    ap.add_argument("--rev", type=lambda v: int(v, 0), default=0)
    ap.add_argument("--custom", nargs=4, type=lambda v: int(v, 0), default=[0, 0, 0, 0])
    args = ap.parse_args()
    if args.page_size < 2048 or args.page_size & (args.page_size - 1):
        ap.error("page size must be a power of two >= 2048")
    fdt = args.input_fdt.read_bytes()
    try:
        summary = _fdt_summary(fdt)
    except ValueError as exc:
        ap.error("input FDT is invalid: " + str(exc))
    fdt = fdt[:summary["totalsize"]]
    header_size, entry_size, count, entries_offset = 32, 32, 1, 32
    data_offset = ((entries_offset + count * entry_size + args.page_size - 1) // args.page_size) * args.page_size
    padded_size = ((len(fdt) + args.page_size - 1) // args.page_size) * args.page_size
    total_size = data_offset + padded_size
    header = HEADER.pack(MAGIC, total_size, header_size, entry_size, count, entries_offset, args.page_size, 0)
    entry = ENTRY.pack(len(fdt), data_offset, args.id, args.rev, *args.custom)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(header + entry + bytes(data_offset - len(header) - len(entry)) + fdt + bytes(padded_size - len(fdt)))

if __name__ == "__main__":
    main()
