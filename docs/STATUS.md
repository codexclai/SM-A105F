# Current checkpoint — 2026-09-29 (explicit root path and artifact retrieval)

This checkpoint is based on private `main` at `8430230fa7377de3f6b89b462bec4d248ec9c4d2`. The initramfs root selector now accepts only an explicitly supplied `/dev/mmcblk0pN` path and rejects UUID/PARTUUID, other disks, whole-device paths, malformed suffixes, and path traversal. The exact partition number must be measured later; the initramfs contains no enumeration or auto-selection. Two focused tests passed, along with separate POSIX shell and Bash syntax checks.

Release inspection found only the existing draft host-only boot-v1 archive (`SM-A105F-host-only-boot-candidate-20260928.tar.gz`, recorded SHA-256 `f28d6a293695ae6075123a4ed9af0a9c5f19b0f7fe6c125c98a71e87cfd98ae5`, about 11.6 MiB). The authenticated browser showed the asset metadata, but the actual download action was blocked by the browser URL policy. Do not retry through alternate browser paths. GitHub Actions has zero workflow runs and its connector does not provide release asset binaries. The exact Samsung-built Image, corrected initramfs, DTB/DTBO remain unavailable in this runtime. No candidate was regenerated or extracted.

Battery review confirms Samsung 4.4 kernel-side temperature/swelling limits, OVP/UVLO response, and charger current/voltage control, all dependent on unsupported board-specific PMIC/ADC callbacks. Linux 6.18 has no `samsung,exynos7885-tmu` match. Exact report: `docs/reports/linux-6.18.54-a10-battery-thermal-review-20260929.md`. No thermal/charging DTS nodes were enabled.

The SD2/eMMC/UART2 A10 DTS validation at 6.18.54 remains the last DTB build; no DTS change occurred in these root/power reviews. No full-tree `dtbs_check` or complete project suite ran here. No physical-device operation occurred.

Next: continue sourcing existing exact binaries from authorized sources without bypassing the browser policy, and advance thermal/charger/PMIC mappings only with driver-level evidence. Physical root selection stays deferred until the partition is measured.
