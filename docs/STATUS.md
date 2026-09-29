# Current checkpoint — 2026-09-29

## Latest verified state

- Remote private `main` was verified through the GitHub branch API at `7bd0d2cb5998ca76f4fa9cb72ea2e86ca47e44a3` before this checkpoint edit. This revision includes the Android boot-v1 section extractor and its test suite, plus the engineering checkpoint linked from `START_HERE.md`.
- The new `scripts/extract_android_boot_sections.py` validates v1 section bounds/alignment, extracts payloads, generates per-section SHA-256 manifest data, and can compare extracted kernel/ramdisk against exact input files. The complete tracked Python suite passed 23/23 in a local reconstruction of the verified GitHub tree; `py_compile` and `bash -n` passed for tracked Python scripts/tests and rootfs/initramfs builders.
- The existing private draft release `a105f-host-only-candidate-20260928` has an asset of 12,118,381 bytes. GitHub's current asset digest is `f28d6a293695ae6075123a4ed9af0a9c5f19b0f7fe6c125c98a71e87cfd98ae5`, which differs from the older continuation handoff's bundle digest. Release metadata alone does not verify its internal payloads. This session did not rebuild or read back the binary artifact; do not supersede the old candidate until the actual bundle, corrected initramfs, kernel, and DT/DTBO bytes are available together for round-trip checks.
- Upstream Linux `bf1aee1ad1c087ffda617207890dc92042a28c96` exposes Exynos7885 `mmc_0` and `serial_2`; the A8 sibling DTS enables its eMMC in 8-bit HS200/HS400 mode. A pinned A10 Linux 4.4.111 community source mirror corroborates A10 downstream `dwmmc_0` as 8-bit eMMC, `dwmmc_2` as removable 4-bit SD, `serial_2`, volume/power keys, and downstream USB OTG. These are porting comparisons, not proof of the installed handset or a Linux 6.18.54 board build. No A10 DTS patch or DTB was compiled in this session.
- The Codespace was not reachable from this Work runtime: its browser tab redirected to GitHub login, and a separate remote desktop device was offline. GitHub connector access still allowed source reads and repository commits. No credentials or human verification were attempted.
- Physical phone remains untouched. No flash, boot, Download Mode, partition read, or other device operation occurred.

See [engineering checkpoint 2026-09-29](engineering-20260929.md) for method, source pins, artifact limitations, and exact next tasks.

---

# Current checkpoint — 2026-09-27

## Latest verified continuation — 2026-09-27 UTC

- Before these documentation edits, live private GitHub main and the existing Codespace checkout were aligned at 920cc8edcf2d57ea796660ade4944d01d3669500; the worktree was clean. This continuation adds newer evidence above the historical checkpoints below.
- The user-supplied Samsung source ZIP is present in this conversation upload. Its SHA-256 is 5c83be7c2452d644ccda1deb898d9a54f2b3d53d3a0e66a7a394dcbf14439931. The extracted Kernel.tar.gz SHA-256 i6.18s e05288db460f2d0a0f86c79beac819066f4ea3baa57cf5f26b46cdf4ec3d0af2. Codespace work/ has only part-00 (33,554,432 bytes; SHA-256 9d2a1f893c8878182ce408da2104c8a61068a08abc6c2c572d83f433c5e98588), matching local part-00 exactly. The remaining six chunks were not transferred; a 1 MiB test upload hit a Codespaces file-chooser backend error. No reconstruction or Samsung 4.4.177 build has occurred.
- Two distinct 196,298,240-byte Debian 13.7 ARM64 archives exist: the preserved artifact at work/artifacts/rootfs/debian-trixie-arm64-rootfs.tar (SHA-256 67ba3022d06670799eb4a3d51d9897655bd1641835e346bf8c6126ed9471f975), matching its recorded sidecar, and the ignored candidate work/debian-trixie-arm64-minbase.tar (SHA-256 a69837bfdffded1e15c8e4e48097506033709e4f945c635acb835042f7838cab), matching its sidecar. They are not hash duplicates; both report 117 installed package records and their dpkg status members have the same SHA-256. Exact tar comparison of the extracted verification tree succeeded against the minbase candidate and not the older preserved TAR.
- QEMU user-mode execution against the exact minbase extraction succeeded for ARM64 Bash 5.2.37, dpkg/dpkg-query 1.22.22, apt 3.0.3, and systemd 257. The expected init/systemd, fstab, dev, proc, sys, run, and dpkg status paths exist. This validates basic userspace execution and archive extraction only; there has been no QEMU system boot, kernel/rootfs integration, initramfs, boot image, or phone test.
- The repository unit suite passed 17/17 tests. The phone remains untouched. Next: resolve a supported Codespaces transfer path for the remaining source chunks, verify reconstructed archive SHA-256, then build the supplied 4.4.177 source with the staged toolchain.


- Live private GitHub `main` was independently read at `b5f74dd950c3332ec3c67e317b8b142e60158378` before this update; this checkpoint is based on that live tree.
- GitHub evidence now includes a Samsung A10 Linux 4.4.111 source mirror with ARM64 A10 defconfig/SWA DTS, and a commit-pinned SM-A105F TWRP tree tied to product fingerprint D9CWD2. The tree specifies Android boot header v1, 2048-byte page size, base/offset values, and separate dtb/dtbo partition names. Its prebuilt DTBO was parsed and identified as one `A10 SWA OPEN 00` overlay.
- Added and tested `scripts/inspect_android_dtbo.py`; 5/5 tests pass. The real community prebuilt parses with expected table header and metadata.
- Exact stock AP firmware is still absent. Eureka and TWRP build recipes conflict on configured boot-image limit (36 MiB vs 53 MiB), and no stock boot header, ramdisk provenance, kernel payload encoding, actual partition size, or handset overlay choice is verified.
- Eureka Linux 4.4.302-p6 host build remains the nearer hardware path. Upstream 6.x still lacks A10 DTS; the Samsung A10 vendor DTS has now been located as a porting reference. No new kernel/boot build ran here because the Codespace terminal was unavailable. No phone action occurred.
- Next gate: inspect the handset-matching AP archive (candidate clue only: A105FDDS9CWD2) or extracted `boot.img`, `dtb.img`, `dtbo.img`; only then determine exact packaging. Keep phone untouched.

