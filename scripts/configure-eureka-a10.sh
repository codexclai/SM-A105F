#!/usr/bin/env bash
# Generate an experimental Debian-oriented A10 kernel config; never builds or flashes a kernel.
set -euo pipefail

if [[ $# -ne 2 || $1 != /* || $2 != /* ]]; then
    printf 'Usage: %s /absolute/pinned/Eureka-Kernel /absolute/new/output-directory\n' "$0" >&2
    exit 2
fi

source_dir=$1
output_dir=$2
expected_source=e1b8464bb29ce5bcb9d52bfcfc71bc2563e12563
expected_kernelsu=109442f8c4c7692af6562bdad6fd9f39dc1f935b

for tool in git make grep sha256sum; do
    command -v "$tool" >/dev/null || { printf 'Missing tool: %s\n' "$tool" >&2; exit 1; }
done
[[ -d "$source_dir" && -f "$source_dir/scripts/config" ]] || {
    printf 'A complete Eureka source tree is required\n' >&2
    exit 1
}
[[ "$(git -C "$source_dir" rev-parse HEAD)" == "$expected_source" ]] || {
    printf 'Unexpected Eureka source revision\n' >&2
    exit 1
}
[[ "$(git -C "$source_dir/KernelSU" rev-parse HEAD 2>/dev/null || :)" == "$expected_kernelsu" ]] || {
    printf 'Pinned KernelSU submodule is required for Kconfig\n' >&2
    exit 1
}
[[ -z "$(git -C "$source_dir" status --porcelain --untracked-files=no)" &&
   -z "$(git -C "$source_dir/KernelSU" status --porcelain --untracked-files=no)" ]] || {
    printf 'Source or KernelSU has tracked changes; use a clean pinned checkout\n' >&2
    exit 1
}
[[ ! -e "$output_dir" ]] || { printf 'Refusing existing output: %s\n' "$output_dir" >&2; exit 1; }

mkdir -p -- "$output_dir"
make -C "$source_dir" O="$output_dir" ARCH=arm64 exynos7885-a10_defconfig
"$source_dir/scripts/config" --file "$output_dir/.config" \
    -e DEVTMPFS -e DEVTMPFS_MOUNT -e FHANDLE \
    --set-str UEVENT_HELPER_PATH ''
make -C "$source_dir" O="$output_dir" ARCH=arm64 olddefconfig

for setting in CONFIG_64BIT CONFIG_BLK_DEV_INITRD CONFIG_BINFMT_ELF CONFIG_EXT4_FS CONFIG_DEVTMPFS CONFIG_DEVTMPFS_MOUNT CONFIG_FHANDLE CONFIG_CGROUPS CONFIG_INOTIFY_USER CONFIG_SIGNALFD CONFIG_TIMERFD CONFIG_EPOLL CONFIG_UNIX CONFIG_SYSFS CONFIG_PROC_FS; do
    if ! grep -qx "${setting}=y" "$output_dir/.config"; then
        printf 'Required setting missing after Kconfig resolution: %s\n' "$setting" >&2
        exit 1
    fi
done
grep -qx '# CONFIG_SYSFS_DEPRECATED is not set' "$output_dir/.config" || {
    printf 'Deprecated sysfs layout is enabled\n' >&2
    exit 1
}
grep -qx 'CONFIG_UEVENT_HELPER_PATH=""' "$output_dir/.config" || {
    printf 'Legacy hotplug helper path remains configured\n' >&2
    exit 1
}
sha256sum -- "$output_dir/.config"
