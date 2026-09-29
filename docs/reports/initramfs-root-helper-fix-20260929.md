# Initramfs root resolver load fix — 2026-09-29

## Finding

At private `main` `d652bac4c8084eb17ff197465776e6d161de3bf0`, `configs/initramfs/a105f-init` called `root_spec_supported` and `resolve_root_device`, but did not source `/lib/root-device.sh`. The builder already places that helper at `/lib/root-device.sh`, so the calls were undefined at runtime and root selection would fail.

## Change

Commit `76123c668533a8d98a45a67c126671eadc910fe9` adds:

```sh
. /lib/root-device.sh || emergency 'root-device resolver unavailable'
```

before root argument validation and resolution.

Commit `5c03c3c8dd1c74f2d2198b13e530486896751bd7` strengthens `tests/test_a105f_initramfs.sh` to require the resolver source line and compare the extracted archive's `/init` with the current source file. This catches omission of the correction from a future archive build.

## Verification

- Read back both changed files from the private GitHub `main` branch after commit `5c03c3c8dd1c74f2d2198b13e530486896751bd7`.
- `sh -n` passed for `a105f-init` and `root-device.sh`.
- `bash -n` passed for both initramfs and selector test scripts.
- `tests/test_root_device_selector.sh` passed against the read-back `root-device.sh`; it verifies explicit `/dev/mmcblk0pN` selection and rejects other eMMC/MMC paths, UUID, PARTUUID and non-eMMC paths.
- Full archive extraction and ARM64 BusyBox/QEMU checks were not run because this runtime has no verified ARM64 static BusyBox or corrected archive. No new initramfs binary or hash is claimed.

This fixes a host-side source-level defect. It does not establish root-partition identity, initramfs bootability, or physical-device behavior. The phone remains untouched.
