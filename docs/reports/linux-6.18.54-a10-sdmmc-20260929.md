# SM-A105F A10 SD/MMC port — 2026-09-29

## Implemented

- Added the Exynos7885 removable SD host at `0x13550000`, size `0x2000`, GIC SPI 147, using the upstream card ACLK and SDCLKIN clocks. The shared SoC node remains `status = "disabled"`.
- Added the SM-A105F A10 board DTS and Makefile target. The board enables the host with a 4-bit bus, SD high-speed, disabled write-protect, SD2 clock/command/data pins, and GPA0 pin 7 as active-low external card detect in EINT mode.
- Used the two Samsung populated memory ranges from the SM-A105F base DTS: `0x80000000 + 0x3da00000` and `0xc0000000 + 0x40000000`. Unpopulated/reserved bank descriptions were not promoted into RAM.
- Do not advertise UHS SDR50/SDR104 yet. The Samsung overlay contains mode-specific tuples for those modes, but Linux 6.18 has no corresponding properties and the board's 1.8 V `vqmmc` regulator mapping is unresolved.

## Timing translation evidence

Samsung's 4.4.177 `dw_mmc-exynos.c` reads four cells for its base SDR and DDR properties and passes them to `SDMMC_CLKSEL_TIMING(div, fine_drive, drive, sample)` in `dw_mmc-exynos.h`. The A10 values are:

| Legacy property | Legacy tuple | Linux 6.18 property | Result |
|---|---:|---|---|
| `samsung,dw-mshc-sdr-timing` | `<3 0 2 0>` | `samsung,dw-mshc-ciu-div = <3>`; `samsung,dw-mshc-sdr-timing = <0 2>` | sample 0, drive 2 |
| `samsung,dw-mshc-ddr-timing` | `<3 0 2 1>` | `samsung,dw-mshc-ciu-div = <3>`; `samsung,dw-mshc-ddr-timing = <1 2>` | sample 1, drive 2 |
| `samsung,dw-mshc-sdr50-timing` | `<3 0 4 2>` | none | unresolved; not emitted |
| `samsung,dw-mshc-sdr104-timing` | `<3 0 3 0>` | none | unresolved; not emitted |

The Linux 6.18 binding requires two-cell SDR and DDR arrays and the Samsung driver reads each as two cells, then forms timing using the separate CIU divider. The legacy fine-drive value is zero in both base tuples and there is no matching Linux 6.18 binding field. The mode-specific UHS tuples are not safely representable by the current binding/driver interface, so they were not converted. The exact A10 vendor overlay advertises UHS capability, but that is not enough evidence to claim the current port has equivalent timing or voltage switching.

Card-detect inversion in the Samsung driver applies to the sampled GPIO value. The vendor overlay identifies GPA0-7 as card detect, marks the path inverted, and assigns EINT function 0xf. The board DTS expresses the polarity through `GPIO_ACTIVE_LOW` and uses the upstream Exynos EINT macro.

## Focused validation

Source: `gregkh/linux` commit `1b357ecb321392158d507b04672ffee57bfa071d`, kernel version 6.18.54. Toolchain: GCC 13.3.0, `aarch64-linux-gnu-`.

Commands run in the Colab Linux source tree:

```text
make -s ARCH=arm64 dt_binding_check DT_SCHEMA_FILES=Documentation/devicetree/bindings/mmc/samsung,exynos-dw-mshc.yaml
exit 0 (yamllint was not installed; binding check skipped that optional lint step)

make -s -j2 ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- CHECK_DTBS=y DT_SCHEMA_FILES=Documentation/devicetree/bindings/mmc/samsung,exynos-dw-mshc.yaml exynos/exynos7885-a10.dtb
exit 0

dt-validate -l Documentation/devicetree/bindings/mmc/samsung,exynos-dw-mshc.yaml -u Documentation/devicetree/bindings -p Documentation/devicetree/bindings/processed-schema.json arch/arm64/boot/dts/exynos/exynos7885-a10.dtb
exit 0; no diagnostics

git diff --check
clean
```

A10 DTB SHA-256: `da3ce7e3a4d4d6d2a802b1c0b8a88d47886db8269eedc863ecf9f8419d9db30e`.

The Makefile's bounded single-DTB target was used rather than invoking a full architecture-wide schema sweep. An earlier full-tree `dtbs_check` run was interrupted during its large parallel DTB build and did not leave complete diagnostics; this is an incomplete run, not evidence of an A10 schema failure. The separate Jackpot LTE (SM-A530F/Exynos7885) result is sibling-only and is not A10 boot evidence.

## Still open

