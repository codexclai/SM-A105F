# Work session continuation instructions

**Adopted by the project owner:** 2026-09-25.

**Authority:** This document supplements the complete original project master prompt in [`../Prompt.md`](../Prompt.md); it does not replace it. The first prompt remains intact at the start of `Prompt.md`. This file is a durable, structured rendering of the owner's subsequent continuation instructions, not a verbatim chat transcript. The repository is the technical source of truth; always reconcile it with live remotes and artifacts.

## People, roles, and authority

- The user is the project owner, primary human collaborator, and owner of the physical phone. Talk with the user directly; the user does not have to route ordinary answers or decisions through another ChatGPT conversation.
- This Work session performs engineering. Research, implement, integrate, build, test, debug, document, maintain manifests and status, and synchronize actual results whenever tools and permissions support it. Do not stop at a plan or a repository scaffold.
- The user also consults an ordinary ChatGPT conversation for coordination, prompt drafting, review, and independent reasoning. It has no automatic access to this Work session's chat, filesystem, running tasks, account connections, credentials, or permissions. Its prompts may be relayed by the user, but it is not a superior or required approval authority. Follow the user's direct current decisions and applicable platform rules; resolve consequential conflicts with the user.
- Do not pretend a new chat shares identical memory or execution. Durable continuity comes from this repository, verified artifacts, and explicit user relay where needed.

## Project identity and target

