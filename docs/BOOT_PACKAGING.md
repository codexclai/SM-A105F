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


## GitHub A10 source and image evidence — 2026-09-27

### Target-specific kernel and board tree

A public GitHub mirror, [neronewman/A10-A105F-kernel at ad623e4df6718c2c371eee6d5fa8c4e1108b75bc](https://github.com/neronewman/A10-A105F-kernel/tree/ad623e4df6718c2c371eee6d5fa8c4e1108b75bc), contains a Samsung A10 source snapshot. Its README identifies it as SM-A105F source from Samsung Open Source Release Center (a repository claim, not an independently verified original ZIP). `Kernel/Makefile` identifies Linux 4.4.111; `Kernel/arch/arm64/configs/a10_00_defconfig` has `CONFIG_ARM64=y`. The tree has the A10 SWA board source `exynos7884B-a10_swa_open_00.dts` and related common/GPIO includes. That DTS declares `samsung,A10 SWA OPEN 00`, `samsung,EXYNOS7884B`, and hardware revision range 0–255. The mirror commit is dated 2020-04-17 and has no verifiable Samsung archive checksum. This is useful source/provenance evidence, not proof of the original archive identity.

The TWRP generator tree [twrpdtgen/android_device_samsung_a10 at af1681558e88d88a625115334724dca8acfbdd80](https://github.com/twrpdtgen/android_device_samsung_a10/tree/af1681558e88d88a625115334724dca8acfbdd80) names model SM-A105F and records build fingerprint `samsung/a10dd/a10:11/RP1A.200720.012/A105FDDS9CWD2:user/release-keys` in `omni_a10.mk`. Its `BoardConfig.mk` specifies boot header version 1, page size 2048, kernel base `0x10000000`, ramdisk offset `0x01000000`, tags offset `0x00000100`, and `Image`. It refers to a prebuilt DTBO. Its `recovery.fstab` exposes distinct `dtb` and `dtbo` partitions. These are build-tree settings for that community recovery target, not an extracted stock boot image or proof of this handset's installed firmware.

The TWRP tree sets recovery `TARGET_ARCH := arm`; the Samsung A10 kernel defconfig independently sets `CONFIG_ARM64=y`. Thus the recovery userspace setting must not be mistaken for the kernel's bitness.

### DTBO payload parsed and checked

I fetched the community tree's [`prebuilt/dtbo.img`](https://github.com/twrpdtgen/android_device_samsung_a10/blob/af1681558e88d88a625115334724dca8acfbdd80/prebuilt/dtbo.img) from that exact commit and inspected the bytes without modifying the image. Size is 89,232 bytes; SHA-256 is `0ab4db461c3d9c7467859d99c23dee7f9da54c9af2f884c4880f5570564a7ad7`. Its Android DT table has magic `0xd7b7ab1e`, version 0, 32-byte header/entries, one entry, page size 2048, ID/revision 0/0, and custom values `[0, 255, 0, 0]`. The FDT strings identify `samsung,A10 SWA OPEN 00` and `samsung,EXYNOS7884B`; this resolves the SWA-versus-SEA ambiguity in the custom metadata for this community prebuilt. It is a specific SWA candidate associated with the tree's D9CWD2 product description, not evidence of the active overlay on the physical phone.

Added `scripts/inspect_android_dtbo.py` and five unit tests. The parser validates table/entry bounds, page size, non-overlap, and FDT magic; it reports metadata and does not select an overlay. `python3 -m unittest discover -s tests -v` passed 5/5. The checker was also run against the fetched prebuilt above and reported the values recorded here. The fetched binary is not committed as a firmware artifact.

### Packaging conclusion

The TWRP header/page/offset recipe agrees with the Eureka offsets, but its configured boot/recovery image limit is 55,574,528 bytes (53 MiB), while the Eureka common recipe says a 37,748,736-byte boot limit (36 MiB). Both values are downstream build settings and neither has been confirmed as the stock partition's actual byte size. The target-family evidence now supports a header-v1, 2 KiB-page packaging candidate and a separate DTBO path; it still does not establish stock ramdisk contents/compression, boot image kernel payload encoding, stock DTB placement, exact stock cmdline, or partition capacity.

The D9CWD2 fingerprint is a useful matching AP-firmware search candidate, not the installed firmware identifier. The exact AP archive (or stock `boot.img`, `dtb.img`, and `dtbo.img` extracted from the phone's confirmed build) remains necessary before building a Debian boot image. Do not combine the community prebuilt and Eureka kernel based only on matching offsets. Keep the device untouched.

### Kernel path update

The 4.4 vendor path now has both the previously built Eureka R24U candidate (Linux 4.4.302-p6) and a GitHub Samsung-source mirror (Linux 4.4.111) with A10 ARM64 defconfig and board DTS evidence. R24U remains the established host-build track; the 4.4.111 mirror is a distinct provenance/reference source, not a replacement binary. The modern 6.x upstream tree still lacks an A10/7884B DTS; the Samsung A10 DTS provides a concrete hardware-description source to port, but no modern A10 kernel has been built or validated in this session.
