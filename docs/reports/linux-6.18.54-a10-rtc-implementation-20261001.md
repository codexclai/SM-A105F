# Linux 6.18.54 A10 Exynos8 RTC implementation

Date: 2026-10-01  
Base: upstream Linux 6.18.54, commit `1b357ecb321392158d507b04672ffee57bfa071d`  
Project series prerequisite: patches 0001–0006, reconstructed and applied cleanly before this change.

## Evidence and translation

The exact Samsung A10 source review is recorded in [the RTC/watchdog evidence report](linux-6.18.54-a10-rtc-watchdog-review-20260929.md). It identifies `samsung,exynos8-rtc` at `0x11c90000`, size `0x100`, with alarm/tick_0/tick_1 IRQs 27/28/36 and no clock property. The Samsung driver’s Exynos8 data uses the S3C6410 IRQ and enable/disable routines. Linux 6.18’s S3C RTC driver handles only platform IRQ 0 and requires a named CCF clock for its existing matches. The port therefore adds a dedicated no-clock variant, retains all three Samsung IRQ specifiers in DT, and requires exactly three for this compatible in the binding. Modern driver behavior uses only the alarm IRQ; periodic tick support is not claimed.

The SoC DTSI carries the disabled RTC node. Only the A10 board DTS enables it. The node has no fabricated clock or interrupt names. This is source-, build-, and schema-validated; it has not been physically tested.

## Patch and validation

Patch: `patches/linux-6.18.54/0007-arm64-dts-exynos-add-a10-rtc.patch`.

In the isolated patched Linux worktree:

- `git apply --check` passed for patch 0007 against the clean six-patch baseline.
- `git diff --check` passed.
- `CONFIG_ARCH_EXYNOS=y` and `CONFIG_RTC_DRV_S3C=y`; `drivers/rtc/rtc-s3c.o` compiled for ARM64.
- `make ARCH=arm64 DT_SCHEMA_FILES=Documentation/devicetree/bindings/rtc/s3c-rtc.yaml dt_binding_check` passed.
- `dt-doc-validate` and a PyYAML parse passed. `yamllint` was not available in the configured venv, so no yamllint result is claimed.
- Targeted A10 DTB build with `CHECK_DTBS=1` and the RTC schema passed.
- Focused direct `dt-validate -s …/s3c-rtc.yaml -l samsung,exynos8-rtc` exited 0 without diagnostics.
- Decompiled A10 DTB contains compatible `samsung,exynos8-rtc`, reg `<0x11c90000 0x100>`, IRQ tuples `<0 27 0>`, `<0 28 0>`, `<0 36 0>`, and `status = "okay"`; there is no `clocks` property.
- Resulting DTB: 21,982 bytes, SHA-256 `b021620dc042547ab3855c86e8e0f0b9598d8389f88e52787a1895482cd2998d`.

The architecture-wide arm64 `dtbs_check` remains a separate running job at the latest observation (about 1h56m elapsed). Its observed diagnostics are from unrelated Rockchip/Qualcomm DTs; the log has no A10/Exynos7885 diagnostic so far. It has no captured final exit status and is not claimed as passed. The separate 21-DTB Exynos-scoped check from the prior checkpoint exited 0. The project Python regression suite has not been run in this Linux-only Colab runtime.

No handset operation occurred. Root partition selection remains unresolved; no root argument is inferred.
