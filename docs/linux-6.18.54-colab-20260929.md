# Linux 6.18.54 A10 port checkpoint — 2026-09-29

## Scope and provenance

The active upstream source snapshot is Linux stable 6.18.54, commit 1b357ecb321392158d507b04672ffee57bfa071d, in the user's Colab runtime. The A10 SoC is Exynos7884B, in the Exynos7885 family. The modern jackpotlte board DTB is for Galaxy A8 (SM-A530F) and is reference-only.

A public community downstream Exynos7885/A10 tree (geckyn, android_kernel_samsung_exynos7885, branch exelixis-2019-04-05_clang_lto) provided comparative legacy A10 configuration. It identifies removable SD controller address 0x13550000, IRQ 147, four-bit SD bus, card detect at GPIO GPA0 line 7, and CIU divider 3 with legacy timing tuples SDR <3 0 2 0>, DDR <3 0 2 1>. The legacy driver defines the tuple order as divider, fine-drive, drive, sample, and reads four cells. This tree is comparative evidence, not the user's supplied exact Samsung source.

## Implemented fragment

A candidate Exynos7885 SoC fragment describes the second DesignWare MMC host at 0x13550000 using the upstream compatible, clock handles, and two-cell timing format. The four legacy timing values map to upstream timing order (sample, drive), while CIU divider is now a separate property: SDR <0 2>, DDR <1 2>, divider <3>. The current upstream binding requires two timing cells, and the current driver reads exactly two. This conversion is code-derived, not a direct electrical validation. The node remains disabled. IRQ 147 and the host's presence still rely on community A10/Exynos7885 evidence; exact Samsung source confirmation is outstanding. Board pinctrl, card-detect polarity, supplies, slot, and status=okay remain out of the shared SoC include.

Patch: patches/linux-6.18.54/0001-arm64-dts-exynos-add-exynos7885-sd-host.patch

## Verification performed

- make -s -j2 ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- dtbs completed successfully after the fragment was applied.
- git diff --check completed without output.
- A targeted dtbs_check was started in Colab against the first revision, before the two-cell conversion; it had not returned by the latest inspection. Re-run it after applying the corrected patch. The initial schema failure (if any) must not be reported as validation of this corrected candidate.
- This is a DTB host build only. No A10 board DTB was built and no handset boot/device validation is claimed.

## Boot, partitions, and recovery research

- AOSP documents boot header v1 component size/address fields and says v1/v2 support recovery DTBO sections. Its generic description does not establish what SM-A105F boot ROM/bootloader accepts, Samsung footer handling, AVB state, or the correct ramdisk address for this handset.
- The community twrpdtgen/android_device_samsung_a10 branch a10dd-user-11-RP1A.200720.012-A105FDDS9CWD2-release-keys has a BoardConfig that specifies header version 1, 2048-byte pages, base 0x10000000, ramdisk offset 0x01000000, tags offset 0x100, separate DTBO, AVB enabled, and 55,574,528-byte boot/recovery image partition-size variables. This is a generated third-party Android recovery configuration; those values are hypotheses/reference data, not proof of the target handset's partition capacity, current AVB metadata, acceptance rules, or suitability for Debian.
- The same branch's recovery.fstab maps Android system root to /dev/block/by-name/system and userdata to /dev/block/by-name/userdata, lists boot, recovery, dtb, dtbo and vbmeta_samsung names, and maps removable SD to mmcblk0p1. It is useful Android layout evidence, not authorization or a recommendation to overwrite system/userdata. Exact current handset mapping and Debian root-device choice remain unverified.
- A separate community service-forum post quotes an A105F PIT log with 36 MiB BOOT and 53 MiB RECOVERY entries. The values broadly align with the candidate stock boot length and the generated TWRP recovery-size variable, but the post does not establish firmware variant, handset identity, or current PIT; treat it as corroboration of low confidence only.
- TeamWin's current Galaxy A10 support page warns that its device workflow uses recovery-partition semantics and that stock AVB protects boot/recovery images through vbmeta. This is third-party A10-specific operational evidence, not proof of the exact installed SM-A105F firmware state. Treat vbmeta and recovery as protected until exact AP package and installed build are verified.
- Heimdall documents Samsung's Odin 3 protocol and supports PIT operations generically; this does not prove compatibility with SM-A105F's current Download Mode/protocol revision. Keep it as a possible recovery tool to qualify against a matching PIT and verified stock firmware, not a guaranteed rollback path.
- Samsung Knox documentation states loading a non-Knox kernel can irreversibly trip its warranty e-fuse and disable Knox-dependent services. Include this consequence in any future informed physical-test gate.
- No defensible first-flash or rollback procedure is established yet. Require a verified matching full stock package, exact model/region/build, current partition evidence, tested Download Mode transport compatibility, and a recovery sequence before any physical write. Phone remains untouched.

## DTBO selector notes

AOSP documents dt_table_entry id/rev/custom fields as optional hardware IDs that the bootloader may use; the bootloader may also inspect properties inside the FDT. It does not prescribe SM-A105F selection policy. The host-generated zero-selector table remains structural evidence only; selector matching with stock and overlay-selection behavior remain unknown.

## Remaining engineering gates

- Build a board-level SM-A105F/A10 DTS/DTBO against exact Samsung source, once board memory/reserved-memory, regulators, GPIOs and variant facts are mapped.
- Confirm the host register/IRQ mapping, SD card-detect polarity, supply/voltage behavior and pinctrl with the exact source; keep removable SD disabled until these are established.
- Resolve first-boot eMMC root partition identity and bootloader DT/DTBO selector behavior from exact firmware and partition-table evidence.
- Obtain current physical firmware/build and bootloader state only at the approved read-only/device gate. No physical operation has occurred.
- Obtain the exact corrected initramfs/kernel artifacts in this runtime before regenerating the boot-v1 candidate; the Colab runtime currently holds only the Linux 6.18.54 source tree and no kernel Image/initramfs.

## Reproduction

    make -s -j2 ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- dtbs
    git diff --check
