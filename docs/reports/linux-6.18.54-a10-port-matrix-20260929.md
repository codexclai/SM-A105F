# A10 Linux 6.18 subsystem port matrix — 2026-09-29

## Scope and source identity

This matrix compares the acquired Samsung SM-A105F SWA source archive and its A10 overlay with Linux 6.18.54 at `gregkh/linux` tag `v6.18.54` (base DT nodes/bindings/drivers). The Samsung ZIP SHA-256 is `5c83be7c2452d644ccda1deb898d9a54f2b3d53d3a0e66a7a394dcbf14439931`; embedded `Kernel.tar.gz` SHA-256 is `e05288db460f2d0a0f86c79beac819066f4ea3baa57cf5f26b46cdf4ec3d0af2`. This is exact user-supplied source provenance, not an independently signed Samsung release. Source paths and hashes are recorded in `docs/SOURCES.md` and `docs/ARTIFACTS.md`.

This is a source/binding crosswalk. It does not establish hardware operation or bootability. No physical-device operation occurred.

## Porting matrix

| Subsystem | Exact A10 4.4 evidence | Linux 6.18 mapping | Decision |
| --- | --- | --- | --- |
| SD2 | `dwmmc_2`, 0x13550000, SPI 147; SD2 clock/cmd/data pins; GPA0-7 external active-low detect | Existing A10 patch adds Exynos7 DW-MSHC node; upstream generic GPIO, pinctrl, and Samsung MMC binding | Already implemented and focused-validated in prior milestone. Do not redo. |
| eMMC | `dwmmc_0`, 0x13500000/SPI 146, clocks MMC_EMBD; 8-bit, non-removable; base SDR `<3 0 4 0>`, DDR `<3 0 4 2>`, HS200 `<3 0 3 0>`, HS400 `<1 0 2 0>`; HS400 delay `0x60`; several Samsung-only tuning/QoS/CMDQ settings | Existing upstream `mmc_0` is `samsung,exynos7885-dw-mshc-smu` with matching address/IRQ/clocks. Linux 6.18 binding requires two-cell SDR and DDR arrays plus CIU divider. Driver reads two cells and builds CLKSEL using sample, drive, divider. | Patch 0002 now enables only 8-bit, non-removable, conservative MMC high-speed operation with the existing SD0 pin groups and legacy base SDR/DDR CLKSEL field values in Linux's timing arrays. Samsung 4.4 `(div, fine_drive, drive, sample)` values map to Linux's `(sample, drive)` array plus separate divider at the register-field level. This does not establish equivalent electrical phase semantics. HS200/HS400 and UHS voltage switching, downstream CMDQ/QoS/fine-drive/delay-line fields remain disabled/unmapped because PMIC rails and per-mode tuning semantics are unresolved. Targeted MMC binding, A10 DTB schema build, and direct validation passed. |
| UART2 | `serial_2` at 0x13820000, SPI 279; A10 common overlay enables it and uses UART2 bus pins | Existing upstream `serial_2` Exynos7885 UART node and pinctrl group | Patch 0002 enables the existing node, sets `serial2` and `/chosen/stdout-path = &serial_2`, matching the sibling board's upstream alias/console pattern. The UART binding, targeted A10 schema build, and direct validation passed. No runtime console output is verified. |
| Pinctrl/GPIO | Exact A10 overlay assigns volume-down GPA1-6, volume-up GPA1-5, power GPA1-7; all EINT, no pull; GPIO specifier flags `<0xf>`; power key is wake-enabled. | Upstream Exynos7885 pinctrl/GPIO plus generic `gpio-keys`; Linux key driver can derive IRQ from a GPIO descriptor with `gpiod_to_irq()`. | Patch 0003 maps the three keys with standard `GPIO_ACTIVE_LOW`, EINT and `EXYNOS_PIN_PULL_NONE`; power uses `wakeup-source`. Legacy direct three-cell `interrupts` tuples and nonstandard flag bits are omitted after tracing. Focused A10 DTB/schema validation passed; see the GPIO key review. No runtime input or wake test. |
| RAM/reserved memory | Exact Samsung base/A10 DTSIs declare two populated banks, a 13 MiB memreserve, nine fixed ranges, and separate dynamic vendor pools | Generic `memory`, `/memreserve/`, and fixed `reserved-memory` `reg` entries | Patch 0004 carries the two bank-matched physical ranges, the exact memreserve, and nine fixed reservations. No vendor consumer, ION/security semantics, `no-map`, or reusable behavior is inferred; dynamic pools remain omitted. Focused reservation binding/build checks pass; whole-DTB output still has root-compatible and osc-clock diagnostics. See the memory review. |
| PMIC/regulators | A10 overlay uses `samsung,s2mpu08mfd`, Samsung ACPM fields, a GPA2 IRQ and named rails including `vqmmc`/`vmmc` | No matching upstream S2MPU08 MFD/regulator driver found in the pinned 6.18 source; generic regulator bindings alone cannot replace driver/transport semantics | Blocked. Do not alias another S2MPSxx PMIC or replace rails with dummy fixed regulators. This also gates eMMC high-speed modes, SD UHS, USB PHY and other loads. |
| RTC | Exact SoC node is `samsung,exynos8-rtc` at 0x11c90000 with three IRQs and no clock; Samsung 4.4 driver maps it to dedicated Exynos8 RTC data. Separate PMIC RTC child | Linux 6.18 RTC driver/binding lack Exynos8 compatible; Exynos850 sibling has different base, two IRQs and clock. No upstream S2MPU08 RTC transport | Keep both RTC paths out. Add support only after modern register/IRQ/clock mapping and PMIC transport are established; see RTC/watchdog review. |
| Watchdog/reboot/poweroff | Exact node is `samsung,exynos8-wdt` at 0x10060000/SPI 233; clocks OSCCLK + GATE_WDT_CLUSTER1; timeout 30s; Samsung driver uses PMU disable/reset bit 24 | Linux 6.18 has no Exynos8 match or binding compatible; Exynos7 uses bit 23 and Exynos7885 upstream clock provider lacks the legacy WDT gate ID | Keep watchdog absent until driver variant, schema, and clock-provider mapping are implemented. Do not infer PMIC poweroff from vendor policy strings; see RTC/watchdog review. |
| USB | Samsung parent UDC at 0x13600000 with DWC3 child and Exynos7885 custom USB DRD PHY at 0x135d0000 plus PHY subregions; A10 requests OTG, high-speed | Upstream 6.18 tree has no matching Exynos7885 DWC3 glue/PHY topology | Blocked pending a supported PHY/glue implementation. Do not add only the generic DWC3 child; missing PHY/regulator/role path is material. |
| Battery/charging | A10 battery profile and `sec_battery.c`, `sec_charger.c`, `sec_fuelgauge.c`; ADC/fuel-gauge/charger dependencies and battery model tables are in exact Samsung source | Standard Linux power-supply framework exists, but S2MPU08/charger glue and A10 calibration are not mapped | Samsung kernel implements charging state, temperature/swelling limits, OVP/UVLO response, charge disable, current/float-voltage changes, and fuel-gauge scaling/filtering. These depend on Samsung HAL-to-PMIC/ADC functions and exact profile data. Keep the A10 charging path unenabled until hardware driver/calibration are supported. Exact Android user-space daemon names are not in the acquired Platform archive. |
| Thermal | Three A10-family SoC TMU nodes use `samsung,exynos7885-tmu` at 0x10070000 (BIG/LITTLE) and 0x10074000 (G3D); separate AP thermistor reads Exynos ADC channel 0 with Samsung ADC-to-temperature table | Linux 6.18 `exynos_tmu.c` match table has no `samsung,exynos7885-tmu`; the Exynos7885 DTSI has no corresponding upstream sensors | Keep thermal zones and sensor nodes disabled until register layout, trip/trim calibration, sensor hierarchy, and the AP thermistor binding are mapped. Userspace thermal reporting cannot substitute for kernel trips or charger protections.
| Wi-Fi/BT/touch/audio/modem | Samsung SCSC, SEC touchscreen, audio, sensors, modem/IPC nodes and Android services | Most are vendor-only or need exact-chip upstream matches | Later optional work after boot, storage, console, PMIC, thermal and charging. Jackpot LTE may inform shared Exynos7885 SoC pieces only; it is not A10 evidence. |

