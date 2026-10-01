# Linux 6.18.54 A10 reset and poweroff object build — 2026-10-01

The existing Exynos7885 description supplies the shared `syscon-reboot` and `syscon-poweroff` devices. This check compiles their generic Linux drivers; it does not alter the DT or claim physical reset/poweroff behavior.

## Build provenance

- Upstream base: Linux 6.18.54 commit `1b357ecb321392158d507b04672ffee57bfa071d`.
- Patched source tree: `/content/work/rtc-wt`, containing project patches 0001–0007, HEAD `de8e7b276be88516858fb4f0bf7d9e050fc854b1`.
- `.config` SHA-256: `c91f12ee48b24734246afb03dd5a357c23d4ba0a0d7be6dc5d3dffb8c90006e`.
- Relevant options resolved to `y`: `CONFIG_POWER_RESET_SYSCON`, `CONFIG_POWER_RESET_SYSCON_POWEROFF`, `CONFIG_RTC_CLASS`, `CONFIG_RTC_DRV_S3C`, `CONFIG_WATCHDOG`, `CONFIG_S3C2410_WATCHDOG`, `CONFIG_SERIAL_SAMSUNG_CONSOLE`, and `CONFIG_MMC_DW_EXYNOS`.

The first direct object-build attempt stalled in Kconfig `syncconfig` while asking about newly introduced ARM64 symbols. The retry supplied empty responses so Kconfig used its displayed defaults. The resulting config retained the hash and required selections above; the build then completed.

## Result

Command:

```sh
yes '' | make -j2 ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- \
  drivers/power/reset/syscon-reboot.o \
  drivers/power/reset/syscon-poweroff.o
```

Exit status: 0.

- `drivers/power/reset/syscon-reboot.o`: AArch64 ELF relocatable; SHA-256 `466e6bd37a8bc7c7fa82b4cde9d2eaa9b2298545ddb509b0773b18eebd7c0600`.
- `drivers/power/reset/syscon-poweroff.o`: AArch64 ELF relocatable; SHA-256 `e38d16aa0f8d562aa79cde430c4fb48d3ecd80f04c886c508d02f196c88a2831`.
- `git diff --check`: passed; patched source worktree clean.

These are build results only. No reset, poweroff, or other behavior was tested on the handset.

The separate full arm64 DT schema sweep is still running in the pinned six-patch tree. It has compiled the A10 DTB and has not shown an A10-specific schema diagnostic in the log so far; global completion and exit status remain pending.