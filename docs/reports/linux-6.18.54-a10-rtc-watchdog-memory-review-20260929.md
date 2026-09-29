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
| ABOX memory | The A10 common overlay includes `exynos7884-rmem_7884.dtsi`. It adds `compatible = "exynos,abox_rmem"` at 0xE9400000, size 0x400000, under the downstream `&reserved_memory` node. Samsung's separate Exynos7885 DTS has an `abox_debug` consumer referencing `&abox_rmem`; the A10 source evidence examined here does not establish that same active consumer. | The generic reserved-memory mechanism can describe fixed ranges, but the Samsung compatible has no upstream consumer in this A10 port. The vendor child has neither `no-map` nor `reusable`; adding either would change semantics. Its interval falls inside the A10 second populated bank (0xC0000000–0x100000000). | Do not copy the vendor compatible or infer `no-map`, reusable/DMA-pool, or firmware ownership. Keep the 4 MiB region out of the Linux board DTS until evidence shows the A10 boot path requires a reservation or a supported consumer. Track it as a DTBO/Android memory-layout item. |
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
