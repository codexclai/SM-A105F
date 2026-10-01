## Current continuation — Exynos8 A10 RTC implementation (2026-10-01)

Added patch 0007, implementing the exact Samsung clockless Exynos8 RTC contract: a disabled shared Exynos7885 node with Samsung’s three IRQs, enabled only in the A10 DTS, plus a dedicated no-clock Linux 6.18 driver variant and compatible-specific binding constraints. Linux 6.18 uses the alarm IRQ only; periodic tick support is not claimed.

The RTC object compiled; binding check, dt-doc-validate, YAML parse, targeted A10 CHECK_DTBS, direct RTC-compatible dt-validate, and patch apply check passed. Decompiled output shows the expected compatible/reg/three IRQs/enabled status and no clocks. DTB is 21,982 bytes, SHA-256 `b021620dc042547ab3855c86e8e0f0b9598d8389f88e52787a1895482cd2998d`. See `docs/reports/linux-6.18.54-a10-rtc-implementation-20261001.md`.

The architecture-wide arm64 dtbs_check remains running with unrelated Rockchip/Qualcomm diagnostics and no final status; do not treat it as passed. The project Python regression suite has not been run in the Linux-only Colab runtime. No phone operation occurred.

---

## Existing reboot and poweroff description (2026-09-30)

Pinned Linux `1b357ecb321392158d507b04672ffee57bfa071d` already supplies the Exynos7885 SoC-level path: `arch/arm64/boot/dts/exynos/exynos7885.dtsi` includes `arch/arm/boot/dts/samsung/exynos-syscon-restart.dtsi`. That shared fragment adds `syscon-reboot` at PMU offset `0x0400` with legacy mask-only value `0x1`, and `syscon-poweroff` at offset `0x330c` (PS_HOLD_CONTROL) with legacy mask-only value `0x5200`. In the pinned `syscon-reboot.c` and `syscon-poweroff.c`, mask-only form is treated as the full-register value for compatibility; it is not converted into a bit mask. The A10 board tree inherits this existing SoC description, so no duplicate A10 node or patch was added. The fresh runtime had no kernel checkout for a new DTB/decompile check; these paths are upstream-source-mapped only and neither reboot nor poweroff has been physically validated on the phone.

---

## Regression replay from verified `main` (2026-09-30)

At source commit `dff28217beef5910218a6b2f62fb7c758542aed2`, the tracked Python unit suite and required project scripts/configuration were fetched through the authorized GitHub connector into a temporary Work scratch reconstruction. `python3 -m unittest discover -s tests -v` passed 33/33. `bash -n` on the rootfs/initramfs/test scripts, `sh -n` on both POSIX initramfs scripts, and `python3 -m py_compile scripts/*.py tests/*.py` also passed. This did not use the Colab terminal or constitute a full checkout/build; no artifact-dependent initramfs archive/QEMU test was run. The current Colab backend is fresh and has no project tree. Its retained broad-check cell failed because the expected directory/Makefile target was absent, so it is not a `dtbs_check` result. The existing Exynos-scoped check remains the validated DT result; architecture-wide `dtbs_check` remains incomplete. No physical-device operation occurred.

---

## Current continuation — Exynos-scoped DT validation and RTC research (2026-09-30)

Colab access is restored. The interrupted architecture-wide arm64 `dtbs_check` log shows all 21 Exynos-subtree DTBs, including A10, reached the `DTC [C]` schema-check stage before the process was terminated while compiling unrelated Freescale, MediaTek, Qualcomm, and Renesas targets. That broad run did not complete and has no successful aggregate exit status.

A fresh Exynos-scoped check on the pinned 6.18.54 tree (base `1b357ecb321392158d507b04672ffee57bfa071d`, watchdog patch 0006 applied; `.config` has `CONFIG_ARCH_EXYNOS=y`) rebuilt and checked all 21 Exynos DTBs with `CHECK_DTBS=1`. It exited 0 with no schema or dt-validate diagnostics. The exact target list and command are in `docs/reports/linux-6.18.54-a10-dtb-validation-20260929.md`. This closes the Exynos-wide validation gap but does not claim the full arm64 aggregate passed.

Two discarded setup retries were invocation issues only: `make -B` triggered a Kconfig “.config not found” failure, and an initial target list incorrectly included the DTS-tree prefix twice. The corrected relative target list passed; neither retry reported an A10 source or binding failure.