## eMMC timing semantics

Exact Samsung `dw_mmc-exynos.h` defines the legacy tuple as `(div, fine_drive, drive, sample)`. The legacy eMMC base values are therefore divider 3, fine-drive 0, drive 4 and sample 0 for SDR; divider 3, fine-drive 0, drive 4 and sample 2 for DDR. Linux 6.18 `dw_mmc-exynos.h` defines CLKSEL fields for sample bits 0..2, drive bits 16..18 and divider bits 24..26. Its parser calls `SDMMC_CLKSEL_TIMING(timing[0], timing[1], div)`; the current binding describes the two array cells as TX and RX phase values. The code field names establish the modern positional contract, but naming equivalence across both drivers does not prove electrical equivalence of the A10 board.

The candidate preserves the exact sample and drive values in Linux's required SDR/DDR arrays and separates the divider. It does not advertise MMC DDR, HS200, or HS400 in DT. Samsung's separate HS200 timing property has no Linux 6.18 field; HS400 has a current field, but its A10 tuple and `hs400-delay-line` value need a dedicated old-versus-new register-semantics review and voltage-path proof. The 6.18 driver advertises some host capabilities internally, so the DT flags alone are not treated as evidence that these modes are safe. Revisit these limits after PMIC/regulator support is available.

## Implementation and validation state

