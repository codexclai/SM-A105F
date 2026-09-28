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


## TeraBox firmware link attempt — 2026-09-27

The user-supplied TeraBox share visibly identifies `SAMFW.COM_SM-A105F_A105FDDS9CWB3_fac_265315.zip` (dated 2023-10-25). After the user authorized the Google OAuth consent, the consent tab was no longer present when checked; the TeraBox share then opened without the earlier login overlay. Clicking its Download control navigated to a `terabox://transfer/` custom protocol instead of producing a browser download. The browser security policy blocks further access to that protocol, so no transfer/download was verified and no firmware bytes were acquired. No CAPTCHA or bot check was solved or bypassed. The shared AP filename is not proof that this is the handset's installed build.

The DTBO inspector and its existing fixture were rerun in this workspace: 5/5 tests passed, and the community DTBO parsed as one 2 KiB-page SWA candidate (artifact SHA-256 remains `0ab4db461c3d9c7467859d99c23dee7f9da54c9af2f884c4880f5570564a7ad7`). The exact handset-matching stock AP inputs remain the blocker. Next, obtain the confirmed-build AP archive or its `boot.img`, `dtb.img`, and `dtbo.img` as files available for read-only local inspection; then record image/header provenance and capacity before packaging.


## Additional Linux 4.4 source candidate — 2026-09-27