The pinned Linux 6.18 RTC binding/driver do not directly express the verified A10 clockless Exynos8 RTC contract. Continue exact-source RTC tracing and resolve the clock/IRQ/tick differences before proposing code. Root partition selection remains unresolved. No physical-device operation occurred.
---

## A10 eMMC and console host validation (2026-09-30)

The latest pinned Linux 6.18.54 A10 DTB was rebuilt and inspected. Host-side checks passed for the focused MMC binding, direct `dt-validate` (exit 0), and `dw_mmc-exynos.o` compilation. The DTB is 21,838 bytes with SHA-256 `655c29627e97c447b58ecbe66ac06d365a085e0147096c1d52293f99f727c52e`.

The compiled tree maps `mmc0` to `/soc@0/mmc@13500000`; that controller is enabled, non-removable, eight-bit, and carries the established conservative timing properties. The A10 `stdout-path` compiles to `/soc@0/serial@13820000`, whose UART node is enabled. This is host/build evidence and does not claim runtime console output.

The MMC alias establishes the controller index, not the handset's partition table. No measured root partition, root UUID/PARTUUID, or root kernel argument is available; root selection remains unresolved and must not be inferred from the eMMC controller. No physical-device operation occurred.

---

## Current continuation — fail-closed root selector (2026-09-30)

The committed resolver now rejects partition zero and leading-zero partition spellings such as `/dev/mmcblk0p0` and `/dev/mmcblk0p03`; these are not canonical Linux MMC partition device names. The committed selector regression covers both. The actual handset partition identity remains unmeasured and is not selected.

---

## Follow-up — initramfs/root-selector checks (2026-09-30)

Replayed root-selector acceptance/rejection cases in a temporary Colab harness with a resolver shim and checked shell syntax; the explicit path and rejected-path cases passed. This was a focused smoke check, not execution of the full project regression suite. The Colab project directory contains only the Linux checkout; Drive is not mounted, and the runtime has no `cpio`, `qemu-aarch64-static`, initramfs archive, or ARM64 BusyBox. Therefore archive extraction/readback and ARM64 BusyBox checks remain unrun. No root partition was inferred.

---

## Current continuation — 2026-09-30 (root-storage configuration)

Added a reusable Linux 6.18.54 A10 root-storage configuration fragment at `configs/linux/6.18.54/a10-root-storage.config`. In a clean worktree at pinned commit `1b357ecb321392158d507b04672ffee57bfa071d`, `defconfig` + `merge_config.sh` + `olddefconfig` resolved initramfs, devtmpfs, ext4, MMC block, DesignWare Exynos MMC, DOS/MBR and EFI/GPT parsing to enabled. The MMC controller objects and `fs/ext4/super.o` compiled for ARM64. This is configuration/object validation only; no full kernel link, handset root partition identity, mount, or boot was established. In particular, no `/dev/mmcblk0pN` is selected.

The ACPM/PMIC source trace found that pinned Linux ACPM/mailbox support assumes GS101 resources and a firmware-populated shared-memory ABI, while the ACPM PMIC MFD is S2MPG10-specific. A10's recorded S2MPU08 channel 2 is insufficient to prove resource, firmware, or wire-protocol compatibility. No PMIC support was added. Next: run initramfs archive/readback tests with verified test-only tooling where available. See `docs/reports/linux-6.18.54-a10-root-storage-config-20260930.md`.

---

## Current continuation — 2026-09-30 (Exynos7885 A10 watchdog)

Implemented Linux 6.18.54 support for the Exynos8 WDT1 using the evidence in `docs/reports/linux-6.18.54-a10-rtc-watchdog-review-20260929.md`. The new `patches/linux-6.18.54/0006-arm64-dts-exynos-add-a10-watchdog.patch` adds the Exynos8 compatible/variant, requires both clocks in the binding, adds a disabled shared Exynos7885 WDT1 node, and enables it only in the A10 DTS. It records PMU offsets 0x0408/0x040c/0x0404 and bit 24, but activates only PMU mask-reset and reset-status quirks; auto-disable and Exynos850/Exynos7 behavior are not enabled. Clock order is WDT1 PCLK then 26 MHz oscclk. Samsung IRQ <0 233 0> remains unspecified as IRQ_TYPE_NONE.