# Resumption checkpoint — 2026-09-27 Asia/Colombo

GitHub connector readback verifies the canonical private `main` at `54a6388c24a792e1cde4d1a376ff4bc804bd1cc8`. The attached `upload/Chat-0.json` is available in this conversation and contains 107 user messages; it was inspected for user decisions. Current repo authority notes preserve the key decisions: continue the existing private repository, do not resume tmate/SSHx, leave the physical phone untouched absent specific informed approval, and avoid arbitrary readiness percentages.

The rootfs TAR is present as a private draft prerelease asset, not merely in Codespace `/tmp`: release metadata reports 196,298,240 bytes and SHA-256 `67ba3022d06670799eb4a3d51d9897655bd1641835e346bf8c6126ed9471f975`; the Drive checkpoint records a fresh Codespace retrieval that matched byte-for-byte. It remains an unprovisioned host-built TAR, not bootable or device-tested. Keep the recovery copy until a new live inventory verifies durable retrieval.

This session has GitHub and Drive connectors but no live Codespace terminal/filesystem access. The reported Eureka compilation-in-progress state in the handoff is therefore unverified here; do not mark it complete until checking the actual process/logs and outputs in Codespace. No build, QEMU boot, or device operation was run in this session. Next: reconnect to the authorized Codespace, verify its branch/worktree and whether the reported single-job kernel build is still running or finished, preserve its full log, validate outputs if complete, then resume rootfs host-side checks and the separate modern-kernel investigation.

---

# Authoritative project checkpoint

Updated: 2026-09-26 UTC after reading the attached collaboration export and rechecking the Codespace rootfs.

## Verified synchronization and continuity

- Canonical repository: private `thamindudenuwarajayasinghe/SM-A105F`, default branch `main`. At the start of this work GitHub `main` was `5166d9da6f585d1bf98d868b17ff20d7bc81d925`; the open Codespace Source Control graph showed `main` and `origin/main` at the same latest commit with no listed changes. Verify again on resume.
- The attached `Chat-0.json` was found in this conversation, not Drive or the repository. It contains 107 user messages. Material decisions have been reconciled here and in the current-authority block at the top of `Prompt.md`. Secrets and irrelevant personal conversation were excluded.
- The earlier bootstrap's public-repository/fresh-start instructions were superseded by the user's later direction to continue the existing private repository. The user canceled tmate/SSHx sharing; do not resume those attempts. The phone remains untouched. Do not substitute arbitrary percentages for subsystem evidence.
- The separate local checkout outside the writable workspace was not read or synchronized in this session. Do not claim it is current.

## Rootfs: found, hashed, copied, statically inventoried

- Original: Codespace `/tmp/SM-A105F/debian-trixie-arm64-rootfs.tar`, root-owned. It was not missing; ordinary shell access to its parent was denied. Its SHA-256 was verified as `67ba3022d06670799eb4a3d51d9897655bd1641835e346bf8c6126ed9471f975` and size as 196,298,240 bytes. This matches the previous build record.
- Recovery copy: `/workspaces/SM-A105F/work/artifacts/rootfs/debian-trixie-arm64-rootfs.tar`, under ignored Codespace workspace storage, with matching `.sha256` sidecar. The sidecar value and a fresh hash of the copy match. The copy is protected against ordinary Codespace stop/start, but not Codespace deletion/rebuild; it is not yet in Drive or GitHub. A Drive search for the project Trixie ARM64 rootfs returned no result.
- Read-only TAR inspection succeeded: 8,406 entries, including package database and pseudo-filesystem paths. The dpkg status database contains 117 package records, including installed ARM64 `systemd-sysv`, `openssh-server`, `iproute2`, and `ca-certificates`. The inspected package names showed no Xorg, GNOME, KDE, Plasma, or XFCE stack. This is host-side archive evidence, not a chroot/systemd runtime test. Recheck `/etc/os-release`, every installed package architecture, ownership/modes, and resolver defaults before calling validation complete.
- Codespace has `/usr/bin/mmdebstrap`, `/usr/bin/qemu-aarch64-static`, working noninteractive sudo, and about 18 GiB available on the workspace filesystem. No Debian rebuild was needed because the checksum-matching archive survived. No new packages were installed and no QEMU system boot was performed.

## Kernel and device status

- Eureka `R24U` / Linux `4.4.302-p6` remains an experimental vendor/community reference with host-build evidence only. It is not established as the final kernel.
- Keep a modern mainline-forward track active. Previous bounded upstream/community scans found generic Exynos7885 support but no exact SM-A105F board port; recheck current upstream/LTS sources and enumerate missing device-specific functions before kernel selection.
- The candidate config has `CONFIG_USER_NS` unset, `CONFIG_CGROUP_PIDS` unset, and `CONFIG_MEMCG=y`. These settings do not establish service resource-limit enforcement. Do not enable user namespaces or claim cgroup runtime behavior without a focused security/configuration/runtime assessment.
- Exact official Samsung source bytes and stock firmware for `SM-A105F / SLK / A105FDDS9CWB3` remain unacquired. No QEMU boot or physical-phone test occurred. The phone remains untouched.

## Next engineering actions

