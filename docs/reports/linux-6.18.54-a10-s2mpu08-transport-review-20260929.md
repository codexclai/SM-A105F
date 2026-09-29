# A10 S2MPU08 PMIC transport and regulator review — 2026-09-29

## Scope and source identity

This review traces the exact user-supplied Samsung SM-A105F SWA source archive (ZIP SHA-256 `5c83be7c2452d644ccda1deb898d9a54f2b3d53d3a0e66a7a394dcbf14439931`) against the Linux 6.18.54 support inventory recorded in the A10 port matrix. The archive is not independently Samsung-signature authenticated. The exact DT and driver source hashes below allow this conclusion to be reproduced.

This is not PMIC, regulator, charging or device-operation validation. No handset was accessed.

## Exact A10 contract

The A10 overlay `exynos7884B-a10_common.dtsi` declares a `samsung,s2mpu08mfd` at register address 0 under an ACPM parent. It sets ACPM IPC channel 2; passes a GPA2 pin as the PMIC IRQ GPIO; enables wakeup; sets WTSR/SMPL policy; configures reset-time RTC initialization; and nests 34 regulator declarations (BUCK1–BUCK8 and LDO1–LDO14, LDO33–LDO37). The downstream regulator labels explicitly identify LDO2 as `vqmmc` (1.8–3.375 V) and LDO35 as `vmmc` (1.8–3.0 V). Those labels and ranges are evidence of the legacy platform description, not yet proof that the current eMMC host should switch to either rail.

The core driver proves that this is not ordinary register-addressed I²C from the AP:
- With `CONFIG_EXYNOS_ACPM`, its read/write/bulk/update helpers call `exynos_acpm_*_reg()` using an I²C address and register number.
- It creates dummy I²C clients for PMIC, RTC, close, and codec addresses after probing the logical parent.
- It initializes a custom interrupt controller, then instantiates regulator and RTC MFD children.
- Its OF parser consumes Samsung-specific ACPM, IRQ-GPIO, wake, WTSR/SMPL, codec-interrupt and speedy-address fields.

The regulator driver contains device-specific behavior that a generic SEC PMIC driver cannot safely inherit by name:
- BUCK5 enable/disable is deliberately ignored.
- On revision 0, LDO35 and LDO36 have a coupled-register workaround that changes external control and enable bits.
- It constructs regulator descriptors/register mappings from the S2MPU08 private header and registers them through the legacy MFD transport helpers.

Therefore the existing `MFD_SEC_I2C` support for other Samsung SEC devices does not establish an S2MPU08 implementation. The current mainline SEC I²C match data covers S2MPA01, S2MPS11/13/14/15, S2MPU02/05, S2MU005 and S5M8767; it has neither `samsung,s2mpu08mfd` nor S2MPU08 register/IRQ/regulator data. The separate SEC ACPM driver targets S2MPG1x PMICs, not this device. A compatible alias would bind the wrong register layout and bus access model.

## Source hashes

| Exact Samsung source | SHA-256 |
| --- | --- |
| `arch/arm64/boot/dts/exynos/dtbo/exynos7884B-a10_common.dtsi` | `b3f7ae8a2cfb47fcc0171f8797fa2110c15182643cb26e814208e2c2be625083` |
| `drivers/mfd/s2mpu08_core.c` | `942c2d137a3b35fde766aa1987a8d4808d59ca9e2d6434fae4217cdf410be0af` |
| `drivers/mfd/s2mpu08_irq.c` | `a3dade64ee74f5a6dcb2329e0143bb1b08fbea780ece45f839345eba808b944e` |
| `drivers/regulator/s2mpu08.c` | `c9f950bcfb46e09b451bc9694e30cb6a2ea847438a07a819dc2281a9aa418693` |
| `drivers/rtc/rtc-s2mpu08.c` | `2fdcaf26f94897ac29fc7d2fe4a0177ed48ce0d3268e0f04dce320a7d930775a` |

Relevant Linux 6.18.54 sources already examined in the port review include `drivers/mfd/sec-i2c.c`, `drivers/mfd/sec-acpm.c`, `drivers/mfd/sec-core.c`, `drivers/regulator/s2mps11.c`, `drivers/rtc/rtc-s5m.c`, and the SEC PMIC binding schemas. The nearby upstream devices are not substitutes for the exact S2MPU08 transport and register definitions.

## Port decision

No S2MPU08 node, dummy/fixed replacement rails, or compatible alias is added to the A10 Linux 6.18 DTS. This keeps boot-critical voltage dependencies honest. In particular, do not enable eMMC high-speed voltage switching, USB PHY/role operation, or battery/charger control on the assumption that the legacy rail names alone provide a working regulator.

A Linux 6.18 port requires, at minimum:
1. A supported description of the ACPM interface exposed to this boot path, including whether required firmware/service is present and its protocol contract. Samsung's private Android ACPM implementation cannot be assumed to exist in a Linux 6.18 Debian boot.
2. A maintained MFD/regmap/IRQ implementation for S2MPU08 with revision and multi-address behavior defined.
3. Regulator and RTC children with current bindings, validated register tables, and explicit handling for the BUCK5 and LDO35/LDO36 special cases.
4. Evidence that the SoC pin/interrupt topology and wake semantics map to the current GPIO/IRQ framework.
5. A regulator consumer map and safe startup voltage policy; only then can MMC/USB/thermal/charging dependencies be considered.

This is a researched blocker, not a claim that hardware is impossible to support. The next independent port task can proceed without guessing this subsystem.
