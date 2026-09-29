# Engineering checkpoint — 2026-09-29

## Verified repository and new host tooling

The verified starting point was private `main` at `c6f15a3c562714a229b238c88eebba5e5977b60e`. This session added `scripts/extract_android_boot_sections.py` and `tests/test_extract_android_boot_sections.py` to make the next boot-v1 package check repeatable. The extractor validates Android boot header v1, page size, section offsets, payload bounds and alignment; extracts kernel and ramdisk bytes; records sizes, load addresses and SHA-256 values in JSON; and can compare extracted payload hashes against supplied source files.

The tests cover valid aligned extraction, truncation, unsupported header versions, CLI output, byte-for-byte source comparison and manifest hashes. The CLI also checks expected page size, kernel, ramdisk and tags addresses; address mismatches fail validation. The complete tracked Python suite passed **24/24** when reconstructed from the verified GitHub tree at this revision. `py_compile` passed for the project Python scripts/tests; `bash -n` passed for the initramfs and rootfs builders. This run did not have the Codespace build filesystem or the private release archive bytes, so no kernel, DTB, DTBO, initramfs or boot image was rebuilt here.

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
