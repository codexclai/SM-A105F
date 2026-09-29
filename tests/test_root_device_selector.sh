#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
. "$ROOT/configs/initramfs/root-device.sh"

root_device_exists() {
	[[ "$1" == /dev/mmcblk0p3 ]]
}
expect_supported() {
	root_spec_supported "$1" || { echo "expected supported root spec: $1" >&2; exit 1; }
}
expect_rejected() {
	if root_spec_supported "$1"; then
		echo "expected rejected root spec: $1" >&2
		exit 1
	fi
}
expect_supported /dev/mmcblk0p3
expect_rejected /dev/mmcblk1p3
expect_rejected /dev/mmcblk0
expect_rejected /dev/mmcblk0p3/../../sda1
expect_rejected UUID=measured-id
expect_rejected PARTUUID=measured-id
expect_rejected /dev/sda1
[[ "$(resolve_root_device /dev/mmcblk0p3)" == /dev/mmcblk0p3 ]]
if resolve_root_device /dev/mmcblk0p4 >/dev/null; then
	echo 'resolver selected a device that the existence check rejected' >&2
	exit 1
fi
if resolve_root_device /dev/mmcblk1p3 >/dev/null; then
	echo 'resolver accepted a non-eMMC device' >&2
	exit 1
fi
echo 'root-device selector inputs and explicit selection validated'
