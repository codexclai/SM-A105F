# Device and distribution facts

| Claim | State | Evidence / limitation |
| --- | --- | --- |
| Target is SM-A105F, historical SLK build A105FDDS9CWB3 | User-specified target | Exact physical device state not inspected |
| Samsung product listing gives 2 GB RAM, 32 GB storage, 3400 mAh battery, micro USB 2.0, 2.4 GHz Wi-Fi b/g/n, Bluetooth 5.0 | Published model specification | [Samsung product page](https://www.samsung.com/ie/business/smartphones/galaxy-a/galaxy-a10-sm-a105fzkubtu/); regional variants may differ |
| Samsung lists open-source package for exact build | Located, contents unverified | [Samsung source search](https://opensource.samsung.com/uploadSearch?searchValue=SM-A105F) |
| Debian 13.7 released 2026-09-12; `arm64` supported | Published | [Debian news](https://www.debian.org/News/2026/20260912), [ARM64 installation guide](https://www.debian.org/releases/trixie/arm64/) |
| Native Debian ARM64 can boot this exact phone | Unknown | Requires exact kernel/source and boot-chain analysis followed by physical testing |
| Public Eureka `R24U` tree has an A10 ARM64 build path | Source inspected, not built or device tested | Pinned commit `e1b8464bb29ce5bcb9d52bfcfc71bc2563e12563`: `build.sh` selects `ARCH=arm64` and `exynos7885-a10_defconfig`, which includes cgroups, namespaces, initrd, `CONFIG_CHARGER_S2MU005`, and `CONFIG_MACH_EXYNOS7885_A10_OPEN`. Config symbols establish source intent, not enabled hardware or stock compatibility. |
| Partition map, image header, stock kernel bitness, verified-boot state | Unknown | Do not use nearby device tree values as flashing targets |

Other user-supplied starting specifications (Exynos 7884B and 2 GB/32 GB) remain subject to source and device verification. The exact Wi-Fi chipset, charger, thermal stack, modem and firmware dependencies remain unknown.
