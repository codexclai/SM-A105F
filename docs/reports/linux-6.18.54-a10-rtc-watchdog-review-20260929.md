# A10 RTC and watchdog review — 2026-09-29

## Source identity

This review uses the exact user-supplied Samsung SM-A105F SWA source archive recorded in `docs/SOURCES.md`: archive SHA-256 `5c83be7c2452d644ccda1deb898d9a54f2b3d53d3a0e66a7a394dcbf14439931`. Relevant extracted file hashes:

| File | SHA-256 |
| --- | --- |
| `arch/arm64/boot/dts/exynos/dtbo/exynos7885.dts` | `9d6b88c24a05ba20cf49de666f9775a9437df6911459902017e92f8bb8264f79` |
| `drivers/rtc/rtc-s3c.c` | `3d3d94cbc698302f53acd1676488c65ad0d309ece889fd53c9d14a6a1221f593` |
| `drivers/rtc/rtc-s2mpu08.c` | `2fdcaf26f94897ac29fc7d2fe4a0177ed48ce0d3268e0f04dce320a7d930775a` |
| `drivers/watchdog/s3c2410_wdt.c` | `17a551e00394a25bb742a2cdddceee442e075da0ade4967c92764399514f31c1` |

Compared with Linux v6.18.54 at source commit `1b357ecb321392158d507b04672ffee57bfa071d`.

## RTC

The Samsung Exynos7885 DTS declares `rtc@11C90000`, compatible `samsung,exynos8-rtc`, register range `0x11c90000/0x100`, and three interrupt specifiers `<0 27 0>`, `<0 28 0>`, and `<0 36 0>`. It declares no clock property.

Samsung 4.4 `drivers/rtc/rtc-s3c.c` explicitly matches `samsung,exynos8-rtc` to a dedicated `exynos8_rtc_data` structure. That structure uses the S3C6410 IRQ handler, tick/frequency operations, and enable/disable callbacks, with a maximum user frequency of 32768 Hz and clock-control disable enabled. This establishes that the compatible is intentional in the old driver, but does not prove Linux 6.18's RTC implementation can consume the same three-interrupt/no-clock node.

The pinned Linux 6.18.54 `rtc-s3c.c` does not match `samsung,exynos8-rtc`; its binding `s3c-rtc.yaml` does not list that compatible. The existing upstream Exynos850 RTC sibling uses a different base (`0x11a30000`), two IRQs, and a named APM peripheral clock. Those sibling values do not map to the A10 source. The vendor PMIC RTC is a separate S2MPU08 child; upstream 6.18 has no S2MPU08 MFD/RTC transport support.

**Decision:** no RTC node or compatible alias is added. A safe port requires a deliberate Linux driver/binding extension based on full old-versus-new register and IRQ semantics, plus the right clock model. The SoC RTC remains absent from the A10 candidate; the PMIC RTC remains blocked by PMIC support. No date-setting policy is carried into DTS.

## Watchdog

The exact Samsung SoC DTS declares `watchdog@10060000`, compatible `samsung,exynos8-wdt`, register range `0x10060000/0x100`, legacy interrupt tuple `<0 233 0>`, clocks `OSCCLK` and `GATE_WDT_CLUSTER1` named `rate_watchdog` and `gate_watchdog`, timeout 30 seconds, and the PMU syscon phandle.

Samsung 4.4 `drivers/watchdog/s3c2410_wdt.c` has an explicit `samsung,exynos8-wdt` match. Its Exynos8 variant selects PMU watchdog-disable and reset-mask registers and bit 24 for both, with reset-status register/bit 24. Thus the old compatible does not merely mean generic Exynos7. The clock provider separately defines OSCCLK as a 26 MHz root and a WDT cluster1 gate.

Linux 6.18.54 has no `samsung,exynos8-wdt` entry in the Samsung watchdog binding or driver match table. Its Exynos7 variant uses bit 23; the Exynos850 variant is a different cluster-aware implementation. The upstream Exynos7885 clock provider does not expose the old `GATE_WDT_CLUSTER1` clock ID, so translating the watchdog node alone would leave a required clock unresolved. Neither Jackpot LTE nor Exynos850 supplies A10 reset-bit or clock evidence.

**Decision:** watchdog stays absent from the A10 DTS. Enabling it safely requires a modern driver variant with the recorded Exynos8 PMU bit semantics, a binding update, and a verified Linux 6.18 clock-provider mapping for both clocks. No 30-second timeout is added without a supported probe path.

## Validation and limits

This is a source/binding review; no RTC or watchdog patch was produced because the required current driver/binding/clock path is not present. The Linux 6.18.54 A10 DTB status is unaffected. The exact Samsung source archive is user-supplied and hash-verified, not independently Samsung-signed. No physical device was accessed and no runtime RTC, reboot, or watchdog behavior is claimed.

Next investigation: examine Linux 6.18 Exynos7885 clock-controller IDs/provider and PMU syscon bindings for a supportable watchdog extension; continue PMIC/regulator work, which also blocks RTC and charging integration.


## Follow-up exact-source verification — 2026-09-29

The three Drive chunks were reassembled in the Colab runtime. The ZIP size is 229,817,794 bytes and its SHA-256 exactly matches the recorded archive hash above. Samsung's extracted `drivers/watchdog/s3c2410_wdt.c` was independently hashed in that archive and matches `17a551e00394a25bb742a2cdddceee442e075da0ade4967c92764399514f31c1`.

The Samsung 4.4.177 Exynos8 variant selects PMU disable register `0x0408`, PMU reset-mask register `0x040c`, reset status register `0x0404`, and bit 24 in all three. Its documented reset-status label is A53 WDTRESET. Its old-driver quirk flags are exactly PMU configuration and reset-status support; it does **not** select the old driver's WTCLRINT quirk. The watchdog MMIO block uses the S3C watchdog register layout: WTCON at `0x00`, WTDAT at `0x04`, WTCNT at `0x08`, and WTCLRINT at `0x0c`; the latter is not accessed for this Exynos8 variant by the old driver's quirk-gated clear path. This distinction matters: Linux 6.18's candidate variant should use `QUIRK_HAS_PMU_MASK_RESET | QUIRK_HAS_PMU_RST_STAT` only. It must not copy Exynos7's WTCLRINT or automatic-disable flags. In 6.18, reset-mask bit set means mask/disable the watchdog reset request; reset-status bit 24 is read as `WDIOF_CARDRESET` boot status.

The source-derived clock mapping is also concrete. Samsung 4.4 names the ordered clocks `OSCCLK` (`rate_watchdog`) and `GATE_WDT_CLUSTER1` (`gate_watchdog`). The old clock source identifies OSCCLK as a 26 MHz root. Linux 6.18's Exynos7885 clock provider exposes the WDT1 peripheral PCLK gate; the source clock should therefore map to the oscillator and the bus clock to WDT1 PCLK, while using modern driver order/names `watchdog` then `watchdog_src`. These old and new names are API translations, not evidence that the provider's numeric IDs are identical.

The Samsung board file associates the watchdog with A53-class Exynos7884B/7885 and bit 24. Exynos7 bit 23 and Exynos850 cluster-indexed variants are not valid substitutes. The watchdog register and PMU mappings above apply to the source's `samsung,exynos8-wdt`; they are not inferred from nearby SoCs.

This completes the source-side semantic check and supports a narrowly scoped Linux 6.18 Exynos8 driver/binding extension. No driver, binding, or DTS change has yet been made from this follow-up, and no WDT-specific schema/DTB or driver compile result is claimed. The earlier “no patch” status remains the current code state. Next execution must implement and validate the extension before enabling it in the A10 board DTS.