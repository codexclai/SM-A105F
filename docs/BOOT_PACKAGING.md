# SM-A105F boot packaging evidence

## Evidence boundary

This note records a downstream Android build recipe. It is not a dump of the installed Samsung boot partition and does not establish the currently installed firmware, image header version, ramdisk format, DTB placement, or board overlay selection.

## Pinned Eureka device-tree recipe

Reviewed source: https://github.com/eurekadevelopment/android_device_samsung_exynos7885/tree/9bc3736454ee43dcdff12ad86189b2a96fdb2678.

| Setting | Value | Source |
|---|---|---|
| Device target | a10, a10dd | a10/BoardConfig.mk |
| Kernel config | exynos7885-a10_defconfig | a10/BoardConfig.mk |
| Kernel image name / arch | Image / arm64 (a10dd configured separately as ARM32) | universal7885-common/BoardConfigCommon.mk |
| Base / page size | 0x10000000 / 2048 | same |
| Kernel / ramdisk / tags offsets | 0x00008000 / 0x01000000 / 0x00000100 | same (BOARD_MKBOOTIMG_ARGS) |
| Boot partition size | 37,748,736 bytes (36 MiB) | same |
| Recovery partition size | 55,574,528 bytes | a10/BoardConfig.mk |
| DTBO build | mkdtimg cfg_create eureka_dtbo.img a10.cfg -d <dtbo-dir> | universal7885-common/dtbo/Android.mk |

The seven A10 overlay entries in universal7885-common/dtbo/a10.cfg are:

| DTBO | custom0 | custom1 |
|---|---:|---:|
| exynos7884B-a10_kor_open_00.dtbo | 0x00 | 0x02 |
| exynos7884B-a10_eur_open_01.dtbo | 0x05 | 0xff |
| exynos7884B-a10_swa_open_00.dtbo | 0x00 | 0xff |
| exynos7884B-a10_eur_open_00.dtbo | 0x00 | 0x04 |
| exynos7884B-a10_kor_open_05.dtbo | 0x05 | 0xff |
| exynos7884B-a10_sea_open_00.dtbo | 0x00 | 0xff |
| exynos7884B-a10_kor_open_03.dtbo | 0x03 | 0x04 |

These values corroborate the seven overlays in the prior Eureka build. They do not identify the active overlay on this handset or prove Samsung stock partition structure.

## Debian boot image requirements still gated

A defensible first boot image requires matching AP firmware original boot.img and dtbo.img (or full AP archive), extracted and inspected for boot header/version, page size, offsets, compression, ramdisk contents, embedded/external DTB arrangement, DTBO table metadata, and exact board ID/revision selection. Preserve hashes and firmware build provenance. Then construct an image using only header fields demonstrated by those originals, a kernel built for A105F, the matching base DTB and selected overlay set, and a Debian initramfs. Validate image parsing, partition-size fit, and checksums before any device action. Do not assume an initramfs or generic DTB from the Eureka recipe is stock-compatible.

Unknown from the inspected downstream recipe: boot header version, boot ramdisk compression and source, stock cmdline, DTB location, stock DTBO partition format/metadata, exact overlay for the handset, and installed firmware build. No image should be flashed until those are resolved and the user separately authorizes physical-device action.

## Kernel paths

- Linux 4.4 Eureka R24U remains the nearer-term hardware bring-up path because it is the existing device-family vendor kernel with the prior Debian config/build. It is old and still needs matching stock image metadata and firmware provenance; the recipe above does not itself establish bootability.
- Linux 6.18.54 is the current LTS source snapshot selected for the modern-path experiment (kernel.org, 2026-09-25). The upstream tree has Exynos7885 support and a jackpotlte DTS, but no A10/SM-A105F/exynos7884B board DTS was found in that tree. A successful generic build is useful compile evidence only; jackpotlte is another device and is not a substitute A10 DTB.

## Acquisition blocker

Samsung source portal and the SamFW listing both presented human-verification challenges in this browser. No challenge was solved or bypassed. Samsung source archive SM-A105F_SWA_RR_Opensource.zip and exact AP archive for SM-A105F/SLK/A105FDDS9CWB3 have not been acquired or hashed. Samsung update notice identifies build A105FDDS9CWB3; that listing does not prove it is the handset installed build. Required next evidence is the original AP archive or extracted stock boot.img + dtbo.img for the handset exact firmware; the Samsung OSS archive is also needed to authenticate the vendor-kernel source baseline.


## 2026-09-27: measured user-supplied firmware boot layout

Candidate input: Android 11 firmware archive `A105FDDS9CWB3` supplied by the user. It is not verified as the handset's currently installed build. Parsed image metadata and hashes are persisted in [the machine-readable layout report](reports/a105f-cwb3.json).

| AP image | Measured layout | SHA-256 |
| --- | --- | --- |
| `boot.img` | 37,748,736 bytes; Android boot header v1; page 2048; kernel 2,911,200 bytes at 0x10008000; ramdisk 0; second loader 0; tags 0x10000100; Android 11, patch 2023-02 | `4dfa2224281458cd0ac3a0aa752681eb6445836fc0d58cea69225dfab113476e` |
| `dt.img` | 8,388,608 bytes; Android DT table v0, page 2048, one FDT at offset 64, 90,300 bytes; compatible `samsung,armv8` / `samsung,exynos7885` | `829b27e3b9235d6603701a25f21dd0240bd5cb43ddc8bbf3c383d30a353a475` |
| `dtbo.img` | 8,388,608 bytes; Android DT table v0, page 2048, one FDT at offset 64, 89,168 bytes; compatible `samsung,A10 SWA OPEN 00` / `samsung,EXYNOS7884B`; entry ID/revision 0/0, custom values [0,255,0,0] | `eb32301133ba5742afe0d782c83bd7b75ac040cbb115015a355d902702db737` |

The stock boot header declares an empty ramdisk. Bytes outside its described kernel/header sections include nonzero, vendor-specific data and a `SEANDROIDENFORCE` marker; the tail has not been classified as a whole. Do not pass that tail off as an initramfs. Debian boot therefore requires an explicit, nonempty Debian initramfs plus a selected kernel and a board-matched DTB/overlay. The firmware candidate provides useful DT/DTBO evidence, but does not identify which overlay the handset selects.

The boot image is exactly 36 MiB, matching the size in the downstream Eureka BoardConfig recipe. That coincidence is not independent proof of the installed boot partition capacity or of the complete partition map. Downstream Eureka offsets (base 0x10000000, kernel 0x8000, ramdisk 0x01000000, tags 0x100) remain candidate recipe values, not all observed stock header values. No flash or device action has occurred.

Stock kernel extracted from the declared kernel payload reports Linux 4.4.177-2184546, build #1 SMP PREEMPT, Wed Feb 22 02:47:35 KST 2023, GCC 4.9. This is distinct from the available Eureka source tree's 4.4.111 baseline. The existing 134-byte Eureka initramfs stub is empty and is not Debian boot media. The 6.18.54 modern source remains a generic Exynos7885 bring-up path without A10/A105F board DTS.
