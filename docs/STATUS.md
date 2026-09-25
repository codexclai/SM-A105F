# Authoritative project checkpoint

Updated: 2026-09-25 UTC, fresh-session reconciliation. Project identity: native Debian 13 Trixie ARM64 for Samsung Galaxy A10 SM-A105F. Stage: initial investigation; below completion level 1.

## Identity and persistence

- Canonical private repository: [thamindudenuwarajayasinghe/SM-A105F](https://github.com/thamindudenuwarajayasinghe/SM-A105F), default branch `main`. Last verified remote commit before this checkpoint update: `f0d44c0100f3eaebd7fe591f0bd997f24addc285`; GitHub connector verified the branch ref after a non-forced fast-forward. Its tree SHA `f17711506dbc3c34f033c7f4d96bfb6db669ead6` exactly matches local historical commit `749b9ecc167f905985f5c40b3d2bc73bef08e606`. The two commit chains differ because connected Git-data writes created new commit metadata. Verify the live remote ref before further edits.
- Current local branch is `main`; use `git log -1 --format=%H` for exact local HEAD. Latest verified private Drive history recovery is `749b9ecc167f905985f5c40b3d2bc73bef08e606`, bundle `SM-A105F-current-749b9ec-20260925.bundle`, SHA-256 `84c4717fb5753cdc06eba92ec8cb80ece0365f6013307e0695fdce6f67baae7b`; readback, byte comparison and fresh checkout passed. See `docs/ARTIFACTS.md` and the [SM-A105F Drive folder](https://drive.google.com/drive/folders/1azGQb-dRNXhy6fNAEKrwNOok4A2KiJYS). Verify whether a newer bundle exists before restoring.
- Root `Prompt.md` is an exact byte-for-byte copy of the supplied attachment, SHA-256 `136b903c10a5ea24e30fa94d05aab6903371208878f51ef0901dbba167b7cb15`.
- User requests task-specific model selection: Luna with suitable effort as default, Sol for tasks needing its capability, Astra exceptionally. Current user-reported setting is GPT-6 Luna High; assistant text cannot change model selection.

## Verified project state

- The recovered source tree contains project instructions, resumption guide, device/source/architecture/build/artifact/status/journal documentation, a guarded Debian ARM64 rootfs build script, a read-only firmware archive inventory tool, and two synthetic tests.
- Re-run in this session: `python3 -m unittest discover -s tests -v` passed 2 tests; `python3 -m py_compile scripts/inventory-archive.py` passed; `bash -n scripts/build-rootfs.sh` passed. These do not test a real Samsung archive or produce a rootfs.
- The shell is Ubuntu 24.04.3 x86_64, root, 9.2 GiB available RAM and about 30 GiB free disk. Debian HTTPS HEAD returned HTTP 200. `mmdebstrap`, `debootstrap`, QEMU and an AArch64 cross compiler are absent from PATH. A package-index fetch or ARM64 build has not been tested here.
- Samsung's official portal has a search result for the exact build `A105FDDS9CWB3` and source package `SM-A105F_SWA_RR_Opensource.zip`; package bytes are not acquired or audited. A third-party exact firmware listing exists but no archive is acquired. Stock boot/recovery, kernel bitness, device tree, partition map and boot constraints remain unverified.
- The public Eureka `R24U` source was inspected at commit `e1b8464bb29ce5bcb9d52bfcfc71bc2563e12563`: A10-specific ARM64 build path and defconfigs exist. Source compatibility with this exact stock firmware, licensing of all dependencies, successful build and physical-device support are unverified. Samsung's portal was blocked by a security challenge in this browser session; no official archive was acquired.
- The public Eureka checkout at this commit was expanded to a full transient tree (~1.1 GiB), with KernelSU submodule pinned at `109442f8c4c7692af6562bdad6fd9f39dc1f935b`; AnyKernel3 remains uninitialized. `docs/SOURCES.md` records revisions and selected hashes. Kconfig host generation passed, and an experimental two-option devtmpfs config was uploaded/read back from private Drive; see `docs/BUILD.md` and `docs/ARTIFACTS.md`. No kernel was built or device tested.
- No kernel, device tree, rootfs, initramfs, boot image or deployment package has been built. No physical device observation or test has occurred. No physical-device operation is authorized.
- The pinned Eureka A10 baseline generated config disables devtmpfs, while the experimental generated config enables devtmpfs and automatic mount; the `olddefconfig` diff showed only these two setting changes. Upstream systemd 257 recommends Linux 5.4 or newer; this candidate kernel is 4.4.302-p6, so userspace compatibility and maintenance remain serious gates.

## Synchronization and approvals

- The private GitHub `main` contains all 16 tracked files from local `749b9ec` byte-for-byte, including `Prompt.md` blob `77c3893980c7c81d9f16439bc922d4024756675a`. The GitHub snapshot has a separate four-commit chain; local history remains complete in Drive. Local `origin` points to canonical GitHub and old bundle upstream tracking was removed; shell Git still has no HTTPS credential. Neither a direct Git push nor an ancestry merge has been verified. Do not claim local SHA `749b9ec` exists on GitHub.
- GitHub browser sign-in succeeded after user takeover. The connected GitHub API created a README seed commit then a full-tree import without a force update; the branch and privacy were verified. The unrelated private `AlternateCLI` repository is separate.
- Drive connector access and readback of the new checkpoint bundle are verified. Its local and downloaded copies have identical size and SHA-256, and the bundle verifies and clones.
- The unrelated Drive folders `Colab Notebooks` and `Google AI Studio` were permanently deleted with the user's specific authorization; root listing showed only `SM-A105F`. The formerly listed unrelated GitHub repository `AlternateCLI` now returns 404 through browser and connector, and the account repository listing shows only `SM-A105F`. The operation that removed `AlternateCLI` was not observed in this workstream; do not attribute it to this assistant. Preserve the project folder.
- User explicitly requests a private repository named `SM-A105F`. Public visibility is not selected; the user says it may be considered only if publication review finds project contents safe. No source license is selected.
- No consequential physical-device action or paid storage action is authorized.

## Next exact actions

1. Commit this synchronization receipt and publish the matching tree to private GitHub `main` through connected Git-data writes; verify the remote ref and preserve the local history through a readback-verified Drive bundle. Because a commit cannot contain its own SHA, verify live remote/Drive refs for any later snapshots.
2. Reconcile the local historical branch with remote through authorized Git credentials when available. The unrelated GitHub repo is absent on current checks; verify again if cleanup matters, and keep project bundles.
3. Acquire exact Samsung source and stock firmware through legitimate accessible sources and hash them; resolve actual kernel architecture, boot image, device tree and partitions before packaging.
4. Assess Debian systemd 257 on the candidate kernel's actual ABI and cgroups, and provision an isolated host with QEMU/binfmt, signed Debian keyring and `mmdebstrap` to build/test an ARM64 rootfs; do not treat `chrootless` as a validated substitute.

Fresh-session resumption instructions: read `START_HERE.md`, `AGENTS.md`, this checkpoint, `Prompt.md` and `docs/JOURNAL.md`; verify Drive bundle hashes and clone the newest recovery ref if this workspace is gone. Inspect Git status and actual remote state before making changes. Keep physical-device work read-only until the user authorizes a specific operation.