- VQMMC/VMMC regulator and PMIC mapping needed before claiming UHS or voltage switching.
- Linux 6.18 has no equivalent properties for the legacy SDR50 and SDR104 timing tuples; controller behavior at those modes is not validated.
- Reconcile all Samsung DRAM banks/reservations against the actual A10 revision before relying on this RAM description.
- Obtain and round-trip verify the exact Samsung-built kernel, corrected initramfs, A10 base DTB/DTBO, and package manifest together before generating a host-only boot-v1 candidate.
- No boot image was made from this DTB. No physical phone operation occurred; the phone remains untouched.

## Source identity

Samsung source archive SHA-256: `5c83be7c2452d644ccda1deb898d9a54f2b3d53d3a0e66a7a394dcbf14439931`.
Relevant extracted files: vendor Exynos7885 base DTS, A10 SWA overlay/GPIO include, and `drivers/mmc/host/dw_mmc-exynos.{c,h}`.

## Artifact acquisition and packaging research — 2026-09-29

The connected project Drive folder inventory contained the Samsung source archive chunks, checkpoint, repo bundles, and Eureka host-build archives, but no standalone exact Samsung-built 4.4.177 kernel, corrected initramfs, A10 DTB/DTBO binaries, checksums manifest, or complete boot candidate. The existing draft GitHub release lists `SM-A105F-host-only-boot-candidate-20260928.tar.gz` at 12,118,381 bytes with asset SHA-256 `f28d6a293695ae6075123a4ed9af0a9c5f19b0f7fe6c125c98a71e87cfd98ae5`. The connected GitHub API exposes metadata but not binary bytes. Opening the asset download from the signed-in browser was blocked by the browser security policy; no alternate download route was attempted. The Codespaces dashboard shows the existing `stunning acorn` Codespace but reports that the monthly free usage/budget is exhausted, so no Codespace was started or changed. Therefore no rebuilt boot image or round-trip verification is claimed in this environment.

A public generated recovery device tree for `SM-A105F` was inspected at `twrpdtgen/android_device_samsung_a10`, branch `a10dd-user-11-RP1A.200720.012-A105FDDS9CWD2-release-keys`. Its `BoardConfig.mk` specifies boot header v1, kernel base `0x10000000`, kernel pagesize 2048, ramdisk offset `0x01000000`, tags offset `0x100`, a separate DTBO image, 55,574,528-byte boot/recovery partition constants, and AVB recovery settings using AOSP's test key. Its recovery fstab names `boot`, `recovery`, `dtb`, `dtbo`, and `vbmeta_samsung` by-name partitions. These are community build inputs, include test-key settings, and do not establish stock partition geometry, actual AVB policy, current root device, signature acceptance, or boot success. They are leads for later comparison against Samsung firmware/partition tables.

The existing checkpoint identifies the exact Samsung-built Image as 29,112,000 bytes, SHA-256 `f68c9992e7fa2c663d3b0c1664d6c786f2ca5bde4a9e90775c95f5f97451e`, the corrected initramfs as SHA-256 `f4112366306b8b26c295a715350398e96a737b4e817425ffd73f010b565729e0`, and earlier A10 DT/DTBO candidates with hashes `15c28d3b14250f0c75be58523ca7c0c5164bc422fa6e3ad6d9b970c45bca5fca` and `93a16c9040e2b8ce62ccb0b57fd23ed1febd0e4a7f36c82b333a20d63a009164`. Those bytes are not present in the active workspace for joint identity/packaging verification. The checkpoint's previous boot-v1 candidate has kernel address `0x10008000`, tags `0x10000100`, and ramdisk address `0x11000000`; these values remain historical package metadata pending reacquisition and parser round-trip. The exact DTBO firmware container was earlier recorded as 8,388,608 bytes SHA-256 `eb32301133ba5742afe0d782c83bd7b75ac040cbb115015a355d902702db737`, also not currently available for byte-level verification.


### Packaging parser and bootloader follow-up

The active project snapshot's host-side packaging/parser suite passed `python3 -m unittest discover -s tests -v`: 31 tests, zero failures. This checks the packaging tools and fixtures; it does not replace round-tripping the missing Samsung/Image/initramfs/DT inputs.

The corrected initramfs source requires an explicit `root=UUID=...` or `root=PARTUUID=...` kernel argument, resolves it through `/dev/disk/by-uuid` or `/dev/disk/by-partuuid`, and enters an emergency shell if missing or unresolved. No A10 Debian partition identifier has been established, so the command line and final root-device selection remain open.

AOSP's bootloader reference documents that unlocking is a state change that enables reflashing and normally triggers a factory data reset; that is generic Android guidance, not evidence of the SM-A105F implementation or current lock state. Source: https://source.android.com/docs/core/architecture/bootloader/locking_unlocking . The inspected community recovery recipe's test AVB key and future-dated patch-level workaround do not demonstrate a Samsung-accepted signature or safe locked-device path. No unlock, signing, flash, recovery boot, or other phone operation was performed or authorized.
