# A10 RTC, watchdog, and reserved-memory review — 2026-09-29

## Source identity

The A10-specific reference is the user-supplied Samsung SM-A105F SWA source archive (SHA-256 `5c83be7c2452d644ccda1deb898d9a54f2b3d53d3a0e66a7a394dcbf14439931`). The exact source files examined are:

- `vendor/arch/arm64/boot/dts/exynos/dtbo/exynos7885.dts`
- `vendor/arch/arm64/boot/dts/exynos/dtbo/exynos7884B-a10_common.dtsi`
- `vendor/arch/arm64/boot/dts/exynos/dtbo/exynos7884-rmem_7884.dtsi`

The last file SHA-256 is `043800953207d58aa7005841fe7b774cb58e678dfc763e35396a4a8b3b09afc6`. Comparisons use upstream Linux `gregkh/linux` tag `v6.18.54`, commit `1b357ecb321392158d507b04672ffee57bfa071d`.

## Findings and decisions

| Area | Exact Samsung A10/SoC evidence | Linux 6.18 comparison | Decision |
| --- | --- | --- | --- |
| ABOX memory | The A10 common overlay includes `exynos7884-rmem_7884.dtsi`. It adds `compatible = "exynos,abox_rmem"` at 0xE9400000, size 0x400000, under the downstream `&reserved_memory` node. Samsung's separate Exynos7885 DTS has an `abox_debug` consumer referencing `&abox_rmem`; the later exact-source cross-check confirms that the A10 common overlay enables ABOX and includes this fixed region; see the clarification below. | The generic reserved-memory mechanism can describe fixed ranges, but the Samsung compatible has no upstream consumer in this A10 port. The vendor child has neither `no-map` nor `reusable`; adding either would change semantics. Its interval falls inside the A10 second populated bank (0xC0000000–0x100000000). | Do not copy the vendor compatible or infer `no-map`, reusable/DMA-pool, or firmware ownership. Keep the 4 MiB region out of the Linux board DTS until evidence shows the A10 boot path requires a reservation or a supported consumer. Track it as a DTBO/Android memory-layout item. |
| RTC | Samsung SoC DTS uses `compatible = "samsung,exynos8-rtc"`, `reg = <0x0 0x11C90000 0x100>`, and interrupts 27, 28, 36. It supplies no clocks in this node. | The current upstream Exynos7885 SoC DTSI has no RTC node. The available Exynos850 RTC node is at a different address, has two interrupts, uses an Exynos850 compatible, and names a CMU clock. That sibling node does not establish the Exynos7885 RTC clock or register behavior. | Keep RTC disabled. Do not copy the Exynos850 node or bind the A10 block to a generic S3C compatible without matching driver evidence. The Samsung S2MPU08 RTC child is independently blocked on its absent upstream MFD. |
| Watchdog | Samsung SoC DTS uses `samsung,exynos8-wdt` at 0x10060000, SPI 233, timeout 30 seconds, PMU syscon, and clock names `rate_watchdog` / `gate_watchdog` sourced from OSCCLK and GATE_WDT_CLUSTER1. | Upstream Exynos7885 DTSI has no watchdog node. Exynos850 has two cluster watchdog nodes and a different compatible, interrupt assignment, and clock tree. | Keep watchdog disabled until the 7885 register layout, gate/rate clock mapping, cluster/reset behavior, and 6.18 driver compatible are verified. Do not copy the Exynos850 sibling node. |

## Artifact and implementation state

The latest verified board patch remains the SD2 + conservative eMMC/UART2 work already in the prior checkpoint. This review adds no DTS changes: the memory, RTC, and watchdog mappings above do not yet meet the evidence bar for a safe Linux 6.18 conversion.

GitHub Actions reports zero workflow runs for the private repository, so no existing workflow artifact can supply the exact Samsung-built kernel or corrected initramfs. The existing release metadata contains a host-only boot candidate but does not contain the missing exact Samsung Image/initramfs/DTB/DTBO set. The active Colab inventory previously found no exact vendor Image, corrected cpio, boot DTB, or DTBO. Do not rebuild or substitute those known-good/missing artifacts.

The committed initramfs script accepts UUID/PARTUUID but only checks `/dev/disk/by-uuid` and `/dev/disk/by-partuuid`; the builder installs no udev, mdev, or other component that creates those symlinks. This is a confirmed source defect, separate from artifact availability. Next root-handoff change should either add and test a real identifier resolver or use an explicitly supplied measured `/dev/mmcblk0pN` device path; do not guess the partition or choose the first block device.