1. Establish a supported transfer/upload path to put the 196 MB rootfs and sidecar in private durable artifact storage; verify metadata, retrieved bytes, and SHA-256 before removing or replacing any copy.
2. Complete non-extracting rootfs validation (release identity, package architectures/status, expected init and services, pseudo-filesystem entries, ownership/modes, resolver/source defaults, absence of desktop packages). Then create a concise manifest and reproducible build record.
3. Continue executable 4.4 config/compatibility checks and the modern-kernel device-support investigation as separate tracks. Inspect the Eureka checkout's exact dirty DTS/symlink state before any restoration or cleanup; preserve evidence.
4. Continue legitimate official Samsung source/firmware acquisition and static boot-chain mapping. No physical action without a specific informed test plan and approval.

---

Historical snapshots follow; their live hashes, estimates, and process state are superseded by this checkpoint and later dated journal entries.
 their live hashes, estimates, and process state are superseded by this checkpoint and later dated journal entries.




## Resume reconciliation — 2026-09-26

- Live GitHub API check: private repository `thamindudenuwarajayasinghe/SM-A105F`, default branch `main`, commit `65dd75c009809cfa1177d8151074172dff145345`, tree `121a98c861489706b2d4e15c5c364321e84464ed`. The local scratch checkout is a different historical line: branch `main`, `HEAD` `5aee00f1c69cca636a0374c4ce3e19a8bb427bab`, tree `c3ec1446643781257cf045138734d978da4425fe0`; its visible working tree is clean, while ignored `work/` and `reference/` contain approximately 968 MiB and 1.1 GiB. Its `origin/main` tracking ref is stale at `e7ae611c2cb2708bc10ef2f85baeb6c59dcacc34`, and the live commit object is not present locally. Do not reset, merge, push, or replace this snapshot blindly; the remote branch is authoritative and this divergence requires file-level reconciliation. The local repository is not synchronized with the live remote.
- The ignored Eureka checkout `reference/inputs/eureka-r24u` identifies upstream commit `e1b8464bb29ce5bcb9d52bfcfc71bc2563e12563` and branch `R24U`, but currently has two deleted tracked symlinks: `arch/arm64/boot/dts/exynos/dtbo/exynos7885-ecd.dtsi` → `../dtb/exynos7885-ecd.dtsi` and `drivers/kernelsu` → `../KernelSU/kernel`. Both targets exist. No current-session edit was made; the reason for their disappearance is unknown and process inventory could not be checked because `/proc` is unavailable in this runner.
- Current host checks rerun: `python3 -m unittest discover -s tests -v` passed both synthetic archive tests; `python3 -m py_compile scripts/inventory-archive.py`, `bash -n scripts/build-rootfs.sh scripts/configure-eureka-a10.sh`, and `git diff --check` passed. The current command lookup finds none of `mmdebstrap`, `debootstrap`, `qemu-aarch64-static`, `aarch64-linux-gnu-gcc`, or `qemu-system-aarch64`; no rootfs was built.
- Persisted KSU-disabled kernel candidate was fetched again from Drive file ID `1Vqzn_d3MWrXIJawOFevk748EKOWLoG7o` into this session. Size is 25,899,371 bytes; SHA-256 `78594b207d6c526fdb2a6e007fefedda8ae66c6a228609694a4d6852302bf8d8`; all 15 payloads listed in the archive's `SHA256SUMS` match. Drive metadata and folder listing show the file remains owner-only/not shared in the project folder. This verifies artifact retrieval/integrity, not kernel runtime or device support.
- Progress estimate: approximately **12%** of the full native-device engineering/acceptance scope, using an informal milestone-weighted estimate. Repository/process continuity and experimental host kernel outputs exist; exact stock inputs, a rootfs, boot integration, phone boot, hardware operation, recovery, and safety/reliability validation do not. Production readiness remains **0%**; the device is untouched.
- The user reported being active at about 09:05 Asia/Colombo on 2026-09-26 and asked for phone contact only if genuinely needed. No decision or physical action was needed in this reconciliation, and no ring was made.

Updated: 2026-09-26 UTC, after live repository/artifact reconciliation and rerun host checks.

## Identity and synchronization

