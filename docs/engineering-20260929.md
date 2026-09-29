# Engineering checkpoint — 2026-09-29

## Verified repository and new host tooling

The verified starting point was private `main` at `c6f15a3c562714a229b238c88eebba5e5977b60e`. This session added `scripts/extract_android_boot_sections.py` and `tests/test_extract_android_boot_sections.py` to make the next boot-v1 package check repeatable. The extractor validates Android boot header v1, page size, section offsets, payload bounds and alignment; extracts kernel and ramdisk bytes; records sizes, load addresses and SHA-256 values in JSON; and can compare extracted payload hashes against supplied source files.

The tests cover valid aligned extraction, truncation, unsupported header versions, CLI output, byte-for-byte source comparison and manifest hashes. The CLI also checks expected page size, kernel, ramdisk and tags addresses; address mismatches fail validation. It recomputes the Android header v1 SHA-1 ID over each kernel, ramdisk, second and recovery-DTBO payload followed by its little-endian size, and rejects a mismatch (algorithm cross-checked against AOSP `mkbootimg.py`). The complete tracked Python suite passed **25/25** when reconstructed from the verified GitHub tree at this revision. `py_compile` passed for the project Python scripts/tests; `bash -n` passed for the initramfs and rootfs builders. This run did not have the Codespace build filesystem or the private release archive bytes, so no kernel, DTB, DTBO, initramfs or boot image was rebuilt here.

## Candidate artifact state

GitHub release metadata confirms the private draft release `a105f-host-only-candidate-20260928` exists with one asset, `SM-A105F-host-only-boot-candidate-20260928.tar.gz`, size 12,118,381 bytes. GitHub reports asset digest `sha256:f28d6a293695ae6075123a4ed9af0a9c5f19b0f7fe6c125c98a71e87cfd98ae5`.

That release digest differs from the older handoff's recorded bundle digest. Treat the current GitHub digest as the remote asset metadata, but do not infer the archive contents from it: this session could not download the private binary asset or inspect its inner manifest. The candidate has therefore **not** been regenerated with the corrected initramfs, and stale artifact evidence has not been superseded. Use the new extractor at the next authorized Codespace session to verify payloads against the actual source `Image` and current `a105f-debian-initramfs.cpio.gz` before creating a replacement bundle.

## Linux 6.18.54 board-port evidence advanced

Current upstream Linux snapshot inspected: `torvalds/linux` commit `bf1aee1ad1c087ffda617207890dc92042a28c96`, including `arch/arm64/boot/dts/exynos/exynos7885.dtsi` and the sibling A8 `exynos7885-jackpotlte.dts`. The SoC DTS exposes `mmc_0` (Exynos7885 DW-MSHC SMU) and `serial_2`; the sibling A8 board enables an 8-bit non-removable eMMC with HS200/HS400 and uses the same serial label. This supports the modern base-node mapping but is sibling-board evidence, not an A10 DTS recipe.

For a target-specific comparison, the public `neronewman/A10-A105F-kernel` mirror at `ad623e4df6718c2c371eee6d5fa8c4e1108b75bc` was inspected. Its A10 common tree enables Samsung downstream `dwmmc_0` as non-removable 8-bit eMMC with HS200/HS400 options, `dwmmc_2` as a 4-bit removable SD host, `serial_2`, GPIO keys on GPA1 pins 5/6/7, and a downstream UDC/DWC3 OTG high-speed configuration. Its A10 SWA overlay identifies `samsung,A10 SWA OPEN 00` and `samsung,EXYNOS7884B`. The mirror identifies Linux 4.4.111 and is not the supplied 4.4.177 source; it is comparison evidence only. The old Samsung properties must be mapped to current bindings and drivers before porting. The inspected upstream Exynos7885 SoC DTS has no USB/DWC3 node, so USB gadget enablement needs separate SoC/PHY/topology work rather than copying the downstream fragment.

No Linux 6 DTS patch or DTB build was made: this runtime lacks the staged 6.18.54 tree and the Codespace browser currently presents a GitHub login page. No account recovery or human-only verification was attempted.

## Boot and recovery constraints

