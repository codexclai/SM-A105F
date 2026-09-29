# Linux 6.18.54 A10 DTB validation — 2026-09-29

## Temporary-tree recovery

The partial Colab tree was inspected before cleanup. An earlier malformed Makefile target and misplaced SD timing edits were discarded by restoring the affected Makefile and SoC DTSI from pinned upstream. The intended board-specific timing values were recreated only in `exynos7885-a10.dts`; none were copied into the SoC DTSI. The working tree now contains only the intended A10 Makefile target, disabled Exynos7885 SD2 controller node, and A10 board DTS.

Pinned source: Linux v6.18.54 commit `1b357ecb321392158d507b04672ffee57bfa071d`.

## Build and focused validation

- Host: authenticated Google Colab runtime, Ubuntu 24.04, 2 vCPU, 12.67 GiB RAM; no GPU requirement.
- Tools: AArch64 GCC cross compiler, dtc 1.7.0, dtschema/dt-validate 2026.9.
- `make ARCH=arm64 defconfig` and targeted `CHECK_DTBS=y` A10 DTB builds returned exit 0.
- Individual `dt_binding_check` runs for `samsung,exynos-dw-mshc.yaml`, `samsung_uart.yaml`, `gpio-keys.yaml`, and `samsung,pinctrl-pins-cfg.yaml` returned exit 0. For each, the A10 `CHECK_DTBS=y` build and `dt-validate -l <schema>` returned exit 0 without diagnostics.
- Direct all-schema `dt-validate` returned exactly two pre-existing whole-tree diagnostics:
  1. Root `compatible = "samsung,A10 SWA OPEN 00", "samsung,exynos7885"` fails the supported Samsung board compatible schema and the compatible-string pattern.
  2. Inherited Exynos7885 `osc-clock` has no required `clock-frequency`.
- The reserved-memory directory in this pinned tree contains `reserved-memory.txt`, not a `reserved-memory.yaml`; so an attempted targeted YAML check for that nonexistent schema was skipped. The direct core validation produced no reserved-memory-node diagnostic.
- `git diff --check` passed.
- Produced A10 DTB: 21,563 bytes, SHA-256 `3e059201353c87f4c310109f83f9bec8bbd4fcff3bcbb69057223d6031663549`.

The first targeted invocation emitted Kconfig prompts before continuing. Although the build target returned success, stabilize the generated .config and rerun the documented commands in a fresh pinned checkout for fully reproducible build logs. The DTB is a host build artifact, not A10 boot evidence.

## Evidence gaps and next work

The upstream Exynos7885 sibling board sets `oscclk` to 26 MHz; this is SoC-sibling evidence, not A10-specific proof. No oscillator frequency is added to the A10 board DTS until exact A10 source evidence is checked. Likewise, the unsupported downstream marketing string is not silently rewritten or added to the upstream compatible schema. Choose a standard A10 board compatible only with a documented binding change or exact source evidence.

The connected Drive project folder contains original Samsung source ZIP parts, old Eureka bundles, and a project checkpoint; it does not contain a matching 4.4.177 kernel/initramfs/DT/DTBO output bundle. GitHub release metadata identifies a prior host-only candidate archive (12,118,381 bytes; SHA-256 `f28d6a293695ae6075123a4ed9af0a9c5f19b0f7fe6c125c98a71e87cfd98ae5`), but the current GitHub connector does not expose the private release asset bytes. No candidate was extracted or regenerated in this run. Use an approved binary-capable route and compare all recovered bytes to their recorded manifests before reuse.

No phone or physical device operation occurred.
