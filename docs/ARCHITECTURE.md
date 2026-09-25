# Architecture decision gate

The intended stack is necessary Samsung boot components → compatible Linux kernel and exact device tree → minimal initramfs → persistent Debian 13 `arm64` rootfs → CLI administration. This is a target architecture, not a verified boot design.

The immediate gate is kernel execution state. A 32-bit ARM kernel cannot directly run an AArch64 Debian userspace, even on a 64-bit capable SoC. A nearby recovery tree's `TARGET_ARCH=arm` is a userspace build declaration, not stock kernel evidence; Eureka's A105 build selects `ARCH=arm64`, but its compatibility with this stock firmware is unverified. Inspect the exact official Samsung release, stock boot image and device tree before choosing a kernel baseline or image format. If the stock path is ARM32, investigate a genuinely device-compatible ARM64 kernel and bootloader handoff; do not quietly switch the requested userspace to `armhf`.

At public Eureka commit `e1b8464bb29ce5bcb9d52bfcfc71bc2563e12563`, the root Makefile identifies a 4.4.302-p6 tree. Its A10 defconfig includes `CONFIG_CGROUPS`, `CONFIG_NAMESPACES`, `CONFIG_BLK_DEV_INITRD`, `CONFIG_CHARGER_S2MU005` and `CONFIG_MACH_EXYNOS7885_A10_OPEN`; the build script uses an A10-specific defconfig and a prebuilt A10 DTBO for packaging. The device tree declares ARMv8 cores and Samsung Exynos7885. These observations narrow the source comparison but do not establish the exact SM-A105F bootloader handoff, DTBO identity, Debian init compatibility, power safety or physical function. Do not execute the third-party build script without auditing its network fetches, destructive cleanup and submodules.

The custom A10 defconfig does not explicitly list every necessary feature, whereas the repository's `stock/a10_00_stock_defconfig` explicitly enables ELF execution, devtmpfs and ext4. This is not a comparison of generated `.config` files: Kconfig defaults and dependencies must be resolved in a complete checkout and the resulting config checked for Debian boot requirements before drawing conclusions about custom-kernel suitability.

Host Kconfig resolution of the pinned custom A10 defconfig on 2026-09-25 produced ARM64, ELF, ext4, initrd, namespaces and seccomp settings, but `# CONFIG_DEVTMPFS is not set`. The stock config had `CONFIG_DEVTMPFS=y`, but no stock correspondence to the user's firmware is established. [The experimental config generator](../scripts/configure-eureka-a10.sh) enabled only `DEVTMPFS` and `DEVTMPFS_MOUNT`; a second `olddefconfig` yielded exactly those two changed lines and a checksum recorded in [ARTIFACTS.md](ARTIFACTS.md). This addresses a host-visible early `/dev` prerequisite. It does not establish that this old Android-derived kernel boots Debian, meets security requirements or safely drives charging hardware.