Patch 0002 (`patches/linux-6.18.54/0002-arm64-dts-exynos-enable-a10-emmc-uart.patch`) was applied in the existing Colab checkout after patch 0001 on upstream Linux commit `1b357ecb321392158d507b04672ffee57bfa071d` (kernel version 6.18.54). The final A10 DTB SHA-256 is `599938bfe2cbbc441bc0bb1220e56a44f3e17f96e4432151919803d0049b99d9`. MMC and Samsung UART `dt_binding_check`, targeted `CHECK_DTBS=y` builds for the A10 DTB, direct `dt-validate` for each binding, and `git diff --check` all exited successfully. Binding generation warned that optional `yamllint` was unavailable.

This validation is host-side DT compilation/schema checking only. The SD2-only DTB hash `da3ce7e3a4d4d6d2a802b1c0b8a88d47886db8269eedc863ecf9f8419d9db30e` belongs to the earlier milestone; the eMMC/UART content is included in the final hash above. The worktree also includes the previously added SoC mmc_2 node and A10 Makefile target. Jackpot LTE output is sibling-only evidence, never an A10 boot result.

## Root handoff and first-boot selector

The current initramfs accepts only an explicit `root=/dev/mmcblk0pN` path, validates the numeric partition suffix, waits for that block device, mounts ext4 read-write, and requires executable `/sbin/init`. It rejects UUID/PARTUUID as well as removable SD and non-eMMC paths. The A10 DT aliases map internal eMMC to MMC host index 0, but the physical partition number remains unmeasured. This resolver was fixed to be sourced by `/init`; see `docs/reports/initramfs-root-helper-fix-20260929.md`.

Do not guess a root UUID/PARTUUID. Keep the eventual measured eMMC partition path injectable via the boot command line. A possible opt-in discovery mode would require a paired install-specific marker and expected value, read-only/no-journal probes limited to eMMC, an exact-one-match rule, and fail-closed handling. It is not implemented: the corrected BusyBox/initramfs artifact is unavailable for verifying mount options and unmount behavior. See `docs/reports/root-device-discovery-assessment-20260929.md`.

## Battery, charging and thermal blocker

The exact downstream source includes `sec_battery.c`, `sec_battery_data.c`, `sec_charger.c`, and `sec_fuelgauge.c`, and the A10 DTS has S2MPU08 rails/IRQ and battery platform data. These kernel drivers expose low-level measurements/controls; Android's BatteryService, health HAL, vendor daemons and policy are userspace components that Debian must replace for userspace charging status, health reporting, charge policy and suspend coordination. Linux kernel thermal and regulator protection must be available independently; userspace policy is not a thermal safety substitute.

Before any physical boot test, establish that the upstream kernel has working battery voltage/current/temperature readings, charge enable/current controls, thermal sensor calibration and safe over-temperature behavior, plus a userspace status/policy replacement. The exact active Samsung thermal/battery device configuration and daemon-to-driver interface remain to be traced. No charging or thermal behavior is claimed for Linux 6.18.

## Exact Linux 6.18 sources consulted

- `arch/arm64/boot/dts/exynos/exynos7885.dtsi` at `gregkh/linux` `v6.18.54`: existing `mmc_0` (0x13500000/SPI 146, Exynos7885 SMU compatible and embedded clocks), `serial_2`, pinctrl.
- `Documentation/devicetree/bindings/mmc/samsung,exynos-dw-mshc.yaml`: compatible list, required SDR/DDR arrays, CIU divider requirement, cell meanings and phase ranges.
- `drivers/mmc/host/dw_mmc-exynos.c`, `dw_mmc-exynos.h`: parser, HS400 path, capabilities, clock divider and timing register field positions.
- Samsung exact source: `arch/arm64/boot/dts/exynos/dtbo/exynos7885.dts`, `exynos7884B-a10_common.dtsi`, `exynos7884B-a10_swa_open_00.dts`, `exynos7884B-a10_swa_open_gpio_00.dtsi`, `drivers/mmc/host/dw_mmc-exynos.{c,h}`, `drivers/regulator/s2mpu08.c`, `drivers/mfd/s2mpu08_core.c`, `drivers/thermal/samsung/exynos_tmu.c`, and battery drivers.


## RAM interval decision