The measured candidate stock boot image remains Android header v1, page size 2048, kernel load address `0x10008000`, tags address `0x10000100`, and no stock ramdisk. The previous source-built kernel size matches the measured candidate kernel payload length, but that is not proof of byte identity or bootloader acceptance. Android's public boot-header specification describes v1 section metadata; it does not establish Samsung footer/signature checks, AVB applicability, or this handset's acceptance behavior.

The community A105F build recipe's 36 MiB boot size and separate DTB/DTBO partition declarations remain configuration evidence only. The observed 8 MiB candidate firmware DT/DTBO files are image lengths, not proof of partition capacities. Active overlay selector, installed firmware, physical partition map, rollback behavior and exact stock restore procedure are still unresolved. No device-side operation has been performed.

## Phone

The physical SM-A105F remains untouched. No boot, flash, recovery, Download Mode, partition read, or other device action occurred.

## Next exact engineering work

1. Reconnect the existing Codespace after its required GitHub browser authentication is available. Preserve its ignored `work/` artifacts and inspect status before changing anything.
2. Rebuild the host boot-v1 candidate from the corrected initramfs. Run the new extractor with `--expected-kernel` and `--expected-ramdisk`, independently parse the output, and record current boot/DT/DTBO hashes and sizes. Update the private draft asset only after these checks and verify the release readback.
3. In the Linux 6.18.54 source tree, derive an A10 DTS from the exact supplied 4.4.177 board/base DTS and compare each node with upstream `exynos7885.dtsi` bindings. Start with memory/reserved memory, eMMC and UART; keep storage timings conservative until validated. Build the actual DTB and run schema checks before recording a patch.
4. Continue locating evidence for battery/charger/thermal and modem/USB dependencies. Do not claim boot safety without runtime/device evidence.

## Additional hardware compatibility audit

The pinned Samsung-derived 4.4.111 SoC DTS gives a useful exact-address comparison. Its embedded host `dwmmc_0` is at `0x13500000`, IRQ 146, and its A10 board overlay enables it as an 8-bit non-removable eMMC. Upstream Linux has `mmc_0` at the same address/IRQ with Exynos7885 embedded-MMC bus clocks. This gives a strong mapping for the initial Debian root-storage path, while the A10 tuning should remain conservative until matched against the exact 4.4.177 tree. The vendor removable SD host `dwmmc_2` is at `0x13550000`, IRQ 147 and uses card clocks; upstream defines the relevant card clock IDs but has no controller node or A10 `sd2_*` pin groups. SD support therefore needs new SoC pinctrl/controller DTS work.

Safety-critical gaps surfaced in the same comparison. The vendor 4.4.111 SoC DTS has three `samsung,exynos7885-tmu` nodes, but upstream's Exynos thermal binding and `exynos_tmu` match table do not list that compatible (they list families through Exynos7/5433). The upstream Exynos7885 DTS has no TMU nodes. Do not label these as upstream-supported or substitute `samsung,exynos7-tmu` without register/trim semantics and calibration proof. A10 common DT includes a Samsung AP thermistor table through the ADC, plus a `samsung,s2mpu08mfd` device. Upstream SEC MFD code supports S2MPU02/05 and S2MPS parts but has no S2MPU08 match; Samsung's sec-battery/charger policy is also downstream-specific. Battery, charging, PMIC and thermal behavior remain first-boot/sustained-use blockers until measured and implemented safely.

The same downstream SoC DTS carries Samsung-specific DWC3/USB-PHY nodes, but the upstream Exynos7885 SoC DTS has no USB node. It also has Samsung-specific RTC, watchdog, display and audio devices. Treat the downstream UDC OTG/high-speed declarations only as evidence that a USB path exists in Samsung's kernel; they do not provide a mainline-compatible first-boot USB-network path. Prioritize console plus eMMC first, then build a safe upstream USB/PHY path and verify it separately. No guessed eMMC partition/PARTUUID was introduced.

## Partition and verification evidence conflict