The user pointed to [geckyn/android_kernel_samsung_exynos7885](https://github.com/geckyn/android_kernel_samsung_exynos7885), branch `exelixis-2019-04-05_clang_lto`. At the inspected branch tip `ad10da74b6b2fcccdb2a2cfdb5d02aaa79b5a282` (2020-09-10), the top-level Makefile identifies Linux 4.4.200. The tree has `arch/arm64/configs/a10_00_defconfig`; it enables ARM64, initrd support, A10-labelled display/factory options, and selects `CONFIG_SOC_EXYNOS7885=y` plus `CONFIG_SOC_EXYNOS7884A=y`, while `CONFIG_SOC_EXYNOS7884` is unset. The Exynos DT directory contains generic `exynos7884-universal7884_*_Treble.dts` targets with model `Samsung Universal7884`; it has no A10 SWA/SM-A105F DTS in the inspected directory.

This is a useful additional downstream Linux 4.4 comparison and could inform source/config diffs. It is not exact SM-A105F board provenance and cannot currently replace the Eureka R24U candidate or the separate Samsung 4.4.111 mirror, whose DTS names A10 SWA OPEN 00 / EXYNOS7884B. The 4.4.200 repository is not modern 6.x, and no build or runtime result from it is available in this session. Do not combine its generic Universal7884 DTB with an A105F kernel package without matching stock-image evidence and board-specific validation.

The Codespace sign-in in this browser is currently stopped at Google's security-code challenge after two submitted codes were rejected. No Codespace terminal or filesystem is available here, so no kernel compilation/download into the Codespace was performed in this session. The supplied TeraBox share likewise did not yield file bytes: its Download action dispatched a `terabox://` app transfer that this browser blocks. Do not attempt a protocol workaround. Exact handset-build AP images remain required for boot packaging.


## 2026-09-27: measured user-supplied firmware boot layout

Candidate input: Android 11 firmware archive `A105FDDS9CWB3` supplied by the user. It is not verified as the handset's currently installed build. Parsed image metadata and hashes are persisted in [the machine-readable layout report](reports/a105f-cwb3.json).

| AP image | Measured layout | SHA-256 |
| --- | --- | --- |
| `boot.img` | 37,748,736 bytes; Android boot header v1; page 2048; kernel 29,112,000 bytes at 0x10008000; ramdisk 0; second loader 0; tags 0x10000100; Android 11, patch 2023-02 | `4dfa2224281458cd0ac3a0aa752681eb6445836fc0d58cea69225dfab113476e` |
| `dt.img` | 8,388,608 bytes; Android DT table v0, page 2048, one FDT at offset 64, 90,300 bytes; compatible `samsung,armv8` / `samsung,exynos7885` | `829b27e3b9235d6603701a25f21dd0240bd5cb43ddc8bbf3c383d30a353a475` |
| `dtbo.img` | 8,388,608 bytes; Android DT table v0, page 2048, one FDT at offset 64, 89,168 bytes; compatible `samsung,A10 SWA OPEN 00` / `samsung,EXYNOS7884B`; entry ID/revision 0/0, custom values [0,255,0,0] | `eb32301133ba5742afe0d782c83bd7b75ac040cbb115015a355d902702db737` |

The stock boot header declares an empty ramdisk. Bytes outside its described kernel/header sections include nonzero, vendor-specific data and a `SEANDROIDENFORCE` marker; the tail has not been classified as a whole. Do not pass that tail off as an initramfs. Debian boot therefore requires an explicit, nonempty Debian initramfs plus a selected kernel and a board-matched DTB/overlay. The firmware candidate provides useful DT/DTBO evidence, but does not identify which overlay the handset selects.

The boot image is exactly 36 MiB, matching the size in the downstream Eureka BoardConfig recipe. That coincidence is not independent proof of the installed boot partition capacity or of the complete partition map. Downstream Eureka offsets (base 0x10000000, kernel 0x8000, ramdisk 0x01000000, tags 0x100) remain candidate recipe values, not all observed stock header values. No flash or device action has occurred.

Stock kernel extracted from the declared kernel payload reports Linux 4.4.177-2184546, build #1 SMP PREEMPT, Wed Feb 22 02:47:35 KST 2023, GCC 4.9. This is distinct from the available Eureka source tree's 4.4.111 baseline. The existing 134-byte Eureka initramfs stub is empty and is not Debian boot media. The 6.18.54 modern source remains a generic Exynos7885 bring-up path without A10/A105F board DTS.


## 2026-09-27 — vendor source matched to candidate kernel version

The attached Samsung archive contains a 4.4.177 kernel tree and the exact `exynos7885-a10_defconfig`. Its source DTBO `exynos7884B-a10_swa_open_00.dts` identifies the SWA A10 overlay (`samsung,A10 SWA OPEN 00`, `samsung,EXYNOS7884B`), matching the candidate firmware's separately parsed `dtbo.img` compatible strings. The candidate firmware's `dt.img` is a separate 8 MiB partition image containing one Android DT-table v0 entry (2048-byte page, base compatible `samsung,armv8` / `samsung,exynos7885`); `dtbo.img` is also an 8 MiB partition image with one table entry for A10 SWA OPEN 00 / Exynos7884B. Both table payloads are about 90 KiB. These measurements are from the user-supplied candidate AP, not an untouched-phone dump.

**Correction:** the AP report's `boot.img` kernel size is **29,112,000 bytes** (not 2,911,200); its header is Android boot v1, page size 2048, kernel load address `0x10008000`, tags address `0x10000100`, and `ramdisk_size=0`, `second_size=0`. The 36 MiB boot file length is not verified partition capacity. The stock boot header therefore provides no stock initramfs bytes or observed Debian ramdisk load address. The exact source defconfig permits an external initrd (`CONFIG_BLK_DEV_INITRD=y`, empty `CONFIG_INITRAMFS_SOURCE`) and leaves `CONFIG_OF_OVERLAY` unset; overlay application belongs to the bootloader/DTBO flow unless deliberately changed and validated.

For a future Debian attempt, required provenance chain is: exact stock AP and boot header; reproducible Linux 4.4.177 A10 SWA build from the attached source using a documented compatible toolchain; generated kernel artifact hash and configuration; Debian initramfs hash/build recipe; base DTB and SWA DTBO bytes/table metadata tied to the same board; and an image builder that emits the measured Android boot-header v1/page-2048 form while documenting any new ramdisk address and cmdline. The stock `dt.img` and `dtbo.img` should remain separate candidates unless bootloader behavior proves otherwise. Validate the repacked image format, section offsets, size versus an independently verified partition size, and all hashes before any hardware decision. The current evidence does not establish active firmware, bootloader behavior, secure-boot acceptance, overlay selection, or permission to modify the phone.


## Host-only initramfs validation (2026-09-28)

The minimal Debian handoff initramfs uses a statically linked Debian Trixie ARM64 BusyBox and a gzip-compressed newc cpio archive. The init script creates /dev/console and /dev/null, mounts devtmpfs, proc, sysfs and temporary /run, resolves root=UUID= or root=PARTUUID=, waits for the selected block device, mounts it, checks /sbin/init, then moves virtual filesystems and calls switch_root. On failure it enters a console shell with diagnostics. Kernel config evidence includes CONFIG_BLK_DEV_INITRD=y and CONFIG_DEVTMPFS=y; CONFIG_DEVTMPFS_MOUNT is unset, so explicit devtmpfs mounting is used.

tests/test_a105f_initramfs.sh passes: host and ARM64 BusyBox shell syntax, static ARM64 ELF identity, gzip integrity, newc archive listing, expected init/tools/mountpoints. This is structural/emulation validation only, not a kernel boot or phone test. Generated archive SHA-256: e09e6dc2f9c1d325d7581a5e07c0eb075a1a1440433cff9296d864c490d9db0.

## Android boot-v1 packaging boundary

Supplied firmware evidence measures header v1, 2048-byte pages, kernel load address 0x10008000, tags address 0x10000100, and a 29,112,000-byte kernel; stock candidate boot.img has no ramdisk and reports ramdisk_addr=0. It does not establish an acceptable nonempty-ramdisk load address, boot partition capacity, Samsung footer/signature handling, AVB acceptance, or bootloader behavior. The file length (37,748,736 bytes) is not a partition-capacity measurement. Therefore the initramfs remains a host artifact and must not be packaged for flashing using generic load-address defaults. Base DTB and overlay remain separate Samsung table images: measured dt.img contains one 90,300-byte FDT and dtbo.img one 89,168-byte FDT, each table v0 with 2048-byte pages and separate 8 MiB candidate files.


## Host-only initramfs validation (2026-09-28)

The minimal Debian handoff initramfs uses a statically linked Debian Trixie ARM64 BusyBox and a gzip-compressed newc cpio archive. The init script creates /dev/console and /dev/null, mounts devtmpfs, proc, sysfs and temporary /run, resolves root=UUID= or root=PARTUUID=, waits for the selected block device, mounts it, checks /sbin/init, then moves virtual filesystems and calls switch_root. On failure it enters a console shell with diagnostics. Kernel config evidence includes CONFIG_BLK_DEV_INITRD=y and CONFIG_DEVTMPFS=y; CONFIG_DEVTMPFS_MOUNT is unset, so explicit devtmpfs mounting is used.

tests/test_a105f_initramfs.sh passes: host and ARM64 BusyBox shell syntax, static ARM64 ELF identity, gzip integrity, newc archive listing, expected init/tools/mountpoints. This is structural/emulation validation only, not a kernel boot or phone test. Generated archive SHA-256: e09e6dc2f9c1d325d7581a5e07c0eb075a1a1440433cff9296d864c490d9db0.

## Android boot-v1 packaging boundary

Supplied firmware evidence measures header v1, 2048-byte pages, kernel load address 0x10008000, tags address 0x10000100, and a 29,112,000-byte kernel; stock candidate boot.img has no ramdisk and reports ramdisk_addr=0. It does not establish an acceptable nonempty-ramdisk load address, boot partition capacity, Samsung footer/signature handling, AVB acceptance, or bootloader behavior. The file length (37,748,736 bytes) is not a partition-capacity measurement. Therefore the initramfs remains a host artifact and must not be packaged for flashing using generic load-address defaults. Base DTB and overlay remain separate Samsung table images: measured dt.img contains one 90,300-byte FDT and dtbo.img one 89,168-byte FDT, each table v0 with 2048-byte pages and separate 8 MiB candidate files.


### Independent review correction — 2026-09-28

Codex CLI read-only review identified and we fixed an early init ordering defect: virtual filesystem mount attempts had preceded creation of /dev/console, devtmpfs failure had been ignored, and console redirection came later. The init now mounts devtmpfs first, falls back to console/null nodes on failure, establishes the console before diagnostics, treats proc/sys/tmpfs mount failures as emergency-shell conditions, and only then resolves/mounts root and switch_roots. Required BusyBox mknod applet is confirmed in the Trixie static binary. The archive was rebuilt and host checks rerun. Superseding archive SHA-256: f4112366306b8b26c295a715350398e96a737b4e817425ffd73f010b565729e0.

The kernel build log's duplicate target warnings are in scripts/Makefile.fwinst for duplicate /lib/firmware/tsp_melfas/mss100_a30.fw and mss100_a30_old.fw install targets. Saved config has both CONFIG_TOUCHSCREEN_MELFAS_MSS100 and CONFIG_TOUCHSCREEN_MELFAS_MSS100_A30KOR unset. Warnings are firmware install-rule duplication, not compile or module link failures; no source change made.


## Debian ARM64 rootfs host validation (2026-09-28)

Read-only validation of the staged Debian 13.7 ARM64 minbase archive and extraction at `work/rootfs-verify.Gm1DH4` found 117 package records, all reporting the `ii` (installed/configured) status when queried as root. `dpkg --audit --root=work/rootfs-verify.Gm1DH4` emitted no audit findings. The archive SHA-256 is `a69837bfddfed1e15c84ee480097506033709e4f945c635acb835042f7838cab`.

The ARM64 systemd executable was identified as an AArch64 ELF using the rootfs dynamic loader, and `qemu-aarch64-static -L work/rootfs-verify.Gm1DH4 .../usr/lib/systemd/systemd --version` executed successfully, reporting systemd 257 (257.13-1~deb13u1). This validates userspace executable/loader compatibility under QEMU user emulation only; it does not boot the rootfs or validate Samsung hardware.

Presence checks found `/etc/fstab`, `/etc/hostname`, `/etc/resolv.conf`, systemd, the SSH service unit and a tty1 getty enablement link. The extraction lacks `/etc/hosts`; the fstab and network configuration still need review/population for the eventual target. SSH policy, actual network interfaces, root-device discovery and full system boot remain unvalidated. The rootfs has no confirmed device-specific root UUID yet.

## Host-only Samsung boot-v1 candidate validation (2026-09-28)

The generated kernel outputs were wrapped into host-validation artifacts under the ignored work tree at work/boot-candidates/host-only-a105f/. This did not involve a device. The packager is the official AOSP repository https://android.googlesource.com/platform/system/tools/mkbootimg at commit fc7b8eb91329b7636a5673b436e4a83510a583d6 (snapshot for 6396176, branch rvc-d1-release).

The boot image was created with explicit Android boot header v1 and 2048-byte pages. Measured supplied boot-header values were kernel address 0x10008000 and tags address 0x10000100. The candidate recipe used base 0x10000000 and kernel offset 0x8000 to reproduce the measured kernel address; base and ramdisk offset 0x01000000 come from the previously identified A105F community BoardConfig candidate, not the supplied stock header. The resulting candidate ramdisk address is 0x11000000. The command line is empty because no verified root UUID/PARTUUID, console target, or handset command line is available. No DTB is embedded in boot.img; the measured Samsung layout keeps dt.img and dtbo.img separate.

The resulting boot.img is 30,132,224 bytes; the inspector reports header v1, page size 2048, kernel size 29,112,000 at 0x10008000, ramdisk size 1,017,184, ramdisk address 0x11000000, tags address 0x10000100, and no second-stage/recovery-DTBO payload. SHA-256: fd7092cc4177e3a075b0d6493dfbc7a723c8a0686f399bef467ffc3aac902f3.

The raw kernel DTB is version 17, 90,300 bytes, and its FDT compatible list is samsung,armv8 and samsung,exynos7885. The raw SWA overlay DTBO is version 17, 89,168 bytes, compatible samsung,A10 SWA OPEN 00 and samsung,EXYNOS7884B. Both were wrapped without modifying their FDT payloads into Android DT table v0 images using scripts/build_android_dt_table.py, with 2048-byte page alignment. The host-only candidate DT table entry id/revision/custom tuple is all zero because the supplied evidence does not disclose the stock selector tuple; this is not asserted to match handset selection behavior. Generated dt.img is 94,208 bytes (SHA-256 15c28d3b14250f0c75be58523ca7c0c5164bc422fa6e3ad6d9b970c45bca5fca); dtbo.img is 92,160 bytes (SHA-256 93a16c9040e2b8ce62ccb0b57fd23ed1febd0e4a7f36c82b333a20d63a009164). Both images pass scripts/inspect_android_boot_layout.py structural parsing.

The host-only archive’s initramfs SHA-256 is f4112366306b8b26c295a715350398e96a737b4e817425ffd73f010b565729e0. A clean nested-output build also succeeded after fixing builder staging and relative-output handling; that independent output hashed 6d71067ba5f02b74044380675f0ff9f087c6a4b9d5b4e227368c8bd568994ebf. The full test suite passes 19 tests, and tests/test_a105f_initramfs.sh validates the archive’s ARM64 static BusyBox, shell syntax, gzip integrity, and newc listing.

These are structural host artifacts only. They are not ready for flashing: the stock AP’s exact installed state is unknown; the DT table selector tuple is unverified; no root command line is set; partition capacity, Samsung footer/signature format, AVB/bootloader acceptance, and overlay application behavior remain unverified. The 8 MiB stock candidate dt.img/dtbo.img file lengths do not prove partition capacities. The phone remains untouched.

Verified generated Samsung Image size and digest: 29,112,000 bytes; SHA-256 f68c9992e7fa2c663d3b0c1664d6c786f2ca5bde4a9e90775c95f5f97451e. The candidate boot header parses the same 29,112,000-byte kernel payload size. This matches the supplied AP measurement by length only and does not establish that the generated kernel is byte-identical to stock or accepted by the handset.
