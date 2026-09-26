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
