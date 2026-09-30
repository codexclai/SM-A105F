# Exynos7885/A10 watchdog implementation — 2026-09-30

## Scope and evidence

This patch extends the pinned Linux v6.18.54 watchdog driver for the Samsung Exynos8 WDT1 used by SM-A105F. It follows the exact-source findings in [the 2026-09-29 RTC/watchdog review](linux-6.18.54-a10-rtc-watchdog-review-20260929.md) and keeps its hardware evidence separate from the modern Linux representation.

| Function | PMU offset | Bit | Linux behavior |
| --- | ---: | ---: | --- |
| WDT disable | 0x0408 | not represented | Offset is retained in variant data; Linux's disable-register access is gated by `QUIRK_HAS_PMU_AUTO_DISABLE`, which is intentionally absent. |
| Reset masking | 0x040c | 24 | `QUIRK_HAS_PMU_MASK_RESET` only |
| Reset status | 0x0404 | 24 | `QUIRK_HAS_PMU_RST_STAT` only |

The Exynos8 variant does not inherit Exynos7 auto-disable behavior, Exynos850 cluster behavior, or the Exynos850 inverted reset-mask semantics. Its compatible is `samsung,exynos8-wdt`.

The binding requires two clocks and names for this compatible and applies no cluster-index requirement. The shared Exynos7885 DTSI contains a disabled WDT1 node with `watchdog` mapped to `CLK_GOUT_WDT1_PCLK` and `watchdog_src` mapped to `oscclk`; A10's board DTS sets that oscillator to 26 MHz, enables the node, and uses the Samsung-source 30-second timeout. The Samsung IRQ tuple `<0 233 0>` is preserved as `<GIC_SPI 233 IRQ_TYPE_NONE>`; no trigger type is inferred.

## Validation

Linux source commit: `1b357ecb321392158d507b04672ffee57bfa071d`.

Passed in the Colab Linux tree:

- `make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- drivers/watchdog/s3c2410_wdt.o`
- `dt-doc-validate Documentation/devicetree/bindings/watchdog/samsung-wdt.yaml`
- `yamllint -d relaxed Documentation/devicetree/bindings/watchdog/samsung-wdt.yaml` (exit 0; reports the existing long line at 23)
- `make ARCH=arm64 DT_SCHEMA_FILES=Documentation/devicetree/bindings/watchdog/samsung-wdt.yaml dt_binding_check`
- `make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- DT_SCHEMA_FILES=Documentation/devicetree/bindings/watchdog/samsung-wdt.yaml CHECK_DTBS=1 exynos/exynos7885-a10.dtb`
- direct `dt-validate -s Documentation/devicetree/bindings/processed-schema.json arch/arm64/boot/dts/exynos/exynos7885-a10.dtb` (no diagnostics)
- patch round-trip against the reconstructed five-patch baseline: reverse check, reverse apply, forward check, forward apply; all exited 0
- `git diff --check`

Decompilation confirms `samsung,exynos8-wdt`, register `0x10060000/0x100`, SPI 233 with unspecified trigger, both named clocks, PMU syscon, `status = "okay"`, and `timeout-sec = <30>`. The compiled DTB is 21,838 bytes; SHA-256 `655c29627e97c447b58ecbe66ac06d365a085e0147096c1d52293f99f727c52e`.

CodexCLI (GPT-6 Luna High) and a separate read-only reviewer found no substantive implementation issue. The project-wide regression tests were not run: the Colab checkout contains the Linux tree rather than the project repository, and unauthenticated Git transport to the private repository is unavailable. This change has build/schema/DT validation but no physical-device test.

## Next subsystem: ACPM / S2MPU08

Do not add an A10 ACPM node or regulator alias yet. Linux 6.18.54's ACPM firmware transport and mailbox match GS101 only, and its ACPM MFD client is S2MPG10 only. The A10 source review records S2MPU08 under an ACPM parent on channel 2 and calls to legacy `exynos_acpm_*_reg()` helpers, but does not establish compatibility with the upstream shared-memory/ring ABI or prove that the normal A10 boot chain provides the needed APM firmware and SRAM/mailbox resources.

The next action is to inspect the already-reassembled exact Samsung Kernel archive in Colab (or recover it from its three recorded Drive chunks if it is absent), locate the legacy ACPM provider, SRAM/mailbox/channel definitions, and firmware handoff, then compare those details to Linux 6.18.54. Keep the gap open until that evidence exists; do not copy GS101 resources. No physical-device action was performed.
