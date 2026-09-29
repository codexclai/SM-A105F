# Current checkpoint — 2026-09-29 (A10 RTC/watchdog source mapping)

This checkpoint records the A10 fixed-memory milestone committed to private `main` at `352253a68217d55d2c4d21ed9c72b7e074257b9f`; this status/journal checkpoint is committed immediately after that source milestone.

Patch `patches/linux-6.18.54/0004-arm64-dts-exynos-reserve-a10-fixed-memory.patch` carries Samsung's exact top-level `/memreserve/ 0xe0000000 0xd00000` plus nine fixed `reserved-memory/reg` regions. The two populated DRAM banks from Samsung's SoC DTSI contain every interval; none of the fixed intervals overlap. Exact source hashes, range table and limits are in `docs/reports/linux-6.18.54-a10-memory-review-20260929.md`.

On Linux 6.18.54 commit `1b357ecb321392158d507b04672ffee57bfa071d`, the corrected patch passed `git apply --check` in an isolated worktree and applied to produce a byte-identical A10 DTS. `git diff --check`, reserved-memory `dt_binding_check`, and targeted A10 `CHECK_DTBS=y` completed with exit 0. The compiled DTB SHA-256 is `ea5b3131cfa55e02472d6f74815082282f0e3b8940471311545e558d380905b7`; `fdtdump` and `fdtget` read back the memreserve and all nine reg tuples.

The direct validator still reports existing A10 root-compatible and `osc-clock` missing `clock-frequency` diagnostics; there were no reserved-memory node diagnostics. The optional yamllint package is absent. No full-tree `dtbs_check` was completed. The patch records physical occupancy only: Android ION consumers, dynamic pools, secure/no-map behavior and reusable semantics are still unresolved. This DTB is host validation, not boot evidence.

The GPIO-key checkpoint suite remains as recorded previously: two focused root-selector tests and shell syntax checks passed in this workspace. The broader initramfs archive test remains blocked because this runtime lacks the verified ARM64 BusyBox and corrected cpio archive. The exact Samsung-built kernel, corrected initramfs and matched A10 DT/DTBO binaries remain unavailable here; no boot image was regenerated. No physical-device operation occurred.

Next: trace the old A10 RTC/watchdog and poweroff paths against Linux 6.18, preserving unsupported semantics, then continue PMIC/regulator and artifact acquisition work independently. Phone remains untouched.


Exact-source RTC/watchdog review was added in `docs/reports/linux-6.18.54-a10-rtc-watchdog-review-20260929.md`. Samsung 4.4 maps `samsung,exynos8-rtc` to a distinct driver variant at 0x11c90000 with three IRQs and no clock; current Linux 6.18 binding/driver lack that compatible. Samsung `samsung,exynos8-wdt` requires PMU bit 24 and the old WDT cluster1 gate clock, which the current Exynos7885 clock provider does not expose. No safe DTS-only mapping was made. Updated port matrix records these findings. Next: assess supportable upstream clock/PMU extension, and continue PMIC/regulator and artifact acquisition work. Phone remains untouched.


## 2026-09-29 — S2MPU08 transport review

Recorded the exact Samsung PMIC contract and upstream support gap in `docs/reports/linux-6.18.54-a10-s2mpu08-transport-review-20260929.md`. The vendor core uses Exynos ACPM register transactions, logical multi-address I2C clients, and a custom IRQ/MFD setup; the regulator driver has S2MPU08-specific workarounds. No DTS or regulator substitution was added. Exact source hashes are in the report. This research does not establish regulator or runtime behavior.


## 2026-09-29 — Binary artifact retrieval audit

The Drive folder's 24 direct children were enumerated; no exact Samsung-built kernel Image, corrected initramfs, or stock A10 DTB/DTBO set was present. The private GitHub API lists a draft host-only boot-candidate asset, but the available connector returns metadata only; its reported digest has not been checked against bytes. The previous browser release-asset attempt errored, so it was not repeated. Full route findings are in `docs/reports/artifact-retrieval-audit-20260929.md`. Do not regenerate the candidate until its required verified inputs are present.
