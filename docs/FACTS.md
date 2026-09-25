# Device and distribution facts

| Claim | State | Evidence / limitation |
| --- | --- | --- |
| Target is SM-A105F, historical SLK build A105FDDS9CWB3 | User-specified target | Exact physical device state not inspected |
| Samsung product listing gives 2 GB RAM, 32 GB storage, 3400 mAh battery, micro USB 2.0, 2.4 GHz Wi-Fi b/g/n, Bluetooth 5.0 | Published model specification | [Samsung product page](https://www.samsung.com/ie/business/smartphones/galaxy-a/galaxy-a10-sm-a105fzkubtu/); regional variants may differ |
| Samsung lists open-source package for exact build | Located, contents unverified | [Samsung source search](https://opensource.samsung.com/uploadSearch?searchValue=SM-A105F) |
| Debian 13.7 released 2026-09-12; `arm64` supported | Published | [Debian news](https://www.debian.org/News/2026/20260912), [ARM64 installation guide](https://www.debian.org/releases/trixie/arm64/) |
| Native Debian ARM64 can boot this exact phone | Unknown | Requires exact kernel/source and boot-chain analysis followed by physical testing |
| Public Eureka `R24U` tree has an A10 ARM64 build path | Host-built kernel/DTB candidate; not emulated or device tested | Pinned commit `e1b8464bb29ce5bcb9d52bfcfc71bc2563e12563`: `build.sh` selects `ARCH=arm64` and `exynos7885-a10_defconfig`. Clang 14 host build produced Image and generic Exynos7885 DTB plus seven A10 overlays including SWA. Config has `CONFIG_KSU=y`; third-party source and Linux 4.4 age are major blockers, so do not deploy. Symbols and build success establish neither exact stock correspondence nor enabled physical hardware. |
| Pinned Eureka custom A10 systemd-oriented config resolves | Host Kconfig and subsequent compilation passed | Config SHA-256 `48fd25767b07834b739ec23d52aab62bb5f8c9bdda5f50ba8d2b1a0b4f717932`; Image SHA-256 `25b9bd876efd635d43fdf5903b455717863a837fdf08dab0049b4372898fea43`. See [BUILD.md](BUILD.md), [ARTIFACTS.md](ARTIFACTS.md), and systemd's [v257 README](https://github.com/systemd/systemd/blob/v257/README). Build evidence is not runtime compatibility or phone evidence. |
| Pinned Eureka source includes A10 SWA Exynos7884B DT overlay | Local source inspected, no stock correspondence | `exynos7884B-a10_swa_open_00.dts` declares `samsung,A10 SWA OPEN 00`, includes SWA GPIO data; file SHA-256 in [SOURCES.md](SOURCES.md). Neither `SLK` mapping nor exact hardware revision has been validated. |
| Partition map, image header, stock kernel bitness, verified-boot state | Unknown | Do not use nearby device tree values as flashing targets |

Other user-supplied starting specifications (Exynos 7884B and 2 GB/32 GB) remain subject to source and device verification. The exact Wi-Fi chipset, charger, thermal stack, modem and firmware dependencies remain unknown.
