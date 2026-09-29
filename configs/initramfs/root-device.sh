#!/bin/sh

# Keep root selection explicit. The A10 DTS aliases eMMC as mmc0, but the
# partition number must be measured on the target before it is supplied.
root_spec_supported() {
	case "$1" in
	/dev/mmcblk0p*)
		partition=${1#/dev/mmcblk0p}
		case "$partition" in
		''|*[!0-9]*) return 1 ;;
		esac
		return 0
		;;
	UUID=*)
		identifier=${1#UUID=}
		case "$identifier" in ''|*/*) return 1 ;; esac
		return 0
		;;
	PARTUUID=*)
		identifier=${1#PARTUUID=}
		case "$identifier" in ''|*/*) return 1 ;; esac
		return 0
		;;
	*) return 1 ;;
	esac
}

root_device_exists() {
	[ -b "$1" ]
}

resolve_root_device() {
	root_spec=$1
	root_spec_supported "$root_spec" || return 1
	case "$root_spec" in
	/dev/mmcblk0p*)
		root_device_exists "$root_spec" && printf '%s\n' "$root_spec"
		;;
	UUID=*)
		root_candidate="/dev/disk/by-uuid/${root_spec#UUID=}"
		root_device_exists "$root_candidate" && printf '%s\n' "$root_candidate"
		;;
	PARTUUID=*)
		root_candidate="/dev/disk/by-partuuid/${root_spec#PARTUUID=}"
		root_device_exists "$root_candidate" && printf '%s\n' "$root_candidate"
		;;
	esac
}
