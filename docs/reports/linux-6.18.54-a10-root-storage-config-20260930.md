# Linux 6.18.54 A10 root-storage configuration

Date: 2026-09-30  
Pinned upstream: `1b357ecb321392158d507b04672ffee57bfa071d`

## Configuration

`configs/linux/6.18.54/a10-root-storage.config` is a merge fragment for the project A10 configuration, not a complete defconfig. It enables the initramfs and devtmpfs, ext4, the MMC block layer and Synopsys DesignWare Exynos host driver, plus DOS/MBR and EFI/GPT partition parsers.

The fragment does not assert which partition table, device number, partition index, filesystem UUID, or root partition is present on the handset. The final root mapping remains unresolved. The project initramfs mounts devtmpfs itself, so `CONFIG_DEVTMPFS_MOUNT` is not required by this configuration.

## Validation performed

A clean detached worktree at the pinned Linux commit was configured with `defconfig`, merged with this fragment using `scripts/kconfig/merge_config.sh`, then normalized with `olddefconfig`. The requested options resolved to `y`; Kconfig also selected `CONFIG_MMC_DW_PLTFM=y` and `CONFIG_RD_GZIP=y`.

The following ARM64 objects compiled successfully with the available cross compiler:

| Object | Size |
| --- | ---: |
| `drivers/mmc/host/dw_mmc.o` | 264,168 bytes |
| `drivers/mmc/host/dw_mmc-pltfm.o` | 29,760 bytes |
| `drivers/mmc/host/dw_mmc-exynos.o` | 70,312 bytes |
| `fs/ext4/super.o` | 549,664 bytes |

These results establish Kconfig resolution and compilation of the listed objects only. They do not establish a complete kernel link, runtime storage enumeration, filesystem mount, root-device identity, or phone boot.

An initial attempt to build a nonexistent aggregate target `fs/ext4/ext4.o` was corrected after checking the Kbuild rules; the actual `fs/ext4/super.o` target and MMC objects completed successfully.

## PMIC transport constraint

The read-only review of the recorded Samsung S2MPU08 evidence against pinned Linux found that upstream ACPM/mailbox support is GS101-specific and expects firmware-populated shared-memory channel descriptors; it does not start the ACPM service. The existing upstream ACPM PMIC MFD client is S2MPG10-specific. A10 evidence naming ACPM channel 2 does not establish the shared-memory/mailbox resources, firmware handoff, channel completion mode, or S2MPU08 wire/register protocol compatibility. No A10 ACPM/PMIC node or regulator consumer mapping is justified until these are evidenced.

## Next validation

Run the project initramfs regression suite and validate its generated gzip/newc archive with a package-authenticated test-only ARM64 BusyBox if the verified package and QEMU-user environment are available. Such archive/readback checks are host validation, not a device boot test. Keep any observed root path unresolved until handset partition evidence is available.


## Additional root-selector check

A focused Colab harness replayed the committed root-selector acceptance/rejection assertions and shell syntax checks successfully. It is not the full project test suite. The archive extraction/readback test could not be run: this runtime has no `cpio`, `qemu-aarch64-static`, ARM64 BusyBox, or project initramfs archive; Drive is not mounted. No device or boot claim follows from the smoke check.
