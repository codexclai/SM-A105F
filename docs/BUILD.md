# Rootfs build: first host-side increment

`scripts/build-rootfs.sh /absolute/output/path/rootfs.tar` is an unprovisioned Debian Trixie `arm64` tar builder. It requires a trusted Debian archive keyring, `mmdebstrap`, root access in an isolated builder, `qemu-aarch64-static` registered through binfmt, and network access to Debian's signed repositories. It refuses an existing output. It requests a minimal package base plus init, SSH, network diagnostics, certificates and module tools. A future stage must implement secure credential provisioning, storage, networking, firmware, initramfs and physical integration before deployment.

The `trixie`, `trixie-updates`, and `trixie-security` suites preserve supported updates. The point-release label describes repository state at acquisition, not a frozen package set. Save package versions and repository metadata with each real build.

Current shell verification: `bash -n scripts/build-rootfs.sh` passed; execution preflight reports missing `mmdebstrap`. **No rootfs exists and no ARM64 package has been configured or executed.**

Reference: [Debian mmdebstrap manual](https://manpages.debian.org/trixie/mmdebstrap/mmdebstrap.1.en.html).

This host currently has no registered AArch64 binfmt handler, QEMU user emulator or Debian archive keyring. The documented `mmdebstrap --mode=chrootless` alternative does not safely substitute for a fully configured foreign architecture rootfs here: Debian warns that only a small subset of packages support it and maintainer scripts execute outside the target. Use a provisioned isolated builder with package signature checks and registered emulator; capture exact package versions, inputs and hashes before treating any rootfs tar as a build result.

## Read-only firmware archive inventory

`python3 scripts/inventory-archive.py /absolute/path/to/archive.zip` (or `.tar.md5`) emits JSON with the input file's size and SHA-256, member names/sizes, and warnings for unsafe or duplicate names. It never extracts members. It **does not** authenticate archive provenance, validate ZIP payload CRCs, calculate individual member hashes, check Samsung's appended MD5, or prove boot compatibility. Run it against an immutable acquired reference and retain its JSON alongside the source manifest.

Host checks on 2026-09-25: `python3 -m unittest discover -s tests -v` passed 2 synthetic archive tests, `python3 -m py_compile scripts/inventory-archive.py` and `bash -n scripts/build-rootfs.sh` passed. No Samsung archive was available to inventory.
