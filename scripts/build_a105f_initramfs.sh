#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
BUSYBOX_STATIC=${BUSYBOX_STATIC:?set BUSYBOX_STATIC to a verified ARM64 static BusyBox}
OUT=${OUT:-$ROOT/work/initramfs/a105f-debian-initramfs.cpio.gz}
[[ "$OUT" = /* ]] || OUT="$ROOT/$OUT"
mkdir -p "$ROOT/work/initramfs" "$(dirname "$OUT")"
STAGE=$(mktemp -d "$ROOT/work/initramfs/stage.XXXXXX")
trap 'rm -rf "$STAGE"' EXIT
mkdir -p "$STAGE/bin" "$STAGE/dev" "$STAGE/proc" "$STAGE/sys" "$STAGE/run" "$STAGE/newroot"
install -m 0755 "$BUSYBOX_STATIC" "$STAGE/bin/busybox"
for applet in sh mount switch_root blkid sleep mkdir cat head; do ln -s busybox "$STAGE/bin/$applet"; done
install -m 0755 "$ROOT/configs/initramfs/a105f-init" "$STAGE/init"
(cd "$STAGE" && find . -print0 | cpio --null -o --format=newc 2>/dev/null | gzip -n -9 > "$OUT")
gzip -t "$OUT"
sha256sum "$OUT"
echo "created $OUT"
