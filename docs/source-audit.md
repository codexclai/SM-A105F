# Samsung SM-A105F SWA source archive verification

Archive supplied by the user: `SM-A105F_SWA_RR_Opensource.zip`

- Outer archive SHA-256: `5c83be7c2452d644ccda1deb898d9a54f2b3d53d3a0e66a7a394dcbf14439931`
- `Kernel.tar.gz` SHA-256: `e05288db460f2d0a0f86c79beac819066f4ea3baa57cf5f26b46cdf4ec3d0af2`
- `Platform.tar.gz` SHA-256: `de94b5e95ee1182435064f4cce1e1c940a1eb529aa35b4a5456692f6af503d1c`
- ZIP integrity test passed. Kernel archive is 202,050,103 bytes; Platform archive is 28,872,812 bytes.
- Kernel Makefile declares Linux 4.4.177. Samsung README instructions select `PLATFORM_VERSION=11`, `ANDROID_MAJOR_VERSION=r`, `ARCH=arm64`, `exynos7885-a10_defconfig`.
- Exact defconfig is present. It enables arm64, 4 KiB pages, OF, initrd, modules and Exynos7885; `CONFIG_INITRAMFS_SOURCE` is empty. `CONFIG_OF_OVERLAY` is not enabled.
- `arch/arm64/boot/dts/exynos/dtbo/exynos7884B-a10_swa_open_00.dts` declares compatible `samsung,A10 SWA OPEN 00` and `samsung,EXYNOS7884B`, with A10 common and SWA GPIO fragments.
- Kernel version aligns with the historical `4.4.177-2184546` candidate firmware noted in this project's private research; this does not prove the phone currently runs that firmware or authenticate the package against Samsung's signature.
- This archive is vendor source; it remains in the user attachment/session scratch because the large Codespaces browser upload detached. Do not commit or redistribute the archive.


## Build checks performed from the attached tree

- Extracted kernel tar payload: 898,743,969 uncompressed bytes.
- `ANDROID_MAJOR_VERSION=r PLATFORM_VERSION=11 make ARCH=arm64 exynos7885-a10_defconfig` succeeded on the local host; generated `.config` SHA-256 `27f3714948ad986331949100e702834fac8d08e917cf5e891c6dc6efde4261a3`. Kconfig reported choice/override warnings. Running without Android environment variables failed on recursive `fs/sdcardfs` Kconfig inclusion.
- `make ARCH=arm64 dtbs` failed before compiling device trees: source default expected `prebuilts/gcc/linux-x86/aarch64/aarch64-linux-android-4.9/bin/aarch64-linux-android-gcc`, which is not included/available. No Image/DTB/DTBO/modules resulted.
- Local tar extraction could not preserve archive UID/GID in this restricted filesystem; content extraction was retried with `--no-same-owner`.
- The host defconfig test is source/configuration evidence only, not a cross-compiled kernel build.