Debian 13 ships systemd 257. Its [upstream v257 README](https://github.com/systemd/systemd/blob/v257/README) gives Linux 3.15 as minimum and 5.4 as recommended baseline; Eureka's 4.4.302-p6 falls between them. A pinned candidate Image and A10 DTB/DTBO set now compile on the host, but no systemd runtime test, QEMU boot or physical-device test occurred. The experimental config also enables `CONFIG_KSU=y`; that Android root integration is not justified for Debian and must be removed or explicitly reviewed before a Debian-oriented candidate. Investigate kernel APIs, cgroups, security maintenance, and userspace behavior before choosing a deployed baseline. A generated configuration or successful host build is not runtime compatibility evidence.

## systemd 257.13 compatibility audit — 2026-09-25

The [upstream systemd v257.13 README](https://github.com/systemd/systemd/blob/v257.13/README) says Linux 3.15 is its minimum baseline and 5.4 its recommended baseline. Eureka `4.4.302-p6` is above the minimum but below the recommended baseline; upstream says kernels below 5.4 have significant feature gaps and limited support/testing, and will receive the `old-kernel` taint. Its README also lists newer facilities that 4.4 does not provide, including pidfd and the new mount API. This is a strong compatibility/security warning, not proof that systemd cannot start.

Static comparison of the tracked KSU-disabled config `configs/eureka-r24u-sm-a105f-debian.config` with that README found:

| Requirement or feature | Candidate config / kernel | Consequence |
| --- | --- | --- |
| Core systemd settings: devtmpfs, cgroups, inotify, signalfd, timerfd, epoll, UNIX sockets, sysfs, procfs, file handles | Required settings are enabled in the recorded config | Static prerequisite check only; does not establish a successful systemd boot. |
| Legacy sysfs/hotplug | `CONFIG_SYSFS_DEPRECATED` is unset; `CONFIG_UEVENT_HELPER_PATH=""` | Matches the README's stated udev requirements. |
| Network namespaces for `PrivateNetwork=` | `CONFIG_NET_NS=y` | This namespace mechanism is configured, but service-level runtime behavior is untested. |
| User namespaces for `PrivateUsers=` | `CONFIG_USER_NS` is unset | Units relying on `PrivateUsers=` cannot obtain that isolation. Decide whether to enable it after security review or explicitly account for reduced service hardening. |
| PIDs controller in cgroup v2 | README requires Linux 4.5 or later for this feature; candidate is 4.4.302 and `CONFIG_CGROUP_PIDS` is unset | The candidate cannot provide this newer cgroup-v2 PID-control feature; resource-control coverage is limited. |
| Seccomp filtering | `CONFIG_SECCOMP=y`, `CONFIG_SECCOMP_FILTER=y` | Configured, but syscall filtering has not been exercised in a target userspace. |
| Userspace firmware loader helper | `CONFIG_FW_LOADER_USER_HELPER=y` | Contradicts the systemd README, which says userspace firmware loading is unsupported and should be disabled. Correct the Debian-oriented config/generator and rebuild before treating it as a systemd candidate. |

This is a source/configuration audit only. No Debian userspace was installed, no systemd process ran under the candidate kernel, and no QEMU OS or phone boot was tested. Track the helper setting as a confirmed config defect; preserve the current artifact as historical evidence, then make and build a separate corrected config once the workspace/build environment is available. Evaluate `CONFIG_USER_NS` as a deliberate hardening choice, not an automatic toggle.

## Mainline and newer-kernel source scan — 2026-09-25

A bounded GitHub code search of upstream [torvalds/linux](https://github.com/torvalds/linux/tree/f14572c203d57492e1d4e5d7851a3b143e083b82) found Exynos7885 SoC support files including `arch/arm64/boot/dts/exynos/exynos7885.dtsi`, `exynos7885-pinctrl.dtsi`, the Exynos7885 clock driver, and a board file for the Galaxy A8 (2018), `exynos7885-jackpotlte.dts`. Searches in that indexed upstream tree for `A105F`, `samsung,A10`, and `exynos7884B` returned no matches. This is a scoped code-search result, not proof that no relevant support exists elsewhere or under different names; the upstream material is useful SoC context but is not an SM-A105F port.

Several public Samsung universal7904 / Exynos7885 repository refs whose labels looked newer were checked by reading only the first ten lines of their `Makefile`:

| Repository ref inspected | Reported kernel baseline |
| --- | --- |
| [SamarV-121/android_kernel_samsung_universal7904, `lineage-22.2`](https://github.com/SamarV-121/android_kernel_samsung_universal7904/tree/lineage-22.2) | 4.4.302 |
| [LineageOS/android_kernel_samsung_universal7904, `lineage-18.1`](https://github.com/LineageOS/android_kernel_samsung_universal7904/tree/lineage-18.1) | 4.4.177 |
| [minhker98/android_kernel_samsung_universal7904, `master`](https://github.com/minhker98/android_kernel_samsung_universal7904/tree/master) | 4.4.177 |
| [exynos7885-dev/old_kernel_samsung_exynos7885, `lineage-18.1`](https://github.com/exynos7885-dev/old_kernel_samsung_exynos7885/tree/lineage-18.1) | 4.4.177 |
| [muhammad23012009/android_kernel_samsung_exynos7885, `Eureka-QRS-Clang`](https://github.com/muhammad23012009/android_kernel_samsung_exynos7885/tree/Eureka-QRS-Clang) | 4.4.288 |

These metadata checks do not review commits, licenses, device trees, patches, or boot compatibility. They show that the inspected branch names do not provide a newer Linux baseline. No newer exact-device kernel candidate is established by this scan. Continue pursuing a newer supportable baseline, but do not select a branch based on a LineageOS release label alone; exact SM-A105F integration and stock boot compatibility still require evidence.

The same pinned source has an `exynos7884B-a10_swa_open_00.dts` overlay whose `compatible` includes `samsung,A10 SWA OPEN 00`. The base `exynos7885.dts` declares `samsung,exynos7885`; the overlay's Exynos7884B naming is not a contradiction to resolve by guessing. Inspect the exact official Samsung source and stock DTBO/boot image to establish base/overlay relationship, revision selection and firmware correspondence. The SWA label alone cannot identify the user's current partition contents or authorize flashing.

Avoid persistent storage placement and flash targets until the exact model's partition evidence, data-preservation needs and recovery path are known. Early boot must remain diagnosable without relying on Wi-Fi alone.