Against pinned Linux commit `1b357ecb321392158d507b04672ffee57bfa071d`, the driver object, `dt-doc-validate`, YAML lint (exit 0 with one line-length warning at existing line 23), `dt_binding_check`, A10-targeted `CHECK_DTBS=1`, direct `dt-validate`, patch reverse/apply round-trip, and `git diff --check` passed. The decompiled DTB contains the expected compatible, reg, IRQ, two named clocks, syscon, enabled status, and 30-second timeout. Size 21,838 bytes; SHA-256 `655c29627e97c447b58ecbe66ac06d365a085e0147096c1d52293f99f727c52e`. CodexCLI GPT-6 Luna High and a separate read-only reviewer found no substantive issue. These are host/build/schema results only; no device test occurred. The project-wide unit suite was not run because the Colab checkout contains only the Linux source tree and private Git transport is unavailable without credentials.

Next: resolve the ACPM/S2MPU08 contract before adding PMIC support. Linux 6.18.54's ACPM/mailbox compatible and firmware-facing shared-memory implementation are GS101-specific; its ACPM MFD client is S2MPG10-specific. A10 Samsung evidence records S2MPU08 on ACPM channel 2 and legacy `exynos_acpm_*_reg()` calls, but firmware handoff, shared-memory/ring layout, mailbox resources and ABI compatibility remain unverified. Inspect the exact Samsung Kernel archive in the existing Colab runtime or recover it through the recorded Drive chunks; do not copy GS101 resources or invent regulator rails.

---

## Current continuation — 2026-09-29 (Samsung source recovery)

Recovered the exact Samsung source ZIP from the existing three-part Drive copy using authorized raw streams and 8 MiB byte ranges. The reassembled 229,817,794-byte ZIP matches SHA-256 `5c83be7c2452d644ccda1deb898d9a54f2b3d53d3a0e66a7a394dcbf14439931`; ZIP integrity passes; embedded Kernel archive matches `e05288db460f2d0a0f86c79beac819066f4ea3baa57cf5f26b46cdf4ec3d0af2`. The durable copy is the existing three Drive chunks; this Work scratch copy is transient. Chunk IDs and recovery procedure are recorded in `docs/ARTIFACTS.md` and `docs/SOURCES.md`. No kernel source build was run: this runtime lacks cross-GCC/Clang/DT tools, and GitHub reports the existing Codespace out of budget. Phone untouched.

---

## Current continuation — 2026-09-29 (ABOX reservation clarification)

A re-read of the hash-verified Samsung 4.4.177 A10 overlay confirms that `exynos7884B-a10_common.dtsi` includes `exynos7884-rmem_7884.dtsi`, enables `&abox`, and defines its fixed `abox_rmem` at 0xE9400000/4 MiB. The inherited Exynos7885 DTS has an `abox_debug` child with `memory-region = <&abox_rmem>`. This resolves the ABOX reservation uncertainty: existing Linux 6.18 patch 0004's generic reg-only reservation is supported and should remain; the ABOX driver/audio function remain unported, and no `no-map`/reusable semantics are inferred. See the appended clarification in `docs/reports/linux-6.18.54-a10-rtc-watchdog-memory-review-20260929.md`. No kernel rebuild was possible in this Work runtime; the existing Codespace is stopped by its out-of-budget notice. Phone untouched.

---

# Current checkpoint — 2026-09-29 (A10 fixed clock and exact source recovery)

Starting from the preceding verified main `908d1e0ca0dceb643174150c8c5881f8055b76f5`, the exact Samsung source chunks were streamed from the existing Drive folder into the workspace and reassembled. The full 229,817,794-byte source ZIP matches SHA-256 `5c83be7c2452d644ccda1deb898d9a54f2b3d53d3a0e66a7a394dcbf14439931`; the embedded 202,050,103-byte `Kernel.tar.gz` matches `e05288db460f2d0a0f86c79beac819066f4ea3baa57cf5f26b46cdf4ec3d0af2`. ZIP integrity passed. These source archives remain workspace-only, not committed.

Exact A10 common DTS evidence sets `oscclk` to 26 MHz. Linux 6.18 uses a standard `fixed-clock`, so patch 0002 now applies that value in the A10 board DTS. The clean five-patch series applies in order to pinned Linux commit `1b357ecb321392158d507b04672ffee57bfa071d`, and the resulting DTS/schema match the tested tree byte-for-byte. The 21,587-byte A10 DTB SHA-256 is `44a77aa2c6ce133def05a8a4986181328c32962a4e7c564fdb2e24e7d6358166`. Focused binding build and focused plus unfiltered direct `dt-validate` are diagnostic-free. A fresh Exynos-enabled aggregate generated 20 arm64 DTBs with only the assembler `.inst` warning; no schema diagnostics or Kconfig prompt noise were logged. The earlier inherited fixed-clock warning is resolved.

