#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
archive=work/initramfs/a105f-debian-initramfs.cpio.gz
init=configs/initramfs/a105f-init
busybox=work/initramfs/skeleton/usr/bin/busybox
test -s "$archive"; test -x "$busybox"; gzip -t "$archive"; bash -n "$init"
qemu-aarch64-static "$busybox" sh -n "$init"
readelf -h "$busybox" | grep -q AArch64
entries=$(gzip -dc "$archive" | cpio -it 2>/dev/null)
for path in init bin/busybox bin/mount bin/switch_root bin/blkid bin/sh dev proc sys run newroot; do grep -qx "$path" <<<"$entries" || { echo "missing entry: $path" >&2; exit 1; }; done
echo 'initramfs structure and ARM64 init syntax validated'
sha256sum "$archive" "$busybox"
