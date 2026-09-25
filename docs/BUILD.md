# Rootfs build: first host-side increment

`scripts/build-rootfs.sh /absolute/output/path/rootfs.tar` is an unprovisioned Debian Trixie `arm64` tar builder. It requires a trusted Debian archive keyring, `mmdebstrap`, root access in an isolated builder, `qemu-aarch64-static` registered through binfmt, and network access to Debian's signed repositories. It refuses an existing output. It requests a minimal package base plus init, SSH, network diagnostics, certificates and module tools. A future stage must implement secure credential provisioning, storage, networking, firmware, initramfs and physical integration before deployment.

The `trixie`, `trixie-updates`, and `trixie-security` suites preserve supported updates. The point-release label describes repository state at acquisition, not a frozen package set. Save package versions and repository metadata with each real build.

Current shell verification: `bash -n scripts/build-rootfs.sh` passed; execution preflight reports missing `mmdebstrap`. **No rootfs exists and no ARM64 package has been configured or executed.**

Reference: [Debian mmdebstrap manual](https://manpages.debian.org/trixie/mmdebstrap/mmdebstrap.1.en.html).

This host currently has no registered AArch64 binfmt handler, QEMU user emulator or Debian archive keyring. The documented `mmdebstrap --mode=chrootless` alternative does not safely substitute for a fully configured foreign architecture rootfs here: Debian warns that only a small subset of packages support it and maintainer scripts execute outside the target. Use a provisioned isolated builder with package signature checks and registered emulator; capture exact package versions, inputs and hashes before treating any rootfs tar as a build result.

## Read-only firmware archive inventory

`python3 scripts/inventory-archive.py /absolute/path/to/archive.zip` (or `.tar.md5`) emits JSON with the input file's size and SHA-256, member names/sizes, and warnings for unsafe or duplicate names. It never extracts members. It **does not** authenticate archive provenance, validate ZIP payload CRCs, calculate individual member hashes, check Samsung's appended MD5, or prove boot compatibility. Run it against an immutable acquired reference and retain its JSON alongside the source manifest.

Host checks on 2026-09-25: `python3 -m unittest discover -s tests -v` passed 2 synthetic archive tests, `python3 -m py_compile scripts/inventory-archive.py` and `bash -n scripts/build-rootfs.sh` passed. No Samsung archive was available to inventory.

## Experimental Eureka A10 config generation

The complete pinned Eureka checkout and its pinned KernelSU submodule can generate a host-side ARM64 `.config` with `scripts/configure-eureka-a10.sh /absolute/Eureka-Kernel /absolute/new/output-directory`. The script refuses an existing output, verifies both Git revisions, runs the A10 defconfig, enables `DEVTMPFS`, `DEVTMPFS_MOUNT`, and `FHANDLE`, clears `UEVENT_HELPER_PATH`, resolves Kconfig, and asserts the early-boot settings listed in systemd 257's upstream README (including cgroups, inotify, signalfd, timerfd, epoll, UNIX sockets, sysfs, and procfs). It also asserts deprecated sysfs is disabled. This is a compatibility-oriented config experiment; it does not establish actual systemd compatibility, run Eureka's network-fetching `build.sh`, compile the kernel or package a flashable image. The exact generated config is recorded in [ARTIFACTS.md](ARTIFACTS.md).

On 2026-09-25, `bash -n` passed, and two independent runs of the updated script produced byte-identical `.config` files (141,300 bytes; SHA-256 `48fd25767b07834b739ec23d52aab62bb5f8c9bdda5f50ba8d2b1a0b4f717932`). Relative to baseline SHA-256 `1430509fa924076c9b2ffe530da691e19a5df1a5c18c7635ca833ede0f5004cc`, the resolved diff enables `FHANDLE`, `DEVTMPFS`, and `DEVTMPFS_MOUNT`, empties the legacy helper path, and Kconfig derives `EXPORTFS=y`. The generator assertions passed. At the time of that configuration-only check, no kernel compilation had occurred; the subsequent successful host build and its limits are documented below. No initramfs, DTB container, Android boot-image packaging or physical boot has been tested.

## Experimental Eureka kernel/DTB host build (2026-09-25)

The host had no system compiler packages registered with dpkg, and package installation was not attempted. Signed Ubuntu Noble snapshot indexes for `https://snapshot.ubuntu.com/ubuntu/20260828T000000Z/` were fetched into ignored `work/apt/`; selected `.deb` packages (Clang/LLVM 14.0.6, LLD 14, GNU AArch64 binutils 2.42, Flex, Bison, `bc`, OpenSSL and ELF/zlib/zstd development files) were downloaded and extracted under `work/apt/stage`. All downloaded package bytes are SHA-256 listed in `work/apt/packages.sha256`; versions are pinned in the package filenames. Nothing was installed system-wide. The successful build environment needed `PATH` to include `work/apt/stage/usr/lib/llvm-14/bin` and `work/apt/stage/usr/bin`, `LD_LIBRARY_PATH` to include `work/apt/stage/usr/lib/x86_64-linux-gnu` and `work/apt/stage/usr/lib/llvm-14/lib`, and the corresponding extracted include/library paths.

The pinned source is `reference/inputs/eureka-r24u` at `e1b8464bb29ce5bcb9d52bfcfc71bc2563e12563` (third-party Eureka `R24U`), with KernelSU submodule `109442f8c4c7692af6562bdad6fd9f39dc1f935b`. Build outputs were kept out of this nested source tree in ignored `work/eureka-kernel-build/`. With the generated config copied to `work/eureka-kernel-build/.config`, the executed build sequence was:

```sh
make -C reference/inputs/eureka-r24u \
  O="$PWD/work/eureka-kernel-build" ARCH=arm64 LLVM=1 LLVM_IAS=1 \
  CROSS_COMPILE=aarch64-linux-gnu- CLANG_TRIPLE=aarch64-linux-gnu- olddefconfig
make -C reference/inputs/eureka-r24u \
  O="$PWD/work/eureka-kernel-build" ARCH=arm64 LLVM=1 LLVM_IAS=1 \
  CROSS_COMPILE=aarch64-linux-gnu- CLANG_TRIPLE=aarch64-linux-gnu- -j2 Image modules
make -C reference/inputs/eureka-r24u \
  O="$PWD/work/eureka-kernel-build" ARCH=arm64 LLVM=1 LLVM_IAS=1 \
  CROSS_COMPILE=aarch64-linux-gnu- CLANG_TRIPLE=aarch64-linux-gnu- -j2 dtbs
```

Host evidence: `make` completed the `Image modules` target; `file` recognized `arch/arm64/boot/Image` as an ARM64 little-endian 4K-page Linux boot executable and `vmlinux` as an AArch64 ELF; `make kernelrelease` with the same toolchain environment returned `4.4.302-p6-Eureka_R24U`. The separate `dtbs` target compiled the generic `exynos7885.dtb` and seven A10 overlays including `exynos7884B-a10_swa_open_00.dtbo`. Decompiling that overlay with the kernel's host `scripts/dtc/dtc` showed compatible values `samsung,A10 SWA OPEN 00` and `samsung,EXYNOS7884B`. This links a plausible SLK-region family overlay to A10/Exynos7884B naming only; the exact stock build, firmware overlay selection, and phone compatibility remain unverified.

The Image is 27,853,024 bytes, SHA-256 `25b9bd876efd635d43fdf5903b455717863a837fdf08dab0049b4372898fea43`; `.config` is SHA-256 `48fd25767b07834b739ec23d52aab62bb5f8c9bdda5f50ba8d2b1a0b4f717932`; `System.map` is SHA-256 `d832beb1bdfb3c71290b52e37dbb4decbb695870c658fe6380becebf06b73292`. Full logs, DTBs/DTBOs and package checksum list are in the Drive artifact recorded in `docs/ARTIFACTS.md`.

The build log contains two compiler warnings (unused `res` in `net/ipv4/tcp.c:1100` and unused `ts` in `drivers/input/touchscreen/sec_incell_ts/sec_ts_fn.c:1591`), the upstream build's harmless missing `kernel_zip/anykernel/version` lookup, and a non-fatal DTS search warning during the Image/modules invocation. The separate DTS build passed; `MODPOST 0 modules` was reported. The output config enables `CONFIG_KSU=y`, an Android-root integration that is not justified for the Debian objective. This kernel is a compiler/toolchain and candidate-driver-source experiment only: **do not deploy it**. It lacks a Debian rootfs, initramfs, verified boot packaging, exact Samsung stock inputs, security review, emulator/device validation, and recovery evidence. Linux 4.4 is an unresolved security/modern-userspace compatibility risk.

The current rootfs host blocker was rechecked in this session: `/usr/bin/unshare --user --map-root-user true` fails because `/proc/self/uid_map` returns `Operation not permitted`; there is no `mmdebstrap`, `debootstrap`, `qemu-aarch64-static`, registered AArch64 binfmt handler or Debian archive keyring. Debian mirror HTTPS was reachable, but that alone does not create a trusted ARM64 rootfs build. The scratch-only compiler staging enabled the candidate kernel build, not Debian rootfs construction. Do not claim a rootfs exists.