The exact Samsung A10 source-to-upstream review is in `docs/reports/linux-6.18.54-a10-memory-review-20260929.md`. Patch 0004 reserves the fixed physical ranges only, after checking interval containment and overlap against the two populated banks. It does not implement ION or claim that downstream secure/modem/GNSS/framebuffer consumers have a Linux 6.18 equivalent. Dynamic allocation pools and `no-map`/reusable semantics remain explicit open items.

Focused Linux 6.18.54 result for this milestone: `dt_binding_check` on the reserved-memory schema and the A10 `CHECK_DTBS=y` build passed; direct `dt-validate` emitted no reserved-memory diagnostics but did report the existing A10 root-compatible and osc-clock fixed-clock issues. The compiled DTB SHA-256 is `ea5b3131cfa55e02472d6f74815082282f0e3b8940471311545e558d380905b7`. This is not a full-tree validation or device result.


## RTC and watchdog decision

Exact Samsung RTC/watchdog source semantics and the reasons neither node is currently supportable in Linux 6.18 are recorded in `docs/reports/linux-6.18.54-a10-rtc-watchdog-review-20260929.md`. These devices remain excluded from the DTS pending driver, binding, and clock mapping work.


## S2MPU08 transport detail

Exact-source transport, register-access, regulator and IRQ findings are documented in [`linux-6.18.54-a10-s2mpu08-transport-review-20260929.md`](linux-6.18.54-a10-s2mpu08-transport-review-20260929.md). The Samsung 4.4 core routes PMIC register access through Exynos ACPM, creates logical dummy I²C clients for four address spaces, and supplies S2MPU08-specific IRQ/MFD children. Linux 6.18 SEC I2C support covers neighboring SEC PMICs but does not contain this compatible or S2MPU08 register data; SEC ACPM support targets another PMIC family. The A10 S2MPU08 node and dependent regulator claims therefore remain excluded until transport availability, MFD/regmap/IRQ support, regulator semantics and safe voltage consumers are established.


## USB DRD and PHY detail

The exact Samsung-to-upstream review is in [`linux-6.18.54-a10-usb-drd-review-20260929.md`](linux-6.18.54-a10-usb-drd-review-20260929.md). Samsung's A10 parent uses `samsung,exynos-dwusb`, one `hsdrd` clock and nested DWC3, while its PHY uses `samsung,exynos-usbdrd-phy`, three register regions, five clocks, PMU offsets and custom revision/reference/tuning properties. The 4.4 PHY explicitly sets a 50 MHz reference clock for Exynos7885. Linux 6.18.54 has no matching glue/PHY compatible or Exynos7885 PHY data; its Exynos DWC3 binding requires supply wiring. No USB node was enabled, and no Exynos7870/850 compatible was copied.


## Latest clean rebuild state — 2026-09-29

The validated A10 DTB was rebuilt from clean pinned Linux v6.18.54 commit `1b357ecb321392158d507b04672ffee57bfa071d` after sequential application of the corrected tracked patch series. Its current SHA-256 is `36f1effe96b5fa41912d1a06c604de8a97f5d5243527aa6cf689321e78bfa05f` (21,555 bytes). Focused MMC/UART/GPIO-key/pinctrl/Samsung-board binding checks and direct validation pass. Unfiltered validation has one inherited diagnostic: `osc-clock` is missing required `clock-frequency`; no A10 frequency has been inferred from Jackpot LTE. The Exynos-enabled aggregate generated 20 arm64 DTBs and logged this diagnostic plus assembler/Kconfig noise; it is not claimed as a clean aggregate schema pass. Detailed log and commands are in `docs/reports/linux-6.18.54-a10-dtb-validation-20260929.md`.


## Fixed oscillator mapping completed — 2026-09-29

Samsung A10 overlay `arch/arm64/boot/dts/exynos/dtbo/exynos7884B-a10_common.dtsi` (SHA-256 `b3f7ae8a2cfb47fcc0171f8797fa2110c15182643cb26e814208e2c2be625083`) defines the board fixed-rate `oscclk` as 26 MHz. Samsung Exynos7885 base DTS independently uses 26 MHz for the ARMv8 timer. The upstream Exynos7885 `oscclk` is already a standard `fixed-clock`; setting its standard `clock-frequency` in the A10 board DTS is the direct binding mapping. Patch 0002 now carries this A10-only property. Jackpot LTE was not used as A10 evidence.

The resulting 21,587-byte A10 DTB SHA-256 is `44a77aa2c6ce133def05a8a4986181328c32962a4e7c564fdb2e24e7d6358166`. Focused A10 schemas, focused and unfiltered direct `dt-validate`, and the fresh Exynos-enabled aggregate (20 arm64 DTBs; assembler warning only) completed without schema diagnostics. Full details and archive hashes are in `docs/reports/linux-6.18.54-a10-dtb-validation-20260929.md`.