Exact Samsung-built Image/initramfs and stock A10 DT/DTBO binaries are still unavailable, so no Android boot candidate was regenerated. The initramfs keeps explicit measured `/dev/mmcblk0pN` selection; no UUID/PARTUUID or partition discovery is guessed. Details: `docs/reports/linux-6.18.54-a10-dtb-validation-20260929.md`, `docs/reports/linux-6.18.54-a10-port-matrix-20260929.md`, and `docs/reports/artifact-retrieval-audit-20260929.md`.

Phone remains untouched; no physical operation occurred.

---

# Current checkpoint — 2026-09-29 (artifact stream boundary)

The preceding build/matrix checkpoint was verified at `a574c56fe0181596ed4bc0c3b7ea3cae671eb5cc`; this checkpoint then records the Drive recheck and transfer limit in subsequent commits. Drive recheck found no exact built Samsung kernel, corrected initramfs, or stock A10 DT/DTBO. The original three Samsung source ZIP chunks remain in Drive. A supported raw stream returned a reference for the 62,045,634-byte final chunk, but workspace transfer is rejected at the executor’s 32 MiB per-file limit; no partial file was created. Do not treat the source as active-workspace data until all chunks can be fetched and combined hash-verified in a larger existing environment. Details: `docs/reports/artifact-retrieval-audit-20260929.md`.

A10 DTB build/schema results and full Exynos aggregate diagnostics are recorded above. One unfiltered fixed-clock diagnostic remains unresolved pending exact Samsung clock source; no Jackpot LTE frequency was copied. Phone remains untouched.

---

# Current checkpoint — 2026-09-29 (clean pinned rebuild and Exynos aggregate)

Private `main` includes refreshed patch contexts for GPIO keys and fixed memory; the tracked A10 patch series now applies sequentially to clean Linux v6.18.54 commit `1b357ecb321392158d507b04672ffee57bfa071d`. Patch application was verified in a clean worktree, with final A10 DTS and schema byte-identical to the validated build tree. The malformed Colab Makefile target and temporary shared-DTSI timing edits were discarded.

The rebuilt A10 DTB is 21,555 bytes, SHA-256 `36f1effe96b5fa41912d1a06c604de8a97f5d5243527aa6cf689321e78bfa05f`. Focused five-schema binding validation, dt-doc-validate, yamllint, targeted CHECK_DTBS, and focused direct dt-validate passed. Unfiltered direct validation reports the one inherited Exynos7885 `osc-clock` missing `clock-frequency`; no value was guessed. Full Exynos-enabled aggregate generated 20 arm64 DTBs; log has that same schema diagnostic, assembler warning, and Kconfig restart prompt noise. It is recorded as completed with a diagnostic, not as a clean full-tree schema pass. Details: `docs/reports/linux-6.18.54-a10-dtb-validation-20260929.md`.

Next engineering work remains artifact retrieval and verified host candidate regeneration, subsystem implementation from exact Samsung semantics, and exact A105F bootloader/recovery/partition plus battery/charging/thermal research. Root selection remains explicit `/dev/mmcblk0pN`; UUID/PARTUUID and partition discovery are not guessed. No phone action occurred.

---

# Current checkpoint — 2026-09-29 (A10 board compatible and focused DTB validation)

Private `main` was at `88c9f18bfad1b7e1f22a5556f1c75e9a3a9edad0` after updating the A10 validation report. Patch 0001 now uses model-specific `samsung,sm-a105f`; patch 0004’s DTS context agrees; new patch 0005 registers that compatible in the Exynos7885 board schema. The schema change passed binding validation, A10 `CHECK_DTBS=y`, direct board-schema validation, and an equivalent schema patch reverse/apply round trip on the reconstructed tree.

