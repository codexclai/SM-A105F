#!/usr/bin/env bash
# Reproducibly build the pinned third-party Eureka candidate; never flash it.
set -euo pipefail

usage() {
    printf 'Usage: %s /absolute/Eureka/source /absolute/kernel.config /absolute/output-directory\n' "$0" >&2
    exit 2
}

[[ $# -eq 3 && $1 = /* && $2 = /* && $3 = /* ]] || usage
source_dir=$(realpath "$1")
config_file=$(realpath "$2")
output_dir=$(realpath -m "$3")
project_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
patch_file=$project_root/patches/eureka-r24u/0001-guard-kernelsu-hooks.patch
expected_source=e1b8464bb29ce5bcb9d52bfcfc71bc2563e12563
expected_kernelsu=109442f8c4c7692af6562bdad6fd9f39dc1f935b
expected_config=faf3394e6f1bc194189b306c7774e31dde308c82cfb56f140c4471d98aa11c34
expected_patch=3427a61bc71b565182d8c71e989b997999c523c314d57aef692a4309bd31cbaa

for tool in git make realpath sha256sum cmp sed awk grep file; do
    command -v "$tool" >/dev/null || { printf 'Missing tool: %s\n' "$tool" >&2; exit 1; }
done
[[ -f "$source_dir/Makefile" && -f "$config_file" && -f "$patch_file" ]] || {
    printf 'Source, config, or project patch is missing\n' >&2; exit 1;
}
[[ ! -e "$output_dir" ]] || {
    printf 'Output path already exists; use a fresh directory for a clean build: %s\n' "$output_dir" >&2; exit 1;
}
[[ $(git -C "$source_dir" rev-parse HEAD) == "$expected_source" ]] || {
    printf 'Unexpected Eureka source revision\n' >&2; exit 1;
}
[[ $(git -C "$source_dir/KernelSU" rev-parse HEAD) == "$expected_kernelsu" ]] || {
    printf 'Unexpected KernelSU submodule revision\n' >&2; exit 1;
}
[[ $(sha256sum "$config_file" | awk '{print $1}') == "$expected_config" ]] || {
    printf 'Unexpected kernel configuration checksum\n' >&2; exit 1;
}
[[ $(sha256sum "$patch_file" | awk '{print $1}') == "$expected_patch" ]] || {
    printf 'Unexpected project patch checksum\n' >&2; exit 1;
}
[[ $(readlink "$source_dir/drivers/kernelsu") == ../KernelSU/kernel &&
   $(readlink "$source_dir/arch/arm64/boot/dts/exynos/dtbo/exynos7885-ecd.dtsi") == ../dtb/exynos7885-ecd.dtsi ]] || {
    printf 'Required tracked source symlinks are absent or altered\n' >&2; exit 1;
}

mkdir -p -- "$(dirname -- "$output_dir")"
mkdir -- "$output_dir"
export TMPDIR=${TMPDIR:-$output_dir/.tmp}
mkdir -p -- "$TMPDIR"
temporary=$output_dir/.source-diff.$$
patch_diff=$output_dir/.patch-diff.$$
cleanup_patch=0
cleanup() {
    if (( cleanup_patch )); then
        git -C "$source_dir" apply --reverse "$patch_file"
    fi
    rm -f -- "$temporary" "$patch_diff"
}
trap cleanup EXIT

if git -C "$source_dir" apply --reverse --check "$patch_file" 2>/dev/null; then
    git -C "$source_dir" diff --binary -- drivers/input/input.c fs/exec.c fs/read_write.c fs/open.c fs/stat.c > "$temporary"
    sed -n '/^diff --git /,$p' "$patch_file" > "$patch_diff"
    cmp -s "$temporary" "$patch_diff" || {
        printf 'Candidate source has changes beyond the recorded project patch\n' >&2; exit 1;
    }
else
    [[ -z $(git -C "$source_dir" status --porcelain --untracked-files=all) ]] || {
        printf 'Candidate source is dirty; refusing to apply a patch over unknown changes\n' >&2; exit 1;
    }
    git -C "$source_dir" apply --check "$patch_file"
    git -C "$source_dir" apply "$patch_file"
    cleanup_patch=1
fi

cp -- "$config_file" "$output_dir/.config"
make -C "$source_dir" O="$output_dir" ARCH=arm64 LLVM=1 LLVM_IAS=1 \
    CROSS_COMPILE=aarch64-linux-gnu- CLANG_TRIPLE=aarch64-linux-gnu- olddefconfig
cmp -s "$config_file" "$output_dir/.config" || {
    printf 'olddefconfig changed the reviewed configuration\n' >&2; exit 1;
}
if grep -q '^CONFIG_KSU=y\|^CONFIG_KSU=m' "$output_dir/.config"; then
    printf 'KernelSU must remain disabled for this Debian candidate\n' >&2; exit 1
fi

jobs=${JOBS:-2}
export LC_ALL=C TZ=UTC
export KBUILD_BUILD_USER=${KBUILD_BUILD_USER:-SM-A105F}
export KBUILD_BUILD_HOST=${KBUILD_BUILD_HOST:-reproducible-builder}
export KBUILD_BUILD_VERSION=${KBUILD_BUILD_VERSION:-1}
export KBUILD_BUILD_TIMESTAMP=${KBUILD_BUILD_TIMESTAMP:-$(git -C "$source_dir" show -s --format=%cI "$expected_source")}
# This old kernel increments .version at each vmlinux link, regardless of
# KBUILD_BUILD_VERSION. Reset this generated build counter for stable output.
printf '0\n' > "$output_dir/.version"
make -C "$source_dir" O="$output_dir" ARCH=arm64 LLVM=1 LLVM_IAS=1 \
    CROSS_COMPILE=aarch64-linux-gnu- CLANG_TRIPLE=aarch64-linux-gnu- \
    -j"$jobs" Image modules dtbs

[[ -s "$output_dir/arch/arm64/boot/Image" && -s "$output_dir/vmlinux" ]] || {
    printf 'Kernel build did not produce Image and vmlinux\n' >&2; exit 1;
}
if command -v llvm-nm >/dev/null && llvm-nm -u "$output_dir/vmlinux" | grep -q 'ksu_'; then
    printf 'Kernel image retains undefined KernelSU hooks\n' >&2; exit 1
fi
make -s -C "$source_dir" O="$output_dir" ARCH=arm64 LLVM=1 LLVM_IAS=1 \
    CROSS_COMPILE=aarch64-linux-gnu- CLANG_TRIPLE=aarch64-linux-gnu- kernelrelease
file "$output_dir/arch/arm64/boot/Image" "$output_dir/vmlinux"
sha256sum "$output_dir/arch/arm64/boot/Image" "$output_dir/.config" \
    "$output_dir/System.map"
