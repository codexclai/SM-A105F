# A10 USB DRD and PHY port review — 2026-09-29

## Scope and exact evidence

Compared the user-supplied Samsung SM-A105F SWA 4.4.177 source (archive SHA-256 `5c83be7c2452d644ccda1deb898d9a54f2b3d53d3a0e66a7a394dcbf14439931`) against Linux 6.18.54 DWC3/Exynos glue, PHY driver and bindings. No hardware test occurred.

Exact A10 board source, `arch/arm64/boot/dts/exynos/dtbo/exynos7885.dts` (SHA-256 `9d6b88c24a05ba20cf49de666f9775a9437df6911459902017e92f8bb8264f79`), declares:
- a disabled parent `samsung,exynos-dwusb` at 0x13600000, size 0x10000, with one `hsdrd` clock;
- a nested Synopsys DWC3 core at the same base, SPI 135, two PHY specifiers named usb2-phy/usb3-phy, and several downstream-only properties;
- an Exynos DRD PHY at 0x135d0000 with three register ranges (0x200, 0x1000, 0x800), five clocks (hsdrd, usb20, usb30_0, usb30_1, out_usb), and a PMU syscon reference plus offsets/masks.

A10 overlay `exynos7884B-a10_common.dtsi` (SHA-256 `b3f7ae8a2cfb47fcc0171f8797fa2110c15182643cb26e814208e2c2be625083`) enables the DWC3 parent and PHY, selects OTG and high-speed maximum speed, sets the standard frame-length-adjustment quirk to 0x20, and supplies an HS tuning phandle.

## Old driver semantics

- Exact Samsung glue `drivers/usb/dwc3/dwc3-exynos.c` (SHA-256 `540c8603222d694998c8227cb9d18fa58a5a4497f8dbacbf761bb0914490d8dc`) matches `samsung,exynos-dwusb`. Its legacy glue acquires the named HS DRD clock and populates the generic DWC3 child. This does not by itself implement the PHY.
- The exact kernel archive also includes `drivers/phy/phy-exynos-usbdrd3.c` (SHA-256 `2d19d7a1097e6f013b327eb99168aeddacfa5dcb27527173b00f83546ea78010`), `phy-exynos-usbdrd.c` (SHA-256 `0ff72da6011e6fd9942e578a58d81a5c9796d2b41facb65a833f69e6757b4fae`) and `phy-exynos-usbdrd.h` (SHA-256 `d29aeb20683c61441b5f997b0b39bd59b21898d8a0255e42c1ead961f0757a1d`).
- The older board source selects a configurable multi-register PHY implementation through the generic legacy PHY compatible. It reads custom properties for PHY/sub-PHY revisions, reference-source selection, clock mux and reference clock, controller type, PMU isolation, VBUS-pad use and tuning tables. For `CONFIG_SOC_EXYNOS7885`, the old PHY clock-enable path explicitly sets its reference clock to 50 MHz. Those values are part of PHY initialization behavior; they are not aliases for mainline clock or PHY properties.
- A10's `hs_tune_param` is a phandle to a tuning table in the overlay. Its semantics are consumed by the legacy driver and are not established as equivalent to any 6.18 Exynos PHY tuning format.

## Linux 6.18.54 comparison

Pinned sources inspected:
- `drivers/usb/dwc3/dwc3-exynos.c` and `Documentation/devicetree/bindings/usb/samsung,exynos-dwc3.yaml`: compatible table includes Exynos5250/5433/7/7870/850 and newer SoCs, but not `samsung,exynos-dwusb` or Exynos7885. The supported clock names/counts are SoC-specific. The binding requires a `vdd33-supply`; several SoC variants also require `vdd10-supply`.
- `drivers/phy/samsung/phy-exynos5-usbdrd.c`: PHY match data includes Exynos5250, 5420, 5433, 7, 7870, 850, 990, 2200 and GS101. It does not match A10's `samsung,exynos-usbdrd-phy` compatible nor contain an Exynos7885 data entry. The supported probe expects a current compatible/register/clock/regulator description, with optional named phy/pcs/pma ranges.
- Generic DWC3 child operation cannot substitute for missing glue, PHY calibration, power rails, PMU isolation or connector role/VBUS handling.

The 6.18 source URLs are pinned to upstream tag `v6.18.54`: [DWC3 Exynos glue](https://github.com/gregkh/linux/blob/v6.18.54/drivers/usb/dwc3/dwc3-exynos.c), [Exynos DWC3 binding](https://github.com/gregkh/linux/blob/v6.18.54/Documentation/devicetree/bindings/usb/samsung%2Cexynos-dwc3.yaml), and [Samsung Exynos DRD PHY](https://github.com/gregkh/linux/blob/v6.18.54/drivers/phy/samsung/phy-exynos5-usbdrd.c).

## Decision and required port work

Keep the USB parent, DWC3 child and PHY out of the Linux 6.18 A10 DTS. The overlay's high-speed cap and generic frame-length quirk do not satisfy the unported clock/PHY/regulator contract. Do not relabel the node as Exynos7870 or Exynos850: neither source proves identical Exynos7885 PHY registers, calibrations, clock tree, PMU offsets or VBUS policy.

A future USB port requires a reviewed Exynos7885 PHY driver-data implementation or a register-level proof that an existing 6.18 PHY variant is identical, a DWC3 glue binding/match with correct clocks and regulators, compatible GPIO/role/VBUS detection, regulator availability (currently blocked by S2MPU08), and schema/build validation. The exact Samsung source currently provides legacy register/tuning implementation evidence, but no upstream validation or hardware evidence.