Corrected A10 DTB: 21,555 bytes, SHA-256 `36f1effe96b5fa41912d1a06c604de8a97f5d5243527aa6cf689321e78bfa05f`. Full direct `dt-validate` now reports only the inherited Exynos7885 `osc-clock` missing required `clock-frequency`; that value is left unresolved pending exact A10 evidence. Focused MMC, UART, GPIO-key, and Samsung pinctrl checks remain clean. Full-tree `dtbs_check` is incomplete. Kconfig prompt output still appeared during target setup, though commands were isolated and returned 0; stabilize and save config for a reproducible build.

Drive has source ZIP parts and old Eureka artifacts but no exact 4.4.177 output bundle. GitHub release metadata confirms an older 12,118,381-byte candidate (`f28d6a293695ae6075123a4ed9af0a9c5f19b0f7fe6c125c98a71e87cfd98ae5`); the authorized connector here cannot retrieve private binary asset bytes. Candidate was not extracted or regenerated. A binary-capable authorized route is still needed for the round-trip checks.

Phone untouched. No physical-device action occurred.

---

# Current checkpoint — 2026-09-29 (pinned A10 DTB validation)

Private `main` was at `9b3639a08620e5e2dfa6be0d2f8d791b28f262e3` after adding `docs/reports/linux-6.18.54-a10-dtb-validation-20260929.md`. From clean upstream Linux v6.18.54 commit `1b357ecb321392158d507b04672ffee57bfa071d`, the recovered Colab edits were re-created with board timings kept in the board DTS, not the SoC DTSI. A10 DTB build and focused CHECK_DTBS/schema checks for MMC, UART, GPIO keys, and Samsung pinctrl returned 0; direct per-schema dt-validate was clean. DTB: 21,563 bytes, SHA-256 `3e059201353c87f4c310109f83f9bec8bbd4fcff3bcbb69057223d6031663549`.

Full direct dt-validate reports the root legacy marketing string is not an accepted DT compatible and inherited `osc-clock` lacks required `clock-frequency`. The reserved-memory path in this tree is text documentation rather than a YAML schema; no reserved-memory diagnostic appeared. Do not guess or suppress these. First build invocation emitted Kconfig prompts before succeeding; rerun from a fresh pinned checkout with configuration stabilized for reproducible logs. Full-tree dtbs_check remains unresolved and separate.

Drive contains original Samsung source ZIP parts, prior Eureka bundles, and a checkpoint, but no matching exact 4.4.177 output bundle. GitHub release metadata confirms a prior 12,118,381-byte host-only boot candidate (SHA-256 `f28d6a293695ae6075123a4ed9af0a9c5f19b0f7fe6c125c98a71e87cfd98ae5`); the available connector cannot retrieve its private binary bytes. No candidate extraction/regeneration was done, and no artifact was treated as verified from metadata alone. Continue via an approved binary-capable route and validate hashes before reuse.

Phone untouched. No physical-device operation was performed or authorized.

---

# Current checkpoint — 2026-09-29 (A10 source milestone preserved; aggregate log unavailable)

Private `main` was verified at `11c904b0d427111cabaeb8ca8f2ad963977fffc3` before this checkpoint update. The initramfs root resolver load defect is fixed and covered by source/archive assertions; fail-closed root discovery is documented. Reconstructed offline tests from remote main pass 33/33. Full archive/QEMU validation remains blocked on missing verified ARM64 BusyBox/archive binaries.

A pinned Linux 6.18.54 full-tree `dtbs_check` was running in Colab at the last saved observation (25m09s, output buffered). This runtime’s browser is signed out and the Colab page now reports “You’re not signed in” / “Your session ended because there was no activity.” The aggregate log cannot currently be retrieved; completion and diagnostics are unknown. Keep its result unclaimed. The A10 GPIO-key and fixed-reserved-memory patches are already committed in private main and their separate focused validations are recorded in their patch/review evidence. Re-run the aggregate check only when a kernel tree/runtime is available, then capture its actual output.

Exact Samsung-built kernel, corrected initramfs and matching stock A10 DTB/DTBO remain unavailable through audited sources. No host boot-v1 image was regenerated. Bootloader acceptance, DTBO selector, signing/rollback and exact partition-capacity evidence remain unresolved. Phone remains untouched.

Next: recover an authorized active Linux build runtime or source tree; run focused combined A10 checks and capture aggregate diagnostics; continue source-backed platform work and artifact retrieval. No physical-device action is authorized or performed.
---

# Current checkpoint — 2026-09-29 (initramfs resolver fix and offline tests)

