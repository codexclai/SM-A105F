#!/usr/bin/env bash
# Output-path helpers shared by the rootfs builder and focused host tests.

rootfs_refuse_existing_outputs() {
    local output=$1 checksum_output=$2
    [[ ! -e "$output" && ! -L "$output" ]] || {
        printf 'Refusing to overwrite existing output or symlink: %s\n' "$output" >&2
        return 2
    }
    [[ ! -e "$checksum_output" && ! -L "$checksum_output" ]] || {
        printf 'Refusing to overwrite existing checksum or symlink: %s\n' "$checksum_output" >&2
        return 2
    }
}

rootfs_publish_outputs() {
    local staged_output=$1 output=$2 staged_checksum=$3 checksum_output=$4
    # Hard links publish completed files exclusively and refuse to replace a
    # destination that appeared after the preflight check.
    ln -- "$staged_output" "$output" || {
        printf 'Could not publish output without replacing an existing path: %s\n' "$output" >&2
        return 1
    }
    if ! ln -- "$staged_checksum" "$checksum_output"; then
        [[ ! "$output" -ef "$staged_output" ]] || rm -f -- "$output"
        printf 'Could not publish checksum without replacing an existing path: %s\n' "$checksum_output" >&2
        return 1
    fi
}
