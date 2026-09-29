# Current checkpoint — 2026-09-29 (artifact stream boundary)

Private `main` verified at `a574c56fe0181596ed4bc0c3b7ea3cae671eb5cc` after refreshing the subsystem matrix’s root handoff and latest A10 validation state. Drive recheck found no exact built Samsung kernel, corrected initramfs, or stock A10 DT/DTBO. The original three Samsung source ZIP chunks remain in Drive. A supported raw stream returned a reference for the 62,045,634-byte final chunk, but workspace transfer is rejected at the executor’s 32 MiB per-file limit; no partial file was created. Do not treat the source as active-workspace data until all chunks can be fetched and combined hash-verified in a larger existing environment. Details: `docs/reports/artifact-retrieval-audit-20260929.md`.

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