Remote `main` was verified at `8e5cc3d8dc9c605286e57cbb17556223cb5f0fa6` before this checkpoint update. The initramfs `/init` previously called root resolver functions without sourcing staged `/lib/root-device.sh`; it now loads the helper before root selection. The archive test checks this source statement and requires extracted `/init` to match source. Review: `docs/reports/initramfs-root-helper-fix-20260929.md`.

The current repository's offline Python tests were fetched from authorized GitHub `main` and run in a reconstructed workspace: 33/33 passed, including explicit eMMC root selection. Script Python compilation, Bash syntax, POSIX init/resolver syntax and the selector shell test passed. The artifact-dependent `tests/test_a105f_initramfs.sh` was not run: no verified ARM64 static BusyBox or corrected archive is available. No initramfs binary hash or bootability claim is made.

Root discovery assessment recommends explicit `root=/dev/mmcblk0pN` rather than guessing UUID/PARTUUID or scanning partitions. A future discovery implementation would require a paired installation marker, eMMC-only read-only/no-journal probes, exact-one-match rule and fail-closed behavior; it is not implemented. See `docs/reports/root-device-discovery-assessment-20260929.md`.

The subsystem matrix and exact-source reports cover fixed RAM reservations, GPIO keys, eMMC/UART, RTC/watchdog, S2MPU08/rails, USB DRD/PHY and battery/thermal. No unsafe DTS-only mappings were added for PMIC, RTC/watchdog or USB. A full-tree `dtbs_check` is still running in the pinned Linux 6.18.54 Colab checkout at last observation (17m18s); output remains buffered until it completes, so no real diagnostics have yet been captured. Previous focused A10 MMC/UART schema validations remain separate.

Exact Samsung-built kernel, corrected initramfs binary and matching stock A10 DTB/DTBO binaries remain unavailable through audited local/Drive/GitHub routes. Do not regenerate Android boot-v1 until verified inputs are present. Ramdisk load address remains community-derived; bootloader acceptance, DTBO selector semantics, AVB/footer/rollback and exact partition capacities remain unresolved. Phone remains untouched.

Next: capture full-tree check diagnostics if it completes, and keep advancing independent Linux 6.18 port work. No physical-device operation is authorized or performed.

---

# Current checkpoint — 2026-09-29 (initramfs resolver loading and root discovery assessment)

Remote `main` was verified at `2075cbffba8868d0e449fed11abd1426e43819fb` before this status update. The initramfs `/init` previously called root resolver functions without sourcing staged `/lib/root-device.sh`; it now sources the helper before root selection. The archive test checks this source statement and requires extracted `/init` to match the source file. See `docs/reports/initramfs-root-helper-fix-20260929.md`.

Readback checks passed: POSIX shell syntax for init/resolver, Bash syntax for both initramfs and selector tests, and explicit eMMC path selector tests. The full ARM64 archive/QEMU test remains unrun because no verified static BusyBox/archive is present. Root discovery assessment recommends retaining explicit `root=/dev/mmcblk0pN`: no UUID/PARTUUID or partition number is guessed. A future scan would require a paired installation marker, read-only/no-journal probe, exact-one-match rule and fail-closed behavior; it is not implemented. See `docs/reports/root-device-discovery-assessment-20260929.md`.

The subsystem matrix and exact-source reports cover fixed RAM reservations, GPIO keys, eMMC/UART, RTC/watchdog, S2MPU08/rails, USB DRD/PHY and battery/thermal. No unsafe DTS-only mappings were added for PMIC, RTC/watchdog or USB. A full-tree `dtbs_check` is still running in the pinned Linux 6.18.54 Colab checkout at last observation (13m28s); the command captures output until completion, so there are no real diagnostics captured yet. Prior focused A10 MMC/UART schema validation remains separate.

Exact Samsung-built kernel, corrected initramfs binary and matching stock A10 DTB/DTBO binaries remain unavailable through the audited local/Drive/GitHub routes. Do not regenerate the Android boot-v1 candidate until verified inputs are present. The ramdisk load address remains community-derived; bootloader acceptance, DTBO selector semantics, AVB/footer/rollback and exact partition capacities remain unresolved. Phone remains untouched.

Next: capture the full-tree check result if it completes, while preserving the focused A10 work. Continue independent exact binary acquisition and source-to-upstream port mapping. No physical-device operation is authorized or performed.

---

