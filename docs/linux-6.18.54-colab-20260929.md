# Linux 6.18.54 A10 port checkpoint — 2026-09-29

## Scope and provenance

The active upstream source snapshot is Linux stable 6.18.54, commit 1b357ecb321392158d507b04672ffee57bfa071d, in the user's Colab runtime. The A10 SoC is Exynos7884B, in the Exynos7885 family. The modern jackpotlte board DTB is for Galaxy A8 (SM-A530F) and is reference-only.

A public community downstream Exynos7885/A10 tree (geckyn, android_kernel_samsung_exynos7885, branch exelixis-2019-04-05_clang_lto) provided comparative legacy A10 configuration. It identifies removable SD controller address 0x13550000, IRQ 147, four-bit SD bus, card detect at GPIO GPA0 line 7, and CIU divider 3 with timing tuples SDR <3 0 2 0>, DDR <3 0 2 1>. This tree is comparative evidence, not the user's supplied exact Samsung source and not an independent upstream validation.

## Implemented fragment

The Exynos7885 SoC include now describes the second DesignWare MMC host at 0x13550000 using upstream-compatible names and clock handles. It is disabled by default. Timing parameters satisfy the Linux samsung,exynos-dw-mshc.yaml binding requirements for samsung,exynos7-dw-mshc. Board pinctrl, card-detect polarity, supplies, slot, and status=okay remain out of the shared SoC include.

Patch: patches/linux-6.18.54/0001-arm64-dts-exynos-add-exynos7885-sd-host.patch

## Verification performed

- make -s -j2 ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- dtbs completed successfully after the fragment was applied.
- git diff --check completed without output.
- A targeted dtbs_check is running in the Colab runtime after installing dtschema; result pending.
- This is a DTB host build only. No A10 board DTB was built and no handset boot/device validation is claimed.

## Boot/recovery research checkpoint

- AOSP documents boot header v1's component size/address fields and says v1/v2 support recovery DTBO sections. Its generic description does not establish what SM-A105F boot ROM/bootloader accepts, Samsung footer handling, AVB state, or the correct ramdisk address for this handset.
- AOSP describes DT table entry id/rev/custom selectors as optional hardware IDs which a bootloader may use; it does not prescribe this Samsung model's selection policy. The existing host-generated zero-selector table remains structural evidence only, and its selector match with stock is unknown.
- TeamWin's current Galaxy A10 support page warns that its device workflow uses recovery partition semantics and that A10 stock AVB protects boot/recovery images through vbmeta; this is third-party A10-specific operational evidence, not proof of the exact installed SM-A105F firmware's state. Treat vbmeta and recovery as protected until exact AP package/partition table and installed build are verified.
- A community service-forum post quotes an A105F PIT log with a 36 MiB BOOT entry. This is weak, variant/build-uncertain evidence and cannot establish this handset's current partition layout or writable capacity. Stock candidate boot file length is not a capacity measurement.
- Samsung Knox documentation states loading a non-Knox kernel can irreversibly trip its warranty e-fuse and disable Knox-dependent services. This is a deployment consequence to include in a future informed physical-test gate.
- Do not claim a safe boot-image restore/recovery path until a verified matching full stock package, exact model/region/build, partition map, download-mode path, and rollback steps are available. Phone remains untouched.

## Remaining engineering gates

- Build a board-level SM-A105F/A10 DTS/DTBO against exact Samsung source, once the board memory/reserved-memory, regulator, GPIO and variant facts are mapped.
- Confirm card-detect polarity, SD supply/voltage behavior, and pinctrl with exact source; keep removable SD disabled until these are established.
- Resolve first-boot eMMC root partition identity and bootloader DT/DTBO selector behavior from exact firmware and partition table evidence.
- Obtain current physical firmware/build and bootloader state only at the approved read-only/device gate. No physical operation has occurred.
- Obtain the exact corrected initramfs/kernel artifacts in this runtime before regenerating the boot-v1 candidate; the Colab runtime currently holds only the Linux 6.18.54 source tree and no kernel Image/initramfs.

## Reproduction

    make -s -j2 ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- dtbs
    git diff --check
