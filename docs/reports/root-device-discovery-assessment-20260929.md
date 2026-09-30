# Fail-closed root discovery assessment — 2026-09-29

## Current handoff

The initramfs takes an explicit `root=/dev/mmcblk0pN` argument, requires a block device, waits up to 30 seconds, mounts the selected device, then requires executable `/sbin/init`. The selector rejects MMC devices other than the A10 eMMC alias `mmcblk0`, malformed paths, UUID and PARTUUID forms. The actual physical partition number remains unknown and is not guessed.

## Can discovery safely avoid a pre-known partition number?

A deterministic mechanism is feasible without a UUID, but simple probing is unsafe. Scanning partitions and mounting each read-write, mounting the first filesystem containing `/sbin/init`, or accepting a label alone could select a backup, recovery, or unrelated partition.

A future opt-in `root=discover` mode could fail closed if all of these conditions are met:

1. Restrict candidates to `/dev/mmcblk0pN`; never scan removable SD, USB or other block devices.
2. Require an installation-specific marker whose expected value is supplied by the same boot configuration as the initramfs. The rootfs must contain the matching marker at a fixed path and executable `/sbin/init`.
3. Probe only the expected root filesystem type, read-only, with journal replay disabled (for ext4, `ro,noload`), and with `nodev,nosuid,noexec`. Do not run filesystem repair or write to a candidate during discovery.
4. Count matches. Continue only for exactly one matching eMMC partition. Zero matches, duplicate matches, mount ambiguity, unsupported options or a marker mismatch must enter emergency mode; never fall back to the first candidate.
5. After one exact marker match, unmount the probe and mount only that device read-write for handoff. Keep the current explicit measured path as the primary and simpler path.
6. Record the generated installation marker in the rootfs/boot manifest and verify that BusyBox, kernel filesystem options and partition enumeration implement every assumption.

This design avoids a pre-known partition number or UUID, but it still needs a deliberately provisioned marker and trustworthy expected value. A marker copied with a cloned rootfs could create multiple matches, which the uniqueness rule rejects.

## Decision

Do not implement discovery yet. The current rootfs artifact is an unprovisioned TAR, and the initramfs builder has no paired marker input. The verified static BusyBox is unavailable, so support for the required mount options and the complete early-boot behavior cannot be tested. Enabling speculative scanning now would weaken the simple, explicit handoff and might mount the wrong storage. The initramfs resolver-loading defect has been fixed separately; see `docs/reports/initramfs-root-helper-fix-20260929.md`.

When the physical storage layout and root partition are measured through an authorized future procedure, supply the exact eMMC partition path as `root=`. Revisit discovery only if avoiding that measured value is still needed and the paired marker, read-only probe and duplicate-match failure behavior can be fully host-tested.

No device operation occurred.


## Selector grammar clarification — 2026-09-30

The resolver accepts explicit `/dev/mmcblk0pN` paths only when `N` is positive and written without leading zeros. `mmcblk0p0` is not a valid partition node (the whole device is `/dev/mmcblk0`), and kernel device names do not use leading-zero partition suffixes. Regression cases reject both forms. This constrains syntax only; it does not establish which partition on a handset contains Debian.
