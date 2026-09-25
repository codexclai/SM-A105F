# Authoritative project checkpoint

Updated: 2026-09-25 UTC, fresh-session reconciliation. Project identity: native Debian 13 Trixie ARM64 for Samsung Galaxy A10 SM-A105F. Stage: initial investigation; below completion level 1.

## Identity and persistence

- Requested repository: private `SM-A105F` under the connected GitHub account `thamindudenuwarajayasinghe`. Canonical URL, remote branch and verified synchronized GitHub commit: **not established**. Do not mistake the existing unrelated `AlternateCLI` repository or a Drive bundle's temporary local `origin` for this project's remote.
- Current branch is `main`; use `git log -1 --format=%H` for exact local HEAD. Latest manifest-recorded private Drive recovery is commit `bee625d26da2821c867183f93574f368bff6e890`, bundle `SM-A105F-current-bee625d-20260925.bundle`, SHA-256 `d878b3169b972e666672923a51d235352edd07f630cdc277db1b3db200d93f05`; readback and fresh checkout of `main` passed. See `docs/ARTIFACTS.md` and the [SM-A105F Drive folder](https://drive.google.com/drive/folders/1azGQb-dRNXhy6fNAEKrwNOok4A2KiJYS). Verify whether a newer bundle exists before restoring.
- Root `Prompt.md` is an exact byte-for-byte copy of the supplied attachment, SHA-256 `136b903c10a5ea24e30fa94d05aab6903371208878f51ef0901dbba167b7cb15`.
- User requests task-specific model selection: Luna with suitable effort as default, Sol for tasks needing its capability, Astra exceptionally. Current user-reported setting is GPT-6 Luna High; assistant text cannot change model selection.

## Verified project state

- The recovered source tree contains project instructions, resumption guide, device/source/architecture/build/artifact/status/journal documentation, a guarded Debian ARM64 rootfs build script, a read-only firmware archive inventory tool, and two synthetic tests.
- Re-run in this session: `python3 -m unittest discover -s tests -v` passed 2 tests; `python3 -m py_compile scripts/inventory-archive.py` passed; `bash -n scripts/build-rootfs.sh` passed. These do not test a real Samsung archive or produce a rootfs.
- The shell is Ubuntu 24.04.3 x86_64, root, 9.2 GiB available RAM and about 30 GiB free disk. Debian HTTPS HEAD returned HTTP 200. `mmdebstrap`, `debootstrap`, QEMU and an AArch64 cross compiler are absent from PATH. A package-index fetch or ARM64 build has not been tested here.
- Samsung's official portal has a search result for the exact build `A105FDDS9CWB3` and source package `SM-A105F_SWA_RR_Opensource.zip`; package bytes are not acquired or audited. A third-party exact firmware listing exists but no archive is acquired. Stock boot/recovery, kernel bitness, device tree, partition map and boot constraints remain unverified.
- The public Eureka `R24U` source was inspected at commit `e1b8464bb29ce5bcb9d52bfcfc71bc2563e12563`: A10-specific ARM64 build path and defconfigs exist. Source compatibility with this exact stock firmware, licensing of all dependencies, successful build and physical-device support are unverified. Samsung's portal was blocked by a security challenge in this browser session; no official archive was acquired.
- A sparse public Eureka checkout at this commit was retrieved into ignored, transient `reference/inputs/eureka-r24u`; Git HEAD and representative file SHA-256 are documented in `docs/SOURCES.md`. Submodules are uninitialized and no generated `.config` exists. Re-clone by pinned revision if the workspace disappears.
- No kernel, device tree, rootfs, initramfs, boot image or deployment package has been built. No physical device observation or test has occurred. No physical-device operation is authorized.

## Synchronization and approvals

- The source is committed locally and a matching commit bundle is verified in Drive. GitHub synchronization remains unavailable because no project repository exists yet.
- GitHub connector reads the authorized account and lists repositories but exposes no repository-creation operation. The only listed repository, private `AlternateCLI`, is an unrelated CLI-agent project and is not canonical for this task. GitHub browser sign-in is still needed for browser-based creation unless another authorized creation workflow becomes available.
- Drive connector access and readback of the new checkpoint bundle are verified. Its local and downloaded copies have identical size and SHA-256, and the bundle verifies and clones.
- The unrelated Drive folders `Colab Notebooks` and `Google AI Studio` were permanently deleted with the user's specific authorization; root listing now shows only `SM-A105F`. The unrelated GitHub repository `AlternateCLI` still awaits an authenticated deletion workflow. Preserve the project folder.
- User explicitly requests a private repository named `SM-A105F`. Public visibility is not selected; the user says it may be considered only if publication review finds project contents safe. No source license is selected.
- No consequential physical-device action or paid storage action is authorized.

## Next exact actions

1. Commit this continuity-test correction and upload/read back a fresh full Git bundle to the private project Drive folder; capture its actual SHA-256 and `main` ref.
2. Through a supported authenticated GitHub workflow, create private `SM-A105F`, push and verify remote branch and commit. Delete `AlternateCLI` only through that authenticated workflow under the user's specific authorization; keep project bundles.
3. Acquire exact Samsung source and stock firmware through legitimate accessible sources and hash them; resolve actual kernel architecture, boot image, device tree and partitions before packaging.
4. Provision an isolated host with QEMU/binfmt, signed Debian keyring and `mmdebstrap` to build/test an ARM64 rootfs; do not treat `chrootless` as a validated substitute.

Fresh-session resumption instructions: read `START_HERE.md`, `AGENTS.md`, this checkpoint, `Prompt.md` and `docs/JOURNAL.md`; verify Drive bundle hashes and clone the newest recovery ref if this workspace is gone. Inspect Git status and actual remote state before making changes. Keep physical-device work read-only until the user authorizes a specific operation.