# Current checkpoint — 2026-09-29 (initramfs root-selection path fixed)

Remote `main` was verified at `34b56921898172f5d99f845db9a7810b5b0cca8f` before this checkpoint update. The initramfs `/init` previously called root resolver functions without sourcing the staged `/lib/root-device.sh`. It now sources the helper before root selection. The archive test asserts the source line and requires extracted `/init` to match its source. Evidence is in `docs/reports/initramfs-root-helper-fix-20260929.md`.

Validation against files read back from remote `main`: `sh -n` passed for init and resolver; `bash -n` passed for both test scripts; `tests/test_root_device_selector.sh` passed, allowing only an explicitly supplied `/dev/mmcblk0pN` and rejecting UUID/PARTUUID guesses and all other devices. Full archive/QEMU validation is still blocked by the absent verified ARM64 static BusyBox and corrected archive. No binary hash or bootability claim is made.

The subsystem matrix and exact-source reports now cover fixed RAM reservations, GPIO keys, eMMC/UART, RTC/watchdog, S2MPU08/rails, USB DRD/PHY and battery/thermal. No unsafe DTS-only mappings were added for PMIC, RTC/watchdog or USB. A full-tree `dtbs_check` is running in the pinned Linux 6.18.54 Colab checkout; the last observation was 7m26s with no captured diagnostics yet. Existing focused A10 MMC/UART checks remain distinct from that full-tree run.

Exact Samsung-built kernel, corrected initramfs binary, and matching stock A10 DTB/DTBO binaries remain unavailable through the audited local/Drive/GitHub routes. Do not regenerate the Android boot-v1 candidate until verified inputs are present. Ramdisk load address remains community-derived; bootloader acceptance, DTBO selector semantics, AVB/footer/rollback and exact partition capacities remain unresolved. Phone remains untouched.

Next: capture the full-tree check result if it finishes; otherwise stop the slow aggregate check only after focused A10 state is preserved, then advance the highest-supported independent port slice. Continue the exact binary acquisition and boot-chain evidence work without physical-device actions.

---

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


## 2026-09-29 — USB DRD/PHY support gap

The exact A10 USB glue and PHY drivers were traced against Linux 6.18.54; evidence and hashes are in `docs/reports/linux-6.18.54-a10-usb-drd-review-20260929.md`. The A10 glue/PHY compatibles, Exynos7885 50 MHz reference behavior, multi-region PHY, five clocks, PMU isolation and custom calibration are not represented by a matching upstream glue/PHY binding/driver data set. USB remains disabled; no sibling SoC compatible was substituted.


## 2026-09-29 — Boot-v1 and DT selector evidence reconciliation

Documented the exact CWB3 candidate header and separate DT/DTBO table facts, plus remaining footer/signing, AVB, selector, capacity, rollback and recovery unknowns in `docs/BOOT_PACKAGING.md`. The measured stock header has no ramdisk; the candidate 0x11000000 ramdisk address remains community-derived. The former host candidate embeds an older initramfs and is not the corrected candidate. No artifact was regenerated, and no phone action occurred.


---

## Current continuation — 2026-09-29 (exact watchdog source verification)

The three authorized Samsung source archive chunks were fetched through Drive's scoped raw streams into the Colab runtime, concatenated, and verified at 229,817,794 bytes with SHA-256 `5c83be7c2452d644ccda1deb898d9a54f2b3d53d3a0e66a7a394dcbf14439931`. Extracted `drivers/watchdog/s3c2410_wdt.c` matches the recorded Samsung-file SHA-256. Exact Exynos8 semantics are now recorded in `docs/reports/linux-6.18.54-a10-rtc-watchdog-review-20260929.md`: PMU offsets 0x0408/0x040c/0x0404, bit 24, only PMU mask-reset and PMU reset-status quirks, reset-status label A53 WDTRESET; old clock names map to OSCCLK at 26 MHz and WDT1 PCLK in modern Linux. No adjacent Exynos variant bits/quirks were copied.

**Implementation remains pending:** no Linux 6.18 driver, binding, or A10 DTS patch was completed or validated in this continuation. Do not describe the watchdog as supported. Next step is the narrow upstream-style Exynos8 extension with two clocks, PMU syscon and a disabled SoC watchdog node enabled only in the A10 DTS; run the watchdog binding and DT checks plus the driver object compile. Continue immediately into the evidence-backed PMIC/regulator boot path gap after that. The phone remains untouched; no flashing or other device operation occurred.


