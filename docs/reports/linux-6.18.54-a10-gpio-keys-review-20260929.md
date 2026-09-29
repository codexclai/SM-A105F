# A10 GPIO keys — Linux 6.18.54 review

## Decision

Add the volume-down, volume-up, and power keys to the A10 board DTS using the Linux 6.18 generic GPIO keys binding. The evidence supports GPIO polarity, EINT function, no internal pull, Linux key codes, and the power key wake source. It does not support copying Samsung's legacy direct IRQ tuples or the complete GPIO flag word.

## Exact Samsung 4.4 evidence

- A10 common overlay: `arch/arm64/boot/dts/exynos/dtbo/exynos7884B-a10_common.dtsi`, SHA-256 `b3f7ae8a2cfb47fcc0171f8797fa2110c15182643cb26e814208e2c2be625083`.
- Key wiring: volume-down is GPA1 pin 6 / Linux key code 114; volume-up GPA1 pin 5 / code 115; power GPA1 pin 7 / code 116. Each downstream node has `gpios = <&gpa1 N 0xf>` and a separate legacy `interrupts = <N 0 0>` with `interrupt-parent = <&gpa1>`. Power has `gpio-key,wakeup = <1>`.
- Downstream pin groups `key_voldown`, `key_volup`, and `key_power` set Samsung function 0xf (EINT), pull 0, drive 0. The A10 GPIO provider advertises 3 interrupt cells for GPA1 in the vendor description.
- Samsung `drivers/input/keyboard/gpio_keys.c`, SHA-256 `cfe412ee61733cc2c0c8be62635cbcc762e490f60b5985790897af1453018b8e`, obtains the GPIO flags and sets `active_low = flags & OF_GPIO_ACTIVE_LOW`; it does not interpret the remaining `0xf` bits for polarity. Its OF parser reads the legacy direct IRQ separately and treats either `wakeup-source` or `gpio-key,wakeup` as a boolean wake source.
- Samsung `include/linux/of_gpio.h`, SHA-256 `3658a510bd54c10e6001506459113607e5fc94f7eb9eae94f0c95aa4e79aea68`, defines only active-low bit 0 and single-ended bit 1. The complete value `0xf` therefore includes two additional bits without a standard GPIO meaning in this header. Those bits are not copied into the Linux 6.18 specifier.

## Linux 6.18 mapping

- The Exynos7885 GPIO bank binding uses two GPIO cells and two interrupt cells for GPA1. Its bank is an interrupt controller, but the Samsung legacy child IRQ tuple uses three cells and cannot be carried forward as-is.
- Current `drivers/input/keyboard/gpio_keys.c` obtains each GPIO descriptor from `gpios`; if an IRQ was not supplied, it calls `gpiod_to_irq()`. The A10 nodes therefore omit legacy `interrupts` and let Linux derive the IRQ from GPA1's GPIO line.
- GPIO flag bit 0 maps to `GPIO_ACTIVE_LOW`, preserving the bit that the exact Samsung driver reads. The pull macro is checked against current Exynos pinctrl definitions: Samsung legacy pull 0 and Linux `EXYNOS_PIN_PULL_NONE` both mean no internal pull. Legacy `pin-drv = <0>` is not translated; the pins are inputs, and no upstream drive-strength conversion is evidenced as necessary.
- `gpio-key,wakeup = <1>` maps to `wakeup-source;` because the exact legacy consumer checks that property as a boolean. Only the power key is marked wake-capable, matching the A10 source.

## Validation

Validated on the existing Linux 6.18.54 Colab checkout at base source commit `1b357ecb321392158d507b04672ffee57bfa071d`. The generated 0003 patch passed `git apply --check` and applied cleanly. The A10 DTB was built with targeted `CHECK_DTBS=y` checks for `Documentation/devicetree/bindings/input/gpio-keys.yaml` and `Documentation/devicetree/bindings/pinctrl/samsung,pinctrl-pins-cfg.yaml`; each corresponding direct `dt-validate` run exited 0. Both relevant `dt_binding_check` runs exited 0 (the host reports that optional yamllint is not installed). `git diff --check` passed. Resulting A10 DTB SHA-256: `bb72f8b3769407d8aa2b61e2b057efc9a62328affea411ab9645174c9d208ab4`.

This is source/build/schema evidence only. It does not verify key events, wake behavior, or boot on physical SM-A105F hardware.