A second pinned A105F recovery build tree, `twrpdtgen/android_device_samsung_a10` commit `af1681558e88d88a625115334724dca8acfbdd80`, identifies `SM-A105F` and an Android 11 `A105FDDS9CWD2` fingerprint. Its `BoardConfig.mk` specifies boot header v1/page 2048, separate DTBO, `BOARD_BOOTIMAGE_PARTITION_SIZE := 55574528` (53 MiB), AVB build enabled, a test recovery signing key and rollback index 1; it also contains a future patch-date override labelled as an anti-rollback hack. The older Eureka config records 37,748,736 bytes (36 MiB) for boot. This 17 MiB disagreement proves these build files are not reliable measurements of the handset partition size. The TWRP `recovery.fstab` lists `boot`, `recovery`, `dtb`, `dtbo`, `vbmeta_samsung`, and other by-name partitions; these are partition-name claims from that build tree, not a validated partition table for the target handset. Its AVB/test-key settings prove only how that recovery tree was configured, not Samsung's acceptance policy for the A10 or a Debian boot image.

No reliable model-specific evidence was found in this pass that closes the physical Download Mode entry/exit, OEM unlock state, downgrade/rollback, Odin/Heimdall restore, or emergency recovery procedure for this handset's installed firmware. Those remain open; do not use community build settings as a substitute for a tested rollback plan.

## A10 boot-chain and rollback evidence

The official TWRP A10 device page (accessed 2026-09-29) identifies the target family as A-only/system-as-root and explicitly says stock devices use AVB through a `vbmeta` partition to verify `boot.img`, `recovery.img` and other images. It warns that installing TWRP without a corresponding verity-disabled `vbmeta` image can leave the device unable to boot. The same page describes TWRP and Magisk-rooted Android using the recovery kernel, with hardware keys selecting the mode. This is a model-targeted warning from the maintained community recovery project, not proof of this handset's current firmware state or exact bootloader policy. It makes the previously generated `boot.img` candidate's intended target partition a question that must be closed from matching stock boot/recovery metadata and the actual installed AP before any device action.

Samsung's Knox technical note describes signature validation along the boot chain and rollback prevention for bootloader/kernel versions, with minimum version values protected in hardware/bootloader state. It is platform-level guidance, not proof of the target's fuse state or that this custom Debian image can or cannot boot after an authorized unlock. Keep the installed binary revision, OEM unlock/security state, AVB/vbmeta behavior, Download Mode entry/exit and a tested stock restore path as pre-flash gates.

Sources:
- TeamWin A10 device page, updated 2026-09-28: https://twrp.me/samsung/samsunggalaxya10.html
- Samsung Knox boot-time protections technical note: https://kp-cdn.samsungknox.com/b9821c47b3ef1cce894325a61a6fcdac.pdf
- AOSP boot header and DTBO format references: https://source.android.com/docs/core/architecture/bootloader/boot-image-header and https://source.android.com/docs/core/architecture/dto/partitions
- AOSP mkbootimg header-ID algorithm source, commit 808d42e197506319ee65eb078d3defd9602e2ac2: https://android.googlesource.com/platform/system/tools/mkbootimg/+/808d42e197506319ee65eb078d3defd9602e2ac2/mkbootimg.py


## Debian Trixie systemd versus Samsung 4.4.177

The Debian rootfs records systemd 257.13. The upstream v257 README lists Linux 3.15 as its hard baseline but recommends 5.4 or newer; versions below 5.4 have significant feature gaps and taint the manager as `old-kernel`. Thus Linux 4.4.177 is not categorically below systemd's hard minimum, but it is well below the recommended baseline and is not an equivalent long-term security/support choice to the Linux 6.x track.

For v257, upstream lists `CONFIG_DEVTMPFS`, `CONFIG_CGROUPS`, `CONFIG_INOTIFY_USER`, `CONFIG_SIGNALFD`, `CONFIG_TIMERFD`, `CONFIG_EPOLL`, `CONFIG_UNIX`, `CONFIG_SYSFS`, `CONFIG_PROC_FS`, and `CONFIG_FHANDLE` as kernel config requirements; `CONFIG_NET_NS` and `CONFIG_USER_NS` are needed by common `PrivateNetwork=` and `PrivateUsers=` service settings. Optional but recommended items include IPv6, tmpfs/ext4 ACL and xattr support, seccomp/filter and kcmp. The exact successful Samsung 4.4.177 generated config is not present in this Work filesystem, so no option is asserted present/absent here. Run a config audit against the exact generated config and systemd's own requirements after restoring the Codespace; then host-test representative Debian service units under QEMU. Avoid enabling security-sensitive kernel features blindly.