## Compiled A10 restart, poweroff, and RTC path review (2026-09-30)

The rebuilt A10 DTB decompiles with the inherited Exynos7885 syscon poweroff at PMU offset 0x330c/mask 0x5200 and syscon reboot at offset 0x0400/mask 0x01. These are SoC-level nodes from the existing shared Exynos restart fragment; no duplicate A10 node was added. This verifies compiled DT representation, not handset restart/poweroff operation.

The pinned Linux 6.18.54 rtc-s3c.c probe unconditionally acquires the named rtc clock and requests only platform IRQ index 0. Exact Samsung A10 evidence describes a clockless Exynos8 RTC with three IRQs and Exynos8-specific data. A compatible-only alias would therefore misdescribe both the clock and interrupt contract. Preserve the blocker until a deliberate driver/binding translation establishes which interrupts and enable/clock semantics modern Linux must implement. The PMIC RTC remains dependent on S2MPU08 support.

## Current continuation — reset configuration and PMIC upstream comparison (2026-09-30)

Pinned Linux 6.18.54 source confirms the existing Exynos reset and poweroff nodes use the generic `syscon-reboot` and `syscon-poweroff` bindings/drivers. The stock arm64 `defconfig` already enables `CONFIG_POWER_RESET_SYSCON`, `CONFIG_POWER_RESET_SYSCON_POWEROFF`, `CONFIG_WATCHDOG`, and `CONFIG_S3C2410_WATCHDOG`; the active validation config has them enabled too. No separate boot-control config fragment is needed. The source-level DT description is already inherited from the shared Exynos7885 tree; runtime reset and poweroff remain untested.

A targeted search of the pinned upstream tree found ACPM MFD support for S2MPG10, including its regulator, RTC, meter, clock, and GPIO children, but no S2MPU08 match or binding. Existing Samsung A10 evidence records S2MPU08 on ACPM channel 2; it does not establish that the upstream S2MPG10 ABI/resources or register tables apply. No PMIC driver or DT translation was added. The exact missing evidence remains the Samsung ACPM firmware/mailbox transport contract and S2MPU08 register/rail mapping needed to select a safe upstream implementation.

The architecture-wide arm64 `dtbs_check` is still running in Colab against the pinned tree with `CONFIG_ARCH_EXYNOS=y`; current log diagnostics are from unrelated upstream Freescale, MediaTek, and Qualcomm DTs. No make failure marker or A10-specific diagnostic has appeared so far. This is a live, incomplete run and has no final exit status yet. The separate A10 targeted `CHECK_DTBS=1` build and direct `dt-validate` remain the applicable A10 validation evidence.


## 2026-09-30 — arm64 dtbs_check progress snapshot

The all-arm64 run is still active in Colab at the Linux 6.18.54 pin. Exact command: `PATH=/content/work/dtschema-venv/bin:$PATH make -j2 ARCH=arm64 dtbs_check`, with output redirected to `/content/work/arm64-dtbs-check.log`. Configuration has `CONFIG_ARCH_EXYNOS=y` and `CONFIG_S3C2410_WATCHDOG=y`; `.config` SHA-256 is `c91f12ee48b24734246afb03dd5a357c23d4ba0a0d7be6dc5d3dffb8c90006e5`. Tool versions: DTC 1.7.0 and dtschema/dt-validate 2026.9.

At the latest observation (process elapsed 1:04:47), the log contained 6,771 lines and 1,933 `from schema $id` diagnostics. The make-level failure-marker scan returned 0; the log contains no `exynos7885-a10.dtb` match and no A10-specific diagnostic. Observed schema notices are from other arm64 platforms (including Marvell, NVIDIA, Freescale, MediaTek, Renesas, Qualcomm, Broadcom, and HiSilicon); they are not A10 findings. Because the A10 target was not emitted in this incremental global run, the separate all-21-Exynos `CHECK_DTBS=1` pass remains the relevant A10/Exynos validation. The global run has no final exit status yet and is not claimed as passed.

A concurrent reset/poweroff object-build attempt was interrupted before compilation because Kbuild entered interactive `syncconfig` and prompted for new ARM64 symbols (BTI, E0PD, MTE). No driver-object result is claimed. After the global DT build ends, run `olddefconfig` noninteractively, then retry the two objects and record their actual status.
