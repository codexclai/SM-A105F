#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
ARCHIVE=${INITRAMFS_ARCHIVE:-"$ROOT/work/initramfs/a105f-debian-initramfs.cpio.gz"}
BUSYBOX=${BUSYBOX_STATIC:-"$ROOT/work/initramfs/skeleton/usr/bin/busybox"}
QEMU=${QEMU_AARCH64_STATIC:-qemu-aarch64-static}
INIT=$ROOT/configs/initramfs/a105f-init
command -v gzip >/dev/null
command -v cpio >/dev/null
command -v readelf >/dev/null
command -v "$QEMU" >/dev/null
test -s "$ARCHIVE"
test -x "$BUSYBOX"
gzip -t -- "$ARCHIVE"
readelf -h "$BUSYBOX" | grep -q 'Machine:.*AArch64'
if readelf -l "$BUSYBOX" | grep -q INTERP; then echo 'BusyBox must be statically linked' >&2; exit 1; fi
grep -Eq '^[[:space:]]*\.[[:space:]]+/lib/root-device\.sh([[:space:]]|$)' "$INIT" || {
  echo 'init does not source the packaged root-device resolver' >&2
  exit 1
}
sh -n "$INIT"
"$QEMU" "$BUSYBOX" sh -n "$INIT"
TMP=$(mktemp -d)
trap 'rm -rf -- "$TMP"' EXIT
gzip -dc -- "$ARCHIVE" | (cd "$TMP" && cpio -id --quiet --no-absolute-filenames)
test -x "$TMP/bin/busybox"
test -f "$TMP/lib/root-device.sh"
cmp -- "$ROOT/configs/initramfs/root-device.sh" "$TMP/lib/root-device.sh"
cmp -- "$INIT" "$TMP/init"
cmp -- "$BUSYBOX" "$TMP/bin/busybox"
APPLET_LIST=$("$QEMU" "$BUSYBOX" --list)
for applet in mount switch_root sleep mkdir cat head sh; do
  grep -Fxq "$applet" <<<"$APPLET_LIST" || { echo "missing BusyBox applet: $applet" >&2; exit 1; }
  test -L "$TMP/bin/$applet"
  test "$(readlink -- "$TMP/bin/$applet")" = busybox
done
ARCHIVE_ENTRIES=$(gzip -dc -- "$ARCHIVE" | cpio -it --quiet | sed 's#^\./##')
for path in init lib/root-device.sh bin/busybox bin/mount bin/switch_root bin/sleep bin/mkdir bin/cat bin/head bin/sh dev proc sys run newroot; do
  grep -Fxq "$path" <<<"$ARCHIVE_ENTRIES" || { echo "missing archive entry: $path" >&2; exit 1; }
done
echo 'initramfs archive extraction, BusyBox static ARM64 identity, applets, and init shell syntax validated'
sha256sum -- "$ARCHIVE" "$BUSYBOX"
