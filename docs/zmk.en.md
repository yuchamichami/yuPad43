# Using yuPad43 with ZMK

[日本語](zmk.md) | English

Use [zmk-driver-yupad43](https://github.com/yuchamichami/zmk-driver-yupad43/blob/main/README.en.md), which includes the electrode configuration and initialization sequence for yuPad43.

The [XIAO nRF52840 example](../firmware/xiao-example/) includes a shield, configuration, keymap, and `west.yml` for ZMK v0.3.0.

## Wiring

| Signal | XIAO GPIO |
| --- | --- |
| SDA | P0.16 |
| SCL | P1.00 |
| RDY | P1.10, active-low |
| RST | P1.11 / D6. The driver uses software reset; it does not drive this pin through `reset-gpios`. |

This example uses different I²C pins from the standard D4/D5 assignment. UART0 is disabled to free P1.11. D0–D2 are unassigned in the example keymap.

When adapting the example to another keyboard, update the I²C bus and GPIO assignments. Use only one input listener for the touchpad.

## Build

Install the Zephyr SDK and the dependencies for your ZMK west workspace. The example's `west.yml` pins the driver to a specific commit. Incorporate the manifest into your workspace and run `west update`.

For a locally checked-out driver, specify its location with `ZMK_EXTRA_MODULES`:

```sh
west build -s zmk/app -b xiao_ble -d build/yupad43 -- \
  -DSHIELD=yupad43_test \
  -DZMK_CONFIG=/absolute/path/to/yuPad43/firmware/xiao-example \
  -DZMK_EXTRA_MODULES=/absolute/path/to/zmk-driver-yupad43
```

The example uses USB and disables BLE. Keep the USB startup settings in the shield's `Kconfig.defconfig` when adapting it.

## Operation

Use one finger to move the pointer and two fingers to scroll vertically or horizontally. Scroll level **0 (standard)** is the default. Pointer and scroll inertia are disabled.

At startup, the driver checks the product ID, writes the configuration, and waits for ATI (automatic electrode calibration) to complete. Keep your fingers off the touch surface during startup.

[Back to the connection and usage guide](../README.en.md)