- Objective: genuine native Debian 13 Trixie ARM64 for Samsung Galaxy A10 **SM-A105F**, minimal/headless/CLI-first. Debian 13.7 is officially available: Debian's release page says it was published 2026-09-12 ([release page](https://www.debian.org/releases/), [13.7 announcement](https://www.debian.org/News/2026/20260912)). Build from verified Trixie repositories at build time and continue security updates; do not freeze the system at a point-release snapshot.
- Canonical repository: [thamindudenuwarajayasinghe/SM-A105F](https://github.com/thamindudenuwarajayasinghe/SM-A105F). Verified live through GitHub connector on 2026-09-25: repository private, default branch `main`, the most recent independently verified `main` before this checkpoint-only follow-up was `c6148bede1adc1d6d3d1a4ba467ba67debaa2b87` (tree `55bbdd2276772285a72b2511e9a1468fd0a37110`), containing the kernel source scan and compatibility audit. Repository visibility remained private. Always re-read the actual branch head before resuming.
- Local `/workspace/scratch/4d6756134406/SM-A105F` was on branch `main`, `HEAD` `389c3bc8b7c5d5743859fd3f426a95ab743877fc`, tree `8b3ed0a90f69509cb3c7ce0301d190ffba1926f0` before this session's documentation changes; at that point its tree matched the then-live remote. The executor disconnected while applying those changes, so current local index/worktree state is unknown. Reconcile it against the live remote before editing. Shell Git has no remote push credentials; use the verified GitHub connector. Local and remote commit ancestries differ. Do not force-push, reset or mechanically merge.
- Original full first prompt remains intact in `Prompt.md` (original prompt-only SHA-256 before the appended continuation addendum: `136b903c10a5ea24e30fa94d05aab6903371208878f51ef0901dbba167b7cb15`). New durable continuation requirements are in `docs/WORK_SESSION_CONTINUATION.md` and linked from `Prompt.md`, `AGENTS.md`, and `START_HERE.md`.
- Project Drive folder: [private SM-A105F folder](https://drive.google.com/drive/folders/1azGQb-dRNXhy6fNAEKrwNOok4A2KiJYS). The project folder previously contained a verified 96,991-byte historical recovery bundle `SM-A105F-current-199011e-20260925.bundle`, SHA-256 `a9b1d2c15596e371ed0fbe32d56d3ba5190d0a170a4c560818c41046a31aa399`, commit `199011e0e9537dbc45c53e394538aa6913f6845b`; this predates newer GitHub status and is recovery only. `docs/ARTIFACTS.md` is authoritative for artifact details. The temporary handoff file uploaded during the preceding exchange was permanently deleted from Drive at the user's direction; it was omitted from a later folder listing and its local scratch copy was removed.

## Stage and technical evidence

- Stage: third-party candidate-source investigation and host-built experimental Eureka kernel/DTB outputs. A separate Debian-oriented KSU-disabled Image and DTBs built successfully. In full-system ARM QEMU, the first Debian Installer attempt did not request the preseed. A second attempt fetched the preseed and configured virtual networking, but failed Debian mirror validation; neither attempt installed a system or yielded a rootfs archive. These are incomplete installer experiments, not an emulated Debian OS boot. No native-device boot package, initramfs, firmware-derived boot container or physical-device test exists.
- Official Samsung source listing found: build `A105FDDS9CWB3`, package `SM-A105F_SWA_RR_Opensource.zip`. The previous source download page reached a Cloudflare/security-verification gate; archive bytes, checksum, content inventory, licensing review, and exact source correspondence remain unverified. A third-party exact-build firmware listing exists, but firmware bytes/hash/provenance are absent.
- Candidate Eureka tree: `reference/inputs/eureka-r24u`, branch `R24U`, commit `e1b8464bb29ce5bcb9d52bfcfc71bc2563e12563`. This is third-party candidate source, not confirmed Samsung source or exact-stock-compatible boot evidence. KernelSU submodule pin `109442f8c4c7692af6562bdad6fd9f39dc1f935b`; AnyKernel3 was uninitialized.
- The candidate checkout had a missing tracked symlink `arch/arm64/boot/dts/exynos/dtbo/exynos7885-ecd.dtsi` pointing to `../dtb/exynos7885-ecd.dtsi`. Upstream contains the link and its target; the exact symlink was restored and the nested checkout was clean before build. The generated A10 SWA overlay compiled successfully.
- The original systemd-oriented `.config` remains 141,300 bytes, SHA-256 `48fd25767b07834b739ec23d52aab62bb5f8c9bdda5f50ba8d2b1a0b4f717932`. A second Debian-oriented config disables KernelSU: `configs/eureka-r24u-sm-a105f-debian.config`, 141,281 bytes, SHA-256 `faf3394e6f1bc194189b306c7774e31dde308c82cfb56f140c4471d98aa11c34`. From pinned Eureka `e1b8464bb29ce5bcb9d52bfcfc71bc2563e12563` with KernelSU submodule `109442f8c4c7692af6562bdad6fd9f39dc1f935b`, Clang/LLVM 14.0.6 and GNU AArch64 binutils 2.42, the host build produced `4.4.302-p6-Eureka_R24U`. The ARM64 Image is 27,853,024 bytes, SHA-256 `25b9bd876efd635d43fdf5903b455717863a837fdf08dab0049b4372898fea43`; `System.map` SHA-256 is `d832beb1bdfb3c71290b52e37dbb4decbb695870c658fe6380becebf06b73292`. The generic base DTB plus seven overlays compiled, including SWA `exynos7884B-a10_swa_open_00.dtbo`; `dtc` identifies compatible `samsung,A10 SWA OPEN 00` and `samsung,EXYNOS7884B`. Build logs report two unused-variable warnings and a non-fatal missing AnyKernel version lookup. `MODPOST 0 modules` was reported. This configuration enables `CONFIG_KSU=y`; do not deploy it. Kernel `4.4.302-p6` is far older than modern Debian/systemd expectations and remains a major security/compatibility blocker.
- Static compatibility audit of the pinned KSU-disabled config against upstream systemd 257.13 identified a confirmed setting defect: `CONFIG_FW_LOADER_USER_HELPER=y`, while systemd's README says userspace firmware loading is unsupported and should be disabled. The candidate also lacks `CONFIG_USER_NS` and `CONFIG_CGROUP_PIDS`; it has `CONFIG_NET_NS`, seccomp/filter, and the listed core systemd options. Linux 4.4 is below systemd's 5.4 recommended baseline and below the stated 4.5 requirement for cgroup-v2 PIDs control. Details and consequences are in `docs/ARCHITECTURE.md`; the config has not yet been corrected or rebuilt. This remains static evidence, not runtime compatibility proof.
- The original KSU-enabled output package remains in private Drive as `SM-A105F-eureka-r24u-host-build-20260925.tar.gz`, 12,406,459 bytes, SHA-256 `78a90a90ac355a6caafe64ee32ca8c630f09bebab243a3449a26413b7b52fde0`. It contains the image, config, System.map, base DTB, seven A10 overlays, logs, provenance notes, all 19 package checksums, and an internal SHA-256 list. Drive metadata reports owner-only sharing; a full download was byte-compared with the local archive and the SHA-256 matched. See `docs/ARTIFACTS.md`. A separate KSU-disabled build archive is now in private Drive: `SM-A105F-eureka-r24u-no-ksu-host-build-20260925.tar.gz`, 25,899,371 bytes, SHA-256 `78594b207d6c526fdb2a6e007fefedda8ae66c6a228609694a4d6852302bf8d8`; downloaded again, byte-identical, all internal payload checks passed, listing reports not shared. See `docs/ARTIFACTS.md`. Scratch build trees and package staging are still temporary; the Drive archive preserves selected outputs, not all source objects or build caches. A bounded upstream/community branch scan found generic Exynos7885 support upstream and only Linux 4.4.x in the inspected universal7904/Exynos7885 refs; no newer exact SM-A105F kernel candidate emerged. The scan scope and refs are in `docs/ARCHITECTURE.md` and `docs/SOURCES.md`.
- Current host checks: 2 archive-inventory unit tests passed; `bash -n scripts/build-eureka-kernel.sh scripts/build-rootfs.sh scripts/configure-eureka-a10.sh` passed; `git diff --check` passed after the current doc/config/script changes. No real Samsung archive was tested.
- Physical phone state: not modified, flashed, wiped, repartitioned, or booted into a project image; no physical-device engineering test. Boot chain, bitness, partition map, boot/recovery images, stock DTB/DTBO and recovery path remain unverified. No phone modification is authorized.

## Current environment and active work

- Current shell is Linux x86_64; the prior staged QEMU 8.2.2 launched Debian Installer with its checksum-verified Trixie ARM64 kernel/initrd. In the retry, `work/rootfs-builder/http-retry.log` recorded `GET /preseed.cfg` with HTTP 200; the installer screen reported network autoconfiguration success, then failed the mirror check. Host `curl` through the configured proxy reached `chatgpt.com` but timed out for `deb.debian.org`, and direct DNS lookup for Debian failed. This provides an observed network-path blocker; no package installation or rootfs archive exists. User namespaces and PRoot remain sandbox-blocked. The retry's QEMU session is no longer active; no background installer is running. The one-use preseed has a transient crypted password hash and stays in ignored scratch. Scratch contains a 911 MiB `work/rootfs-builder` tree, mostly an incomplete sparse installer disk and logs; none of this is durable storage.
- The fresh KSU-disabled kernel build and verified private Drive artifact remain the last successful engineering build milestone. Candidate source, temporary apt packages, compiler stage, full object tree, raw build logs, and incomplete installer state are still only in ignored scratch; those files are not GitHub or Drive backups. Recreate from the pinned revisions and documented package snapshot if this workspace is lost.
- Personal Context retrieval reported disabled, consistent with the user's prior privacy choice. Use only conversation and project files available in this session; do not claim hidden memory access.
- No external purchases, account changes, physical actions, or model switch are pending/authorized by this checkpoint. The user's model and Chat-vs-Work preferences are described in `docs/WORK_SESSION_CONTINUATION.md`; actual model/quota status must not be invented.

## Blockers and next authorized work

1. Reconcile the local scratch checkout against remote `main`. The workspace executor disconnected during documentation edits; its post-disconnection index/worktree status is unknown. Do not assume the checkout matches the remote or overwrite it without inspection.
2. Correct the confirmed Debian-config mismatch `CONFIG_FW_LOADER_USER_HELPER=y` against systemd 257.13, decide through security analysis whether `CONFIG_USER_NS` should be enabled, then regenerate/build and record the new config/artifact. No newer kernel candidate was found in the bounded source scan; broaden the evidence search without inferring compatibility from branch labels. Also investigate the 8-byte LLVM/LTO Image difference before claiming bit-for-bit reproducibility.
3. Find a supported ARM64 Debian rootfs path with access to authenticated Trixie package indexes. Full-system QEMU booted Debian Installer and retrieved the local preseed, but mirror validation failed because this environment's network route cannot reach `deb.debian.org`; user namespaces and PRoot remain sandbox-blocked. No rootfs exists.
4. Continue legitimate Samsung official source and exact stock-firmware provenance/acquisition. The source listing is known, but archive bytes are gated by Samsung's security page; no exact firmware bytes are present. Do not bypass access controls or substitute a third-party listing as acquired firmware.
5. Reconcile documentation/manifests after each substantive result and verify each artifact's actual durable location. The KSU-disabled kernel archive remains the last retrieval-verified Drive artifact; the Debian Installer kernel/initrd and the incomplete QEMU disk exist only in temporary scratch.

Exact next action: on a connected workspace, verify live GitHub `main` and tree, inspect local Git status and outstanding processes, reconcile the local checkout without destructive reset, then fix and rebuild the Debian-oriented kernel configuration. Continue rootfs access research and exact source/firmware work independently where feasible. The phone remains untouched.

## Current synchronization snapshot — 2026-09-26 UTC

This snapshot supersedes the earlier status above that identified `f62cb267` as the current checkpoint or said this documentation update was unsynchronized. Codespace `main` and GitHub `origin/main` were verified at commit `24af697c7728246677cc07771b4c05d0006fa282`, with matching tree `ada0585097fffe75c3d455be85201af96720c5c30`; the Codespace worktree was clean after the push.

The separate scratch checkout at `/workspace/scratch/4d6756134406/SM-A105F` remains at `5aee00f1c69cca636a0374c4ce3e19a8bb427bab` and is not synchronized. Its GitHub remote authentication failed in this runner. It was left untouched; two nested symlinks were already absent there and were not restored.

The verified 196,298,240-byte Debian rootfs archive and matching sidecar remain only in Codespace `/tmp/SM-A105F`; they have not been uploaded to Drive or GitHub. Therefore source/docs are synchronized between Codespace and GitHub, while the scratch checkout and rootfs artifact remain outstanding. No phone, boot, or QEMU test occurred.

## Reconciled engineering state — 2026-09-27 Asia/Colombo

This is a historical snapshot as of its stated date; current kernel-support and user-namespace findings are updated in the top checkpoint and the later architecture review. Its broad action to assess `CONFIG_USER_NS` security has been refined into the explicit resource-limit and effective memory-cgroup verification gate.

At the time of this 2026-09-27 snapshot, this section superseded the status records that preceded it where later evidence in `docs/ARCHITECTURE.md`, `docs/ARTIFACTS.md`, and the tracked config disagreed. The present top checkpoint contains newer repository and review state. The tracked `configs/eureka-r24u-sm-a105f-debian.config` is 141,261 bytes with SHA-256 `8cf0cdb2afd5dfcaff779460b09351cb6feeb4ebc306710598c2aeed6aae3d4c`. The ineffective hidden-symbol assignment was removed; `CONFIG_FW_LOADER_USER_HELPER_FALLBACK` is unset. Two fresh host builds using the documented pinned sources/toolchain matched the Image and recorded outputs. This resolves the static config finding and documents host build repeatability only; it does not prove systemd runtime compatibility or device readiness.

`CONFIG_USER_NS` and `CONFIG_CGROUP_PIDS` remain unset. Linux 4.4.302-p6 is below systemd 257.13's recommended 5.4 baseline; user namespaces require a deliberate security/operations review, and the 4.4 kernel cannot provide the later cgroup-v2 PID controller. No config change or new build is justified until those consequences and a compatible kernel path are assessed.

The earlier statement that no rootfs archive exists describes the failed Debian Installer/QEMU route. A later separate `mmdebstrap` host build produced `/tmp/SM-A105F/debian-trixie-arm64-rootfs.tar` (196,298,240 bytes; SHA-256 `67ba3022d06670799eb4a3d51d9897655bd1641835e346bf8c6126ed9471f975`); its sidecar and archive entries were verified. It remains temporary in Codespace `/tmp`, not stored in Drive or GitHub. The Google Drive sync receipt `SM-A105F-sync-checkpoint-20260926.md` (file ID `1wfyD3ELfLUCwsHHIh624kqvMqLE6bF85`) records the current commit and this outstanding artifact gap.

The current Codespace and GitHub `main` were verified clean and identical at `acc88e103c05c746d19637d0bc72af3a7e9816ab`, tree `301fe2410090765995d0154987431ccaecf506cc`, before this status correction. The separate scratch checkout remains at `5aee00f1c69cca636a0374c4ce3e19a8bb427bab`; its tracked tree was clean, but it is a divergent historical line. Remote authentication failed in the local runner, so it remains untouched and unsynchronized.

Next exact work: (1) find a supported, verifiable path to persist the already-built rootfs without rebuilding or routing the 187 MiB file through the local runner; (2) assess `CONFIG_USER_NS` security and document the practical systemd 257/4.4 limitations; (3) continue legitimate Samsung source/firmware acquisition and newer device-compatible kernel research. No phone modification, flash, or project-image boot is authorized.

## Rootfs archive validation and Eureka host build — 2026-09-26

The private draft rootfs release rootfs-trixie-arm64-20260926 contains the 196,298,240-byte TAR; SHA-256 67ba3022d06670799eb4a3d51d9897655bd1641835e346bf8c6126ed9471f975. Read-only inspection in the authenticated Codespace confirmed the TAR matches that digest and lists a Debian GNU/Linux 13 (trixie) base (VERSION_ID 13, VERSION_CODENAME trixie, DEBIAN_VERSION_FULL 13.7). /etc/os-release links to /usr/lib/os-release. dpkg status contains 117 packages, all marked install ok installed: 101 arm64 and 16 all. The archive contains base /dev entries, proc/run/sys directories, /usr/lib/systemd/systemd, and an APT source file under /etc/apt/sources.list.d with Debian trixie, trixie-updates, and trixie-security main entries. No Xorg, Weston, GNOME Shell, or startx binaries were found by the bounded path check. Archive bytes were not extracted or changed. This validates archive metadata only; no chroot, package transaction, emulation, boot, hardware, or runtime check occurred. Treat it as an unprovisioned rootfs archive, not a bootable image.

The separate Linux 4.4 Eureka R24U host build and its private draft artifact are recorded in docs/BUILD.md and docs/ARTIFACTS.md. Image, vmlinux, System.map, generic Exynos 7885 DTB, and seven A10 DTBOs were packaged and verified by checksums and fresh retrieval. Host build only; not tested on hardware. Keep the 4.4 vendor track distinct from modern-kernel research.

## R24U boot-path and packaging audit — 2026-09-26

Read-only inspection of work/build/eureka-r24u-sm-a105f-retry1/.config found built-in ext4 (CONFIG_EXT4_FS=y), initrd (CONFIG_BLK_DEV_INITRD=y, CONFIG_RD_GZIP=y), devtmpfs and its automatic mount (CONFIG_DEVTMPFS=y, CONFIG_DEVTMPFS_MOUNT=y), MMC and block support, Samsung serial console, and Exynos 7885 SoC support. These are configuration prerequisites only, not proof that the storage controller, partition map, bootloader handoff, device tree, or Debian init sequence works on SM-A105F.

The repository's scripts directory contains only scripts/build-eureka-kernel.sh. Its final checks establish Image and vmlinux outputs, reject unresolved KernelSU symbols, report kernelrelease and hashes; it does not create an initramfs, boot.img, AnyKernel archive, or flash package. The current host output has a generic exynos7885.dtb and seven A10 DTBOs but no exact boot image, no extracted matching vendor ramdisk, and no device-tested DTB/DTBO composition. Therefore no packaging format or bootable artifact is justified yet. Next dependency is exact SM-A105F boot image/layout and matching stock ramdisk/device-tree provenance from an authorized source; do not infer it from the generic DTB or other A10 variants. No device access occurred.

## 2026-09-27 continuation update

- Live project work is now based on GitHub main through the preceding journal/source-review update; the linked geckyn tree was inspected at commit ad10da74b6b2fcccdb2a2cfdb5d02aaa79b5a282. It is Linux 4.4.200 with an A10 ARM64 defconfig, but not an exact A105F tree: its config selects Exynos7885/7884A and it has only generic Universal7884 Treble DTs in the inspected set. The candidate is documented as comparison material, not a boot input.
- The TeraBox share named SM-A105F_A105FDDS9CWB3 launched a terabox:// transfer instead of yielding downloadable image bytes; the browser security policy blocks that protocol. No firmware was acquired and no protocol workaround was attempted.
- The Codespace browser currently requires Google sign-in and is stopped at an invalid security-code challenge. This session has no verified live Codespace terminal/filesystem, so there was no kernel build or firmware download into Codespace. No phone action occurred.
- Repeat local verification of scripts/inspect_android_dtbo.py completed: 5/5 tests passed; the saved community SWA DTBO parsed as one 2 KiB-page entry. This remains community evidence, not stock-image provenance.
- Exact blocker: obtain handset-matched stock AP data and authenticate an active Codespace session before host compilation there. Next: complete the visible Google verification manually if Codespace work is needed; obtain the confirmed-build AP archive or stock boot.img/dtb.img/dtbo.img for read-only inspection. Keep Linux 4.4 candidates separate and the modern 6.x port as a distinct track.


## 2026-09-27 update: firmware candidate parsed

The user-supplied A105FDDS9CWB3 Android 11 firmware archive is now downloaded and outer-ZIP/hash verified. Its AP images are measured in `docs/reports/a105f-cwb3.json`. The stock boot header is v1/page 2048 and declares kernel size 29,112,000 bytes at 0x10008000 with ramdisk size zero. Separate DT and DTBO containers each hold one table entry. The stock kernel identifies as 4.4.177-2184546; this does not match the 4.4.111 Eureka source baseline. The firmware does not remove these gates: verify that its build matches the untouched handset, resolve the opaque vendor boot tail/signing behavior, confirm installed partition map/capacities and selected overlay, and obtain/authenticate the exact vendor source before producing a flashable Debian image. The existing 134-byte Eureka initramfs is not Debian initramfs. The 6.18.54 path remains a board-port experiment. No physical-device action was taken; test suite passes 12/12.


## Current source and packaging checkpoint — 2026-09-27

The user-attached Samsung source archive is integrity-checked and correlates to the candidate AP kernel's 4.4.177 version string. The vendor defconfig succeeds with the Samsung README environment; the full kernel/DTB build is blocked by missing GCC 4.9 AArch64 cross-toolchain, and the large archive did not transfer into Codespaces. Do not claim a kernel output from this source.

The AP candidate's stock boot is Android header v1 / 2048-byte page, kernel size 29,112,000 bytes at `0x10008000`, and no stock ramdisk. Base DT and DTBO are separate 8 MiB table images with a single Exynos7885 base entry and a matching A10 SWA OPEN 00 overlay entry. Firmware archive is a user-provided candidate; active phone firmware, installed partition sizes, bootloader DT flow, selected overlay, and authenticity remain unverified.

The previous Eureka Linux 4.4.302 image is still only a different-source host artifact; modern Linux 6.18.54 remains a generic Exynos7885 build without A10 DTS. Latest verified GitHub/Codespace baseline before these edits: `7b3f7c77f2c761c0b4182b75735786e5f066c9c1` (`main`). Phone untouched. Next: use the Samsung tree and a matching cross-toolchain in Codespaces, build and record hashes, then derive a nonempty Debian initramfs and package only against independently verified stock layout.


## Live continuation update — 2026-09-27

- Live private GitHub `main` and Codespace checkout were verified aligned at `c6fcc6fb1a19006630bea8efa1edc0bd2f56a31b` before this update.
- Official AOSP Android AArch64 GCC 4.9 is staged outside Git in ignored `work/toolchains/aosp-gcc49`, pinned to populated upstream commit `f144eaad5cb268fa4105875e98ed4ac47efa7f06`. The compiler passes a freestanding AArch64 compile/static-link probe; the Samsung kernel build has not run.
- Only source transfer part confirmed in Codespace is `work/kernel.tar.gz.part-00` at 33,554,432 bytes. The current Work session does not have the supplied source ZIP available. Reconstruction and hash verification are blocked pending retransmission of the source archive.
- Physical handset remains untouched. No Debian boot image or initramfs is validated or deployable.

### Mirror audit update — 2026-09-27

A public same-version mirror (`topser9/kernel_samsung_universal7885`, `master` commit `ae3bd5aef8fd81bff8c8807fa9a16ef47970b9c3`) has Linux 4.4.177 and `exynos7885-a10_defconfig`, but that config selects Android P and no A10/A105F DTS appears in its Exynos DTS directory. Retain as a comparison source only; exact supplied Android R kernel build remains blocked on archive transfer.

### Modern kernel upstream support check - 2026-09-27

Upstream Linux torvalds/linux snapshot fd179f8a05be3ccae366b9b96e176b51fbe54aab has Exynos7885 SoC DTS and a Galaxy A8 2018 / SM-A530F board DTS, but no A10/A105F board DTS in the inspected Exynos directory. Kernel.org listed 7.2.8 as stable and 6.18.54 as longterm on 2026-09-27. Keep 6.18.54 as the first longterm port candidate and evaluate 7.2 separately; neither is A10-ready.

## Host-side verification update — 2026-09-27

- `python3 -m unittest discover -s tests -v`: PASS (17 tests).
- Generic upstream Linux 6.18.54 ARM64 `Image`: PASS; see `docs/ARTIFACTS.md` for build command, path, and SHA-256.
- This image is not an SM-A105F candidate. The original Samsung source archive is not kept in Git; the extracted build source is staged at `work/sources/samsung-a105f` in the Codespace.
- Physical SM-A105F remains untouched. Device-specific integration, boot-image validation, and hardware validation remain outstanding.

## 2026-09-28 verified Samsung kernel build

The 4.4.177 source now builds successfully with the official historical AOSP GCC 4.9.2 toolchain. The in-tree Android 11 build produced Image, base DTB, matching A10 SWA DTBO, vmlinux, System.map and one KUTF module. Config SHA-256: 27f3714948ad986331949100e702834fac8d08e917cf5e891c6dc6defe4261a3. See BUILD.md for compiler provenance, exact parameters, host workaround and artifact paths. Host-only result; no phone boot/action.

## 2026-09-28 host verification follow-up

- Re-ran project checks: `python3 -m unittest discover -s tests -v` passed 19 tests; `bash -n scripts/build-rootfs.sh` and `python3 -m py_compile scripts/inventory-archive.py` also passed.
- Upstream Linux 6.18.54 `dtbs` completed with `make -C work/sources/linux-6.18.54 ARCH=arm64 -j4 dtbs`. The verified `exynos7885-jackpotlte.dtb` is 20,923 bytes with SHA-256 `752c7932361b4b81e2f849c2a13d5687e221d3dea49f648e99a26b5259721261`; it is the Galaxy A8 (2018) reference board, not an A10 image.
- The current rootfs staging snapshot at `work/rootfs-verify.Gm1DH4` is 200 MiB and reports Debian GNU/Linux 13 (trixie), 117 installed packages, and an empty `dpkg --audit`. AArch64 systemd 257.13 runs under `qemu-aarch64-static`; this is a userspace execution check, not a boot test. `/etc/hosts` is missing, so this snapshot is not ready to boot as a system root.
- The host-only boot candidate archive `work/artifacts/SM-A105F-host-only-boot-candidate-20260928.tar.gz` has SHA-256 `f28d6a29369a5ea06750123a4ed9af0a9c5f19b0f7ef6c125c98a71e87cfd98a`. It remains a structural candidate without verified handset partition/signing/bootloader compatibility.
- No physical-device action was performed; the phone remains untouched.

## 2026-09-28 Debian 13.7 ARM64 rootfs rebuild

- Rebuilt with sudo -n bash scripts/build-rootfs.sh /workspaces/SM-A105F/work/artifacts/debian13-trixie-minbase-arm64-20260928-hosts.tar; mmdebstrap completed successfully in 292.8296 seconds using the registered AArch64 qemu-user binfmt handler and Debian Trixie repositories.
- Archive size: 196,298,240 bytes. SHA-256: 15acec8dba2c2ef535d721221d3a049f7ea243c46c8c2a9a4cadaf2ba6b5bb2d; the generated sidecar passed sha256sum -c from work/artifacts/.
- The archive contains /etc/hosts with 127.0.0.1 localhost and ::1 localhost ip6-localhost ip6-loopback, produced by the customize hook in scripts/build-rootfs.sh.
- Extracted archive reports Debian GNU/Linux 13 (trixie), VERSION 13. dpkg --audit returned 0 with no output. qemu-aarch64-static -L <rootfs> <rootfs>/usr/lib/systemd/systemd --version ran and reported systemd 257.13-1~deb13u1. This is AArch64 user-mode execution, not a system boot.
- Build log: work/logs/rootfs-build-hosts-20260928.log. Archive, sidecar, and log are attached to private draft GitHub release rootfs-trixie-arm64-20260928; tar and sidecar readback was byte-identical. Rootfs remains unprovisioned; mount discovery, initramfs integration, console/network boot, Samsung boot behavior, and physical-device validation remain unverified. The phone is untouched.

### Rootfs provisioning follow-up (2026-09-28)

A read-only audit of the published Debian 13.7 ARM64 rootfs archive (196,298,240 bytes; SHA-256 `15acec8dba2c2ef535d721221d3a049f7ea243c46c8c2a9a4cadaf2ba6b5bb2d`) confirmed 117 installed package records and `/etc/fstab` still contains the unconfigured base-system placeholder. `/etc/hostname` contains the Codespace-generated value `codespaces-1ab46f`; replace it with an intentional target hostname during rootfs generation/provisioning before preparing any boot candidate. The corrected localhost `/etc/hosts` is present. Target root-device/fstab entries and networking configuration remain unprovisioned. No source or artifact changed during this audit; this archive is still a host-validated candidate and has not booted.


### Rootfs hostname remediation (2026-09-28)

The mmdebstrap builder now explicitly writes hostname a10 rather than inheriting the Codespace name. Rebuild completed in 324.2584 seconds. New archive debian13-trixie-minbase-arm64-20260928-hostname.tar: 196,298,240 bytes; SHA-256 29d42b57730c4976b9c3c599b79cd9ecdf33c7017033cdb50d107bfb4323cc. The checksum sidecar verifies when checked from work/artifacts because its recorded path is basename-relative. TAR inspection confirms hostname a10, deterministic localhost entries, 117 installed package records and the still-unconfigured fstab placeholder. Extraction, dpkg --audit, and AArch64 systemd 257.13 execution under qemu-user completed without errors. This remains host-only; root-device mapping, networking and boot validation are open.

Modern-kernel source check: upstream Linux includes an Exynos7885 sibling board DTS for Samsung Galaxy A8 2018 / SM-A530F, compatible samsung,jackpotlte and samsung,exynos7885. It uses the Exynos7885 SoC include and describes board memory, serial aliases, GPIO keys and eMMC. This is useful reuse evidence, not an SM-A105F DTS; A10 SWA base/overlay differences must be reconciled before a mainline board port.
