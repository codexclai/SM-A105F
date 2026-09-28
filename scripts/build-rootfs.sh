#!/usr/bin/env bash
# Build an unprovisioned Debian ARM64 tarball. This is not a deployable image.
set -euo pipefail

usage() {
    printf 'Usage: %s OUTPUT.tar\n' "$0" >&2
    exit 2
}

[[ $# -eq 1 ]] || usage
output=$1
[[ "$output" = /* ]] || { printf 'Output must be an absolute path\n' >&2; exit 2; }
[[ "$output" = *.tar ]] || usage
checksum_output="$output.sha256"
source "$(dirname -- "${BASH_SOURCE[0]}")/rootfs-output.sh"
rootfs_refuse_existing_outputs "$output" "$checksum_output" || exit $?

for tool in mmdebstrap qemu-aarch64-static sha256sum; do
    command -v "$tool" >/dev/null || { printf 'Missing required tool: %s\n' "$tool" >&2; exit 1; }
done
[[ $(id -u) -eq 0 ]] || { printf 'Requires a root-capable isolated build environment\n' >&2; exit 1; }
[[ -f /usr/share/keyrings/debian-archive-keyring.gpg ]] || {
    printf 'Missing Debian archive keyring\n' >&2; exit 1;
}
if [[ ! -r /proc/sys/fs/binfmt_misc/qemu-aarch64 ]]; then
    printf 'Missing registered qemu-aarch64 binfmt handler\n' >&2
    exit 1
fi
output_dir=$(dirname -- "$output")
output_name=$(basename -- "$output")
mkdir -p -- "$output_dir"
# Build in a private sibling directory so failed mmdebstrap runs do not leave a
# partial final archive. A sibling also lets ln publish without copying bytes.
staging_dir=$(mktemp -d --tmpdir="$output_dir" ".${output_name}.build.XXXXXXXX")
staged_output="$staging_dir/$output_name"
staged_checksum="$staged_output.sha256"
sources=''
cleanup() {
    [[ -z "$sources" ]] || rm -f -- "$sources"
    [[ -z "$staging_dir" ]] || rm -rf -- "$staging_dir"
}
trap cleanup EXIT
sources=$(mktemp)
cat > "$sources" <<'SOURCES'
deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian trixie main
deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian trixie-updates main
deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://security.debian.org/debian-security trixie-security main
SOURCES

mmdebstrap --mode=root --architectures=arm64 --variant=minbase --format=tar \
    --include=systemd-sysv,openssh-server,iproute2,ca-certificates,kmod \
    --customize-hook='printf "127.0.0.1 localhost\\n::1 localhost ip6-localhost ip6-loopback\\n" > "$1/etc/hosts"' \
        --customize-hook='printf "a10\n" > "$1/etc/hostname"' \
    trixie "$staged_output" "$sources"
(cd -- "$staging_dir" && sha256sum -- "$output_name" > "$output_name.sha256")

rootfs_publish_outputs "$staged_output" "$output" "$staged_checksum" "$checksum_output"
printf 'Unprovisioned rootfs: %s\nChecksum: %s\n' "$output" "$checksum_output"
