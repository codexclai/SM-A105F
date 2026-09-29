# Linux 6.18.54 A10 DTB validation — 2026-09-29

## Temporary-tree recovery

The partial Colab tree was inspected before cleanup. The malformed Makefile target and misplaced board timing edits were discarded by restoring the affected Makefile and SoC DTSI from pinned upstream. Intended hardware properties were recreated in the board DTS; board-specific MMC timing tuples remain out of the SoC DTSI.

Pinned source: Linux v6.18.54 commit `1b357ecb321392158d507b04672ffee57bfa071d`.

## Board compatible correction

The downstream marketing string `samsung,A10 SWA OPEN 00` contains spaces and fails the DT compatible pattern and supported Samsung board list. It is replaced with the model-specific `samsung,sm-a105f`, retaining `samsung,exynos7885` as the fallback. This board identification is registered under Exynos7885 in `samsung-boards.yaml`.

The patch series now carries the DTS compatible in patch 0001 and the corresponding context in patch 0004; patch 0005 adds the binding enum. The schema hunk was generated from the tracked schema change and passed a `git apply --reverse --check`, reverse-apply, and re-apply round trip on the reconstructed tree.

## Build and focused validation

- Host: authenticated Google Colab runtime, Ubuntu 24.04, 2 vCPU, 12.67 GiB RAM; no GPU requirement.
- Tools: AArch64 GCC cross compiler, dtc 1.7.0, dtschema/dt-validate 2026.9.
- A10 `CHECK_DTBS=y` build returned exit 0 after compatible correction.
- `dt_binding_check` for the Samsung board schema returned exit 0; direct board-schema validation of the compiled A10 DTB returned exit 0.
- Earlier individual `dt_binding_check` runs for `samsung,exynos-dw-mshc.yaml`, `samsung_uart.yaml`, `gpio-keys.yaml`, and `samsung,pinctrl-pins-cfg.yaml` returned exit 0. Each targeted A10 build and `dt-validate -l <schema>` returned exit 0 with no diagnostics.
- Full direct `dt-validate` now reports only one diagnostic: inherited Exynos7885 `osc-clock` has no required `clock-frequency`.
- The reserved-memory directory in this pinned tree contains `reserved-memory.txt`, not a `reserved-memory.yaml`; no reserved-memory-node diagnostic appeared in direct core validation.
- `git diff --check` passed.
- Corrected A10 DTB: 21,555 bytes, SHA-256 `36f1effe96b5fa41912d1a06c604de8a97f5d5243527aa6cf689321e78bfa05f`.

Kconfig still emitted prompt text during target setup despite an `oldconfig` pass; config prompts were isolated from the shell commands and each target returned 0. Stabilize and preserve a clean config snapshot before treating the invocation as a reproducible build recipe. Whole-tree `dtbs_check` is not complete.

## Evidence gaps and next work

The upstream Exynos7885 sibling DTS sets `oscclk` to 26 MHz; this remains SoC-sibling evidence, not A10-specific proof. No oscillator frequency is added to the A10 board DTS until exact A10 source evidence is checked.

The connected Drive project folder contains original Samsung source ZIP parts, old Eureka bundles, and a project checkpoint; it does not contain the exact 4.4.177 output bundle. GitHub release metadata identifies a prior host-only candidate archive (12,118,381 bytes; SHA-256 `f28d6a293695ae6075123a4ed9af0a9c5f19b0f7fe6c125c98a71e87cfd98ae5`), but the current GitHub connector does not expose its private bytes. No candidate was extracted or regenerated in this run. Use a binary-capable authorized route and compare every recovered artifact to its recorded manifest before reuse.

No phone or physical-device operation occurred.


## Clean pinned rebuild and aggregate check — 2026-09-29

The disposable Colab tree was not reused. A fresh upstream Linux v6.18.54 checkout at commit `1b357ecb321392158d507b04672ffee57bfa071d` was used. The tracked A10 patch series from private `main` was applied and checked in order. During that round-trip, stale context in patches 0003 (GPIO keys) and 0004 (fixed memory) was corrected in private `main`; the series then applied cleanly, and the resulting A10 board DTS and schema matched the validated workspace files byte-for-byte. `git diff --check` passed. No temporary Makefile target or misplaced SoC-DTSI timing edits were carried forward.

Rebuilt A10 DTB: 21,555 bytes, SHA-256 `36f1effe96b5fa41912d1a06c604de8a97f5d5243527aa6cf689321e78bfa05f`. The rebuilt artifact was decompiled and inspected for GPIO keys, reserved memory, and SD card detect. The A10 SD host remains at 0x13550000 with IRQ 147, SD2 pins, and active-low card detect on GPA0 pin 7.

Focused checks on the rebuilt artifact:

- `dt_binding_check` for Exynos DW MMC, Samsung UART, GPIO keys, Samsung pinctrl, and Samsung boards schemas returned 0.
- `dt-doc-validate` and repository `yamllint` for those five schemas returned 0.
- Targeted A10 `CHECK_DTBS=y` completed; focused direct `dt-validate -l` across those schemas returned 0 with no diagnostics.
- Unfiltered direct `dt-validate` still emits exactly one inherited diagnostic: Exynos7885 `osc-clock` lacks required `clock-frequency`. The value remains unresolved; Jackpot LTE’s 26 MHz value is sibling evidence only and was not copied.

A real Exynos-enabled aggregate was run after setting `CONFIG_ARCH_EXYNOS=y`; 20 arm64 DTBs were generated. The command returned 0 and its captured log contains the known A10 `osc-clock` schema diagnostic, an assembler `.inst` reliability warning, and Kconfig restart prompt noise. Since the kernel build recipe masks some dtbs-check validator status, this is recorded as a completed aggregate invocation with one known schema warning, not a clean full-tree schema pass. Log: `full-exynos-dtbs-check.log` in the execution workspace.

The container lacked system /tmp and package state. Required build/schema tools were obtained or installed into workspace-local directories; no host packages or tracked source were modified for this setup.

The current artifact acquisition and boot-chain gaps remain as documented above. No physical device was accessed.