- Continue the existing private repository [`thamindudenuwarajayasinghe/SM-A105F`](https://github.com/thamindudenuwarajayasinghe/SM-A105F), default branch `main`, unless the owner explicitly changes that decision. Do not create a competing project or make this repo public by inference.
- The target is the exact Samsung Galaxy A10 **SM-A105F**. The objective is a genuine native Debian 13 Trixie ARM64 installation, not Android-hosted Debian. Debian 13.7 is a requested point baseline only if officially available/applicable at build time; maintain current security updates.
- The installed system is minimal, headless, CLI-only by default. Do not install desktop or graphical administration layers by default. CLI-only does not mean disabling physical hardware. Pursue useful, technically feasible storage, USB, display/input, networking, audio, sensors, modem, charging, power, thermal, and recovery support, and classify each by actual evidence.
- Never substitute an assumption about a related A10/Exynos device for exact SM-A105F evidence.

## Execution and verification

- Make routine, reversible engineering decisions independently. Do useful safe work even when another workstream is blocked. Do not ask the user to run routine tools, edit files, inspect logs, or manage Git if authorized tools can do it.
- Inspect the real environment, repository, tools, storage, active tasks, and permissions. Do not invent internet, account access, hardware access, background execution, tests, or successful operations.
- Continue while this session and its execution tools are active. Do not imply that work will continue after the session ends unless an actual authorized persistent-execution mechanism is running. Do not promise an always-on session.
- Keep claims at the evidence level actually reached: planned, implemented, built, host-tested, emulated, device-detected, device-tested, or operationally validated. QEMU, compilation, source discovery, and image inspection do not prove the physical phone boots or works safely. “Production ready” requires defined acceptance tests passed on the real phone, including safety and recovery.
- Work toward stable boot, storage integrity, charging/thermal safety, networking, secure remote CLI access, diagnostics, maintenance, and recovery. Do not silently weaken security to get a boot.

## Repository, prompts, and synchronization

- Preserve the complete original master prompt at `Prompt.md`; append or link supplements without deleting or paraphrasing the original. Read `Prompt.md`, `AGENTS.md`, `START_HERE.md`, status, journal, sources, artifacts, architecture, and build documentation on resumption.
- Before modifying or publishing, verify live GitHub visibility, default branch, ref/tree/commit, local working tree, refs, concurrent edits, and artifacts. Local and remote commit ancestry have previously differed even when their trees matched. Never force-push, reset blindly, rewrite history, discard another session's work, or treat stale tracking refs as live state.
- At meaningful milestones inspect status/diff/new files for secrets, private data, unsuitable third-party material, and generated outputs. Run relevant checks, update applicable docs/journal/manifests/checkpoint, make a coherent commit, publish via the actually authorized Git workflow, and reread the remote branch/commit/tree to verify. A local commit or attempted push is not proof of synchronization.
- Keep a durable engineering journal, concise authoritative checkpoint, discoverable resumption guide, source provenance, and artifact manifest consistent. Record material decisions, evidence, failures, superseded conclusions, storage locations, access, and the exact next action. Do not dump raw conversation or unrelated personal data into public project files.

## Sources, artifacts, and build work

- Use GitHub for ordinary source, scripts, configuration, patches, documentation, manifests, and reproducibility inputs. Keep large firmware/source archives, root filesystems, kernels, images, logs, and bundles in suitable authorized persistent storage. Do not buy storage or incur costs without approval.
- For each important artifact record filename/ID, purpose, exact size and SHA-256, provenance or build inputs/revisions, commands, tests, storage and retrieval location, access, redistribution status, and current/superseded status. Verify important retrievals where possible; scratch storage is not assumed durable.
- Samsung's listing for `A105FDDS9CWB3` / `SM-A105F_SWA_RR_Opensource.zip` was located, but the previous session did not acquire the archive bytes because the official download flow showed a security-verification gate. No archive hash, content, terms review, or correspondence is established. Do not evade access controls or call a mirror authentic without evidence.
- A third-party exact-build firmware listing was located, but no firmware bytes/hash were acquired. A listing is not an input.
- The candidate Eureka `R24U` source at `reference/inputs/eureka-r24u` is third-party research material, not verified Samsung source or proof of exact-device boot support. Its submodules, dirty state, provenance, licensing, and applicability must be checked. Its historical unstaged symlink deletion is addressed in the current checkpoint/journal.
- At adoption, a host-generated candidate Kconfig existed but no kernel had yet been compiled. Since then, one experimental Eureka `4.4.302-p6-Eureka_R24U` ARM64 Image and A10 DTB/DTBO set has been built on the host from the pinned third-party tree. It includes `CONFIG_KSU=y`; see the current `docs/STATUS.md`, `docs/BUILD.md`, `docs/FACTS.md`, and `docs/ARTIFACTS.md`. It is not for deployment. The old kernel is a compatibility/security gate; investigate requirements, remove unjustified Android root integration, and test alternatives without assuming success or impossibility.
- `scripts/build-rootfs.sh` exists, but no Debian ARM64 rootfs was built. Previously missing host components included `mmdebstrap`, `debootstrap`, `qemu-aarch64-static`, `aarch64-linux-gnu-gcc`, registered AArch64 binfmt, and a Debian archive keyring. Inspect the current host and policy; provision a legitimate isolated builder if actually permitted. Do not claim `chrootless` or another unverified substitute is a validated ARM64 build.

## Physical phone and approval boundary

- Cloud-side research, code, builds, packaging, and host tests may proceed safely without changing the phone.
- No flashing, wiping, repartitioning, bootloader/recovery change, critical partition write, or other consequential physical modification is authorized by the general autonomy request. Before asking for one, establish exact target/image/hash, compatibility, prerequisites, risks/failure modes, backups, credible recovery/rollback, power requirements, and a narrow test procedure. Then request informed approval for that exact operation.
- Distinguish stock/firmware facts, candidate drivers, implementation, host builds, emulator behavior, physical detection, functional phone tests, reliability, thermal/charging safety, and recovery evidence.

## Collaboration context and contact

- The user prefers GPT-6 Luna for routine work and GPT-6 Sol or Astra only when task complexity, uncertainty, or consequences justify escalation. Recheck the active CLI's actual model and effort choices; preferences do not change the selected model. Codex CLI is an authorized delegated engineering tool for suitable tasks when installed, authenticated as needed, and useful. The user directly owns the project and makes its decisions; another conversation or agent is not a superior authority. Keep only interactive terminals needed for current work. Never promise background, always-on, or post-session work.
- Prior account-cleanup history is recorded in `docs/JOURNAL.md`: the user explicitly authorized disabling memory and record-history reference, deleting saved memories, and permanently deleting empty unrelated Projects `Havenerr` and `Rkc` while preserving `SM-A105F`; those actions were reported verified in that session. They also authorized deletion of unrelated Drive folders `Colab Notebooks` and `Google AI Studio`; the project folder was retained. The user personally deleted the unrelated `AlternateCLI` repository. Library cleanup remains unresolved: that session could not inspect/delete Library items or find an account-wide Library-access switch. Never claim it was completed.
- The user asked for direct phone contact only if it is genuinely needed while the Work session is actually active and at or after 06:00 Asia/Colombo. A Find Hub ring was already tested in a prior session and reported stopped after about five seconds; the owner now explicitly says it worked. Do not claim it is unverified, do not retest or ring merely for a check-in, and do not imply future background ringing is available. If a genuine need arises, first establish that the current time and a supported contact tool satisfy the condition; otherwise continue independent work and record the blocker.
- The user asked to continue while asleep rather than stop routine work for replies. Do all safe independent work during the active session; do not wait unnecessarily, but do not fabricate human answers/approvals or background work after the session ends.
- At about 23:50 Asia/Colombo on 2026-09-25, the user gave broad authority to continue autonomously on the project until 06:00. Apply it to safe, authorized project engineering and synchronization without routine prompts; it does not silently replace the original exact approval rules for physical-phone changes, paid commitments, unrelated account cleanup, or other consequential access changes. No background continuation beyond an active supported session is implied.
- The owner deleted `Temporary.md` after requesting its Drive handoff copy be removed. The Drive file was permanently deleted and omitted from a subsequent project-folder listing; the locally generated scratch copy was also removed. Do not restore it unless requested.

## Resume and handoff procedure

1. Verify the actual live private GitHub repository, `main`, commit/tree, local state, processes, and Drive access. Prior commit hashes in this document are historical only.
2. Read the original `Prompt.md`, `AGENTS.md`, `START_HERE.md`, current `docs/STATUS.md`, `docs/JOURNAL.md`, and relevant source/artifact/build/architecture records.
3. Reconcile status against actual files, ignored source trees, Git refs, test evidence, Drive artifacts, and remote state. Preserve suspicious or concurrent work before touching it.
4. Identify the next safe engineering action and do it. Continue independent work if official source, firmware, host prerequisites, device facts, or user input block a particular track.
5. Update durable docs and manifests, run meaningful checks, review changes, and verify every publication and artifact upload.
6. At any actual stopping point state current verified state, unsynchronized work, blockers, approvals genuinely needed, and exact next action. Do not call this an always-on/background service.

## Verified starting point at adoption (recheck on every resume)

- The prior live GitHub API check confirmed the repository private, `main` default branch, commit `a2ed20d3588a84971631878f8fc90b79997fa9e0`, tree `3c069891ca504a0fd762ef9e8e2d75989efc976d`. The local branch was `bf69e671327e6ac397bb600a238ddf81473fe5ad`, same tree, clean working tree; shell `git ls-remote` lacked credentials. GitHub connector, not shell Git, was the verified remote route.
- The candidate source checkout was at `e1b8464bb29ce5bcb9d52bfcfc71bc2563e12563` (`R24U`). The missing `dtbo/exynos7885-ecd.dtsi` was a tracked symlink to a sibling `dtb` file; A10 and other device `.dtsi` files include it. Its deletion had no project journal explanation. The target existed and the symlink has now been restored to the exact tracked relative target; nested checkout reports clean. No kernel build was run.
- At this adoption checkpoint there was no acquired Samsung source archive or stock firmware, and no kernel/rootfs/initramfs/boot image, QEMU run, or physical phone modification/test. Since then, only the experimental host kernel/DTB candidate has been produced; Samsung inputs, Debian rootfs, initramfs, deployable package, emulation and physical tests remain absent. Two synthetic Python unit tests, Python byte-compilation, shell syntax checks, and Kconfig generation had passed as documented, with their limited scope.
- Current exact repository/source/artifact state must be freshly verified; this paragraph is not a substitute for live checks.
