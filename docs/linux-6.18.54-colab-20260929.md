# Linux 6.18.54 A10 port checkpoint — 2026-09-29

## Scope and provenance

The active upstream source snapshot is Linux stable 6.18.54, commit 1b357ecb321392158d507b04672ffee57bfa071d, in the user's Colab runtime. The A10 SoC is Exynos7884B, in the Exynos7885 family. The modern jackpotlte board DTB is for Galaxy A8 (SM-A530F) and is reference-only.

A public community downstream Exynos7885/A10 tree (geckyn, android_kernel_samsung_exynos7885, branch exelixis-2019-04-05_clang_lto) provided comparative legacy A10 configuration. It identifies removable SD controller address 0x13550000, IRQ 147, four-bit SD bus, card detect at GPIO GPA0 line 7, and CIU divider 3 with timing tuples SDR <3 0 2 0>, DDR <3 0 2 1>. This tree is comparative evidence, not the user's supplied exact Samsung source and not an independent upstream validation.

## Implemented fragment

The Exynos7885 SoC include now describes the second DesignWare MMC host at 0x13550000 using upstream-compatible names and clock handles. It is disabled by default. Timing parameters satisfy the Linux samsung,exynos-dw-mshc.yaml binding requirements for samsung,exynos7-dw-mshc. Board pinctrl, card-detect polarity, supplies, slot, and status=okay remain out of the shared SoC include.

## Verification performed

- make -s -j2 ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- dtbs completed successfully after the fragment was applied.
- git diff --check completed without output.
- No dtbs_check run yet; the Colab runtime does not currently have the dtschema validator confirmed installed.
- This is a DTB host build only. No A10 board DTB was built and no handset boot/device validation is claimed.

## Remaining engineering gates

- Build a board-level SM-A105F/A10 DTS/DTBO against exact Samsung source, once the board memory/reserved-memory, regulator, GPIO and variant facts are mapped.
- Confirm card-detect polarity, SD supply/voltage behavior, and pinctrl with exact source; keep removable SD disabled until these are established.
- Resolve first-boot eMMC root partition identity and bootloader DT/DTBO selector behavior from exact firmware and partition table evidence.
- Obtain current physical firmware/build and bootloader state only at the approved read-only/device gate. No physical operation has occurred.
- Obtain the exact corrected initramfs/kernel artifacts in this runtime before regenerating the boot-v1 candidate; the Colab runtime currently holds only the Linux 6.18.54 source tree and no kernel Image/initramfs.

## Reproduction

    make -s -j2 ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- dtbs
    git diff --check
