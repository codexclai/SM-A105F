# A10 battery, charging, and thermal dependency review — 2026-09-29

## Exact source and checksums

The following source is from the acquired Samsung SM-A105F SWA source archive (archive SHA-256 `5c83be7c2452d644ccda1deb898d9a54f2b3d53d3a0e66a7a394dcbf14439931`):

| File | SHA-256 |
| --- | --- |
| `vendor/drivers/battery/sec_battery.c` | `e86fe585d9aae4931b0377eb6ced6c04f0034763c8e87b47e858d504a9fd05d0` |
| `vendor/drivers/battery/sec_charger.c` | `5124f9aae3ab4a44486bd9f01c947eb07af23adda01b1c5eff05d4e0755a3154` |
| `vendor/drivers/battery/sec_fuelgauge.c` | `01442bd1779c6dbeff8741bbfad500787ce484a1476d0c868fe4ba542e288b89` |
| `vendor/drivers/thermal/samsung/exynos_tmu.c` | `3873094e0100410f5abb9f67ce63b1d90497805cc00b614b44794535ff0090eb` |
| `vendor/arch/arm64/boot/dts/exynos/dtbo/exynos7884B-a10_common.dtsi` | `b3f7ae8a2cfb47fcc0171f8797fa2110c15182643cb26e814208e2c2be625083` |
| `vendor/arch/arm64/boot/dts/exynos/dtbo/battery_data_a10_common.dtsi` | `f366a2cbef376c0e67b89fbf0f6992f26b0eb5f72820668c06c7f4fee439d9fe` |

The upstream comparison is `gregkh/linux` tag `v6.18.54`, commit `1b357ecb321392158d507b04672ffee57bfa071d`; its `drivers/thermal/samsung/exynos_tmu.c` blob SHA is `47a99b3c5395825132d916f7d0f32f0cf2dca171`.

## Function split established by source

| Function | Samsung 4.4 evidence | Linux 6.18 / Debian work |
| --- | --- | --- |
| Charge policy and safety response | `sec_battery.c` runs monitoring work and implements recharge/full state, battery temperature limits, swelling mode, OVP/UVLO response, charging disable, current reductions, and float-voltage changes. Its A10 profile provides thermal thresholds, recovery thresholds, swelling currents/voltages, and SOC/OCV tables. | These are kernel-side Samsung functions in this tree, not proof that Android user space performs the protection. The upstream port needs a supported charger/fuel-gauge/ADC path and calibrated A10 data before exposing charging. Do not replace or bypass kernel protections with a Debian daemon. |
| Charger hardware access | `sec_charger.c` exposes the Linux power-supply interface but delegates property reads/writes to `sec_hal_chg_get_property()` and `sec_hal_chg_set_property()`; it applies configured cable/charging currents. | These callbacks depend on the board-specific charger/PMIC driver and rails. Upstream S2MPU08 support remains absent, so the A10 charger path is not mapped. |
| Fuel gauge | `sec_fuelgauge.c` delegates voltage/current/capacity/temperature retrieval to `sec_hal_fg_get_property()`, then scales, clamps, and filters capacity using A10 profile data. | The sensor IC, calibration, and units must map first. A generic Linux `power_supply` consumer cannot recreate missing measurements or calibrated capacity. |
| Application reporting/policy | The kernel exports power-supply properties plus Samsung-specific sysfs attributes. The acquired Platform archive does not provide A10 Android userspace services or init configuration; a filename inventory search for battery/health/thermal/charger/power returned only unrelated Eigen files. | Exact Samsung service/daemon names and their sysfs writes remain unknown. Once kernel support exists, Debian needs telemetry/reporting; any charge-policy writer must be specified separately and must not supersede kernel thermal/charger protection. |
| SoC thermal sensors | Samsung DTS has BIG/LITTLE TMU entries at 0x10070000, G3D at 0x10074000, and thermal-zone data. All use `samsung,exynos7885-tmu`. | Linux 6.18's Exynos TMU driver match table contains Exynos3250/4210/4412/5250/5260/5420/5433/7 compatibles but no Exynos7885. Keep these sensors/zones disabled until register and trim mapping is proved. |
| AP thermistor | A10 overlay defines `samsung,sec-ap-thermistor` on Exynos ADC channel 0 with Samsung ADC and temperature arrays. Battery profile separately selects ADC thermal source and specific temperature check policy. | Do not reuse the vendor compatible or copy the calibration arrays into a generic binding without driver semantics and unit verification. This sensor is not the SoC TMU. |

## Thermal/charging pre-physical gate

The source shows safety-critical work in the Samsung kernel driver: bad battery temperature or unsafe charger health can stop charging; swelling policy can reduce charge current and float voltage. The A10 4.35 V profile and thresholds are device-specific data and are not a generic operating limit.

Before any physical boot, a replacement kernel must provide verified battery temperature/voltage/current/fuel-gauge signals, charger enable/current/voltage control, over-temperature and OVP/UVLO behavior, and SoC thermal trip handling. Debian userspace can report those values and implement separately reviewed policy, but it must not be treated as the underlying safety mechanism. No such support or behavior is currently claimed for Linux 6.18.

## Unresolved Android user-space evidence

The exact Samsung kernel archive does not include the complete Android product/vendor filesystem. The acquired Platform archive contains no matching battery, health, thermal, or charger service/init filenames. The present evidence therefore does not identify the exact Samsung Android daemon names or whether they write particular vendor sysfs attributes on this build. Keep these consumer names and interactions explicitly unknown until the matching firmware image or product source is acquired.

No DT changes, charging tests, sensor tests, or device operations occurred in this review. The phone remains untouched.
