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
[[ ! -e "$output" ]] || { printf 'Refusing to overwrite %s\n' "$output" >&2; exit 2; }

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
mkdir -p -- "$(dirname -- "$output")"
sources=$(mktemp)
trap 'rm -f -- "$sources"' EXIT
cat > "$sources" <<'SOURCES'
deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian trixie main
deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian trixie-updates main
deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://security.debian.org/debian-security trixie-security main
SOURCES

mmdebstrap --mode=root --architectures=arm64 --variant=minbase --format=tar \
    --include=systemd-sysv,openssh-server,iproute2,ca-certificates,kmod \
    trixie "$output" "$sources"
sha256sum -- "$output" > "$output.sha256"
printf 'Unprovisioned rootfs: %s\nChecksum: %s.sha256\n' "$output" "$output"
