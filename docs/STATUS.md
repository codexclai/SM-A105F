# Current checkpoint — 2026-09-29 (A10 GPIO keys)

This checkpoint follows the GPIO-key implementation milestone published on private `main` at `eb310ccc33c56b2678b105685ae0a7ceddb6adc7`; this checkpoint update itself is committed immediately after it. The new patch is `patches/linux-6.18.54/0003-arm64-dts-exynos-add-a10-gpio-keys.patch`, with source-to-upstream semantics in `docs/reports/linux-6.18.54-a10-gpio-keys-review-20260929.md`.

The A10 DTS now describes volume-down GPA1-6, volume-up GPA1-5, and power GPA1-7. The exact Samsung driver reads only the active-low bit from its legacy `0xf` GPIO flags; its power key treats `gpio-key,wakeup` as a boolean. Upstream Linux 6.18 takes the IRQ from the GPIO descriptor when the child has no explicit `interrupts`, so the vendor three-cell IRQ tuple is omitted. Exact EINT and no-pull pinctrl values were mapped to the upstream Exynos macros. No ambiguous drive-strength or extra GPIO flag bits were copied.

Validation on Linux 6.18.54 source commit `1b357ecb321392158d507b04672ffee57bfa071d`: generated patch passed `git apply --check` and applied cleanly; focused `dt_binding_check`, `CHECK_DTBS=y` A10 target, and direct `dt-validate` passed for the GPIO keys and Samsung pin configuration schemas. Resulting A10 DTB SHA-256: `bb72f8b3769407d8aa2b61e2b057efc9a62328affea411ab9645174c9d208ab4`. The optional yamllint program was absent, so kernel tooling skipped that subcheck. No hardware input or wake test occurred.

Previously implemented A10 SD2/eMMC/UART2 stays as recorded in the port matrix. Reserved-memory, PMIC/regulators, thermal/charging, watchdog/RTC, USB, and stock boot compatibility remain unimplemented where exact upstream driver mappings are absent or ambiguous. No new full-tree `dtbs_check` or full project test suite was run in this Work workspace.

Artifact retrieval remains blocked at the previously documented private release asset download path; no alternate browser route was attempted. Exact Samsung-built Image, corrected initramfs, DTB/DTBO inputs needed for the host boot-v1 candidate remain unavailable here, so no boot image was regenerated or extracted. The explicit root path selector still waits for a measured physical partition number. No physical-device operation occurred.

Next: continue exact-source porting beyond keys (priority: memory intervals and remaining boot-critical subsystems), resume broader upstream diagnostics independently, and pursue authorized artifact retrieval without retrying the blocked browser route.