No full-tree `dtbs_check` was run during this review. No A10 DTB was changed or rebuilt, no binaries were recovered, and no device operation occurred. The phone remains untouched.


## Root-device handoff source fix — 2026-09-29

The initramfs previously looked up UUID/PARTUUID only through `/dev/disk/by-*` symlinks, while the builder installed no utility to create those links. The selector is now a separate POSIX shell library included in the cpio image. It also accepts only an explicit `/dev/mmcblk0pN` path (matching the A10 `mmc0 = &mmc_0` alias) so a future measured eMMC partition can be supplied through the boot command line without inventing UUID/PARTUUID data. It never enumerates devices or chooses the first match. UUID/PARTUUID still require an existing symlink; resolver creation and BusyBox compatibility remain to be validated against the recovered exact static BusyBox.

Focused verification in the active workspace passed 2 Python unittest cases, covering accepted/rejected root specs and shell syntax. Bash syntax checks passed for the builder and test script. The archive build/extract test and full repo suite were not run because the exact BusyBox/initramfs artifacts and full repository checkout are unavailable here.


## ABOX reservation clarification from exact A10 overlay — 2026-09-29

A re-read of the verified source resolves the earlier uncertainty in the table above. The exact user-supplied 4.4.177 source hashes remain those recorded in `docs/SOURCES.md` and this report:

- `exynos7884B-a10_common.dtsi` includes `exynos7884-rmem_7884.dtsi`, which defines `abox_rmem` at 0xE9400000 with size 0x400000.
- The same A10 common overlay sets `&abox` to `status = "okay"` and its sound-card nodes reference the ABOX block.
- The inherited Exynos7885 source DTS defines `abox_debug` with `memory-region = <&abox_rmem>`; the A10 overlay supplies the corresponding fixed region through the included 7884 rmem file.
- Neither region description declares `no-map` or `reusable`.

This supports the existing Linux 6.18 patch's generic, non-reusable fixed `reserved-memory` entry for 0xE9400000–0xE9800000. It prevents ordinary Linux allocations from overlapping memory assigned by the A10 description while avoiding unsupported Samsung ABOX compatibles or fabricated no-map/reusable semantics. It does **not** provide an upstream ABOX/audio driver or make audio operational; those remain unported. The earlier suggestion to leave this fixed range out is superseded by this exact overlay evidence. No change to patch 0004's range or semantics is warranted.


## Linux 6.18.54 RTC probe and binding cross-check — 2026-09-30

The pinned upstream files at commit `1b357ecb321392158d507b04672ffee57bfa071d` narrow the port gap:

- `Documentation/devicetree/bindings/rtc/s3c-rtc.yaml` lists S3C6410, Exynos7/Exynos850 plus S3C6410 fallback, and deprecated Exynos3250 compatibles. It constrains RTC interrupts to exactly two entries. Clocks are permitted but not required by the schema, with names `rtc` and `rtc_src`.
- `drivers/rtc/rtc-s3c.c` does not match Exynos8, unconditionally acquires/enables the `rtc` clock during probe, and requests only interrupt index 0 as the alarm IRQ. It does not request the additional tick IRQs described by the exact A10 DTS.
- `drivers/clk/samsung/clk-exynos7885.c` has no RTC gate/clock output. The Exynos7885 provider's WDT1 PCLK is not an RTC clock and cannot fill this gap; the Exynos850 RTC clock description is not transferable evidence.

The already hash-verified Samsung source report establishes the A10 node has three IRQs, no clock properties, and an Exynos8 variant with `clock_ctrl_disable`. Thus adding only the compatible would still fail at runtime in the 6.18 driver, despite being schema-permitted without clocks. A 6.18 port must add an explicit clockless Exynos8 variant path (including no-op clock enable/disable and cleanup handling) and decide whether exposing the third IRQ is required. The mainline driver presently supplies alarm handling only; the source report does not yet document whether losing Samsung's periodic tick IRQ functionality is acceptable. No RTC binding, driver, or DTS change is claimed.

The public `topser9/kernel_samsung_universal7885` 4.4.177 mirror at `ae3bd5aef8fd81bff8c8807fa9a16ef47970b9c3` shows its RTC driver consumes IRQ indices 0/1/2 as alarm/tick0/tick1 and applies the same clock-control-disabled Exynos8 data. This is secondary comparison evidence, not a substitute for the hash-verified A10 archive. Before implementation, confirm the exact Samsung 4.4.177 IRQ request/tick behavior from the existing recovered source in a working build environment, then decide whether upstream should preserve the extra periodic IRQs or document their omission. The handset remains untouched.