Source: upstream systemd v257 README, versioned source: https://github.com/systemd/systemd/blob/v257/README

## Reusable systemd kernel config auditor

Added executable `scripts/audit_systemd_kernel_config.py` and six focused tests. It parses standard Linux `.config` enabled/unset records and audits them against upstream systemd v257's published config requirements: core required options, options expected disabled, service sandbox namespace gaps, recommended options, and a nonempty legacy hotplug helper. It exits nonzero for missing core requirements or incorrectly enabled required-off options, while reporting feature/recommended gaps separately. The audit logic is grounded in the versioned upstream `systemd v257 README` referenced above.

The project Python suite now passes **29/29**, and `py_compile` passes for tracked scripts/tests. This session did not have the exact generated Samsung 4.4.177 `.config`, so the tool was tested using fixtures only; no conclusion about the actual kernel config has been made.

## Component match audit against Linux 6.18.54

Exact stable source inspected: `gregkh/linux` branch `linux-6.18.y` at `1b357ecb321392158d507b04672ffee57bfa071d`, whose commit message is `Linux 6.18.54` (2026-09-25).

- eMMC has an upstreamable path: Exynos7885's SoC `mmc_0` node includes the `samsung,exynos7-dw-mshc-smu` fallback matched by `drivers/mmc/host/dw_mmc-exynos.c`. The 4.4.111 A10 mirror's `dwmmc_0` is the same 0x13500000 / IRQ 146 block. Keep tuning and regulators from the 4.4.177 source under review.
- The downstream A10 SD host `dwmmc_2` (0x13550000 / IRQ 147) has no current Exynos7885 SoC node/pinctrl group. The driver supports related Exynos DW-MSHC variants, but address, clocks, SD2 pins, detect and voltage handling need explicit porting.
- USB is not a simple DT enable: `dwc3-exynos.c` and `phy-exynos5-usbdrd.c` in v6.18.54 have no Exynos7885 compatible match, while the downstream A10 DTS uses Samsung `exynos-dwusb` and `exynos-usbdrd-phy` plus vendor PHY properties. New glue/PHY match data or a validated equivalent is required before USB gadget/USB networking can be claimed.
- The Samsung `scsc_wifibt` mailbox/device node has no match in the inspected mainline wireless/Bluetooth drivers. The A10 tree depends on SCSC vendor WLAN/BT support and firmware; Wi-Fi/BT is not available by merely enabling an upstream generic interface.
- Mainline ST accelerometer driver tables match `st,lis2ds12`; the A10 vendor DT uses `st,lis2ds`. Verify the actual sensor ID/binding before reusing the driver or changing the compatible. A10's `sec,sec_ts`, `sharp,gp2ap110s`, `codec,cod3035x`, and `siliconmitus,sma1301` likewise have no matching compatible in the inspected 6.18.54 tree. Mainline has SMA1303/1307 codec drivers, which are not proof of SMA1301 compatibility.
- The Samsung modem board data declares `sec_modem,modem_pdata` and SIPC 5.0; no mainline compatible/driver path was found for this Exynos/S327AP integration. Treat cellular data and modem control as downstream-only pending a distinct modem protocol/driver port.
- The gaps above are host source match findings, not proof that the physical devices are absent. No unsafe DT node has been copied or enabled.

Pinned source paths:
- https://github.com/gregkh/linux/blob/1b357ecb321392158d507b04672ffee57bfa071d/drivers/mmc/host/dw_mmc-exynos.c
- https://github.com/gregkh/linux/blob/1b357ecb321392158d507b04672ffee57bfa071d/drivers/usb/dwc3/dwc3-exynos.c
- https://github.com/gregkh/linux/blob/1b357ecb321392158d507b04672ffee57bfa071d/drivers/phy/samsung/phy-exynos5-usbdrd.c
- https://github.com/gregkh/linux/blob/1b357ecb321392158d507b04672ffee57bfa071d/drivers/iio/accel/st_accel_i2c.c
