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

From the workspace root, apply the included patch once to your ZMK v0.3.0 checkout. It scales vertical and horizontal scrolling to the wheel resolution requested by the host.

```sh
YUPAD_CONFIG="/absolute/path/to/yuPad43/firmware/xiao-example"
git -C zmk apply "$YUPAD_CONFIG/patches/zmk-v0.3.0-wheel-resolution.patch"
```

To build with a local copy of the driver, set `ZMK_EXTRA_MODULES` to its path.

```sh
west build -s zmk/app -b xiao_ble -d build/yupad43 -- \
  -DSHIELD=yupad43_test \
  -DZMK_CONFIG="$YUPAD_CONFIG" \
  -DZMK_EXTRA_MODULES=/absolute/path/to/zmk-driver-yupad43
```

The example uses USB and disables BLE. Keep the USB startup settings in the shield's `Kconfig.defconfig` when adapting it.

## Operation

Use one finger to move the pointer and two fingers to scroll in either direction. A quick two-finger flick keeps the page moving briefly after you lift your fingers. Touch the pad again to stop it.

The XIAO example uses a coordinate range of 1300 × 1192 and **scroll level 0 (standard)**. ZMK’s `zip_scroll_scaler 1 16` sets the rate on both axes. Pointer inertia and pinch gestures are off.

### Pinch to zoom

For apps that use Ctrl + mouse wheel to zoom, set `CONFIG_INPUT_IQS9151_2F_PINCH_ENABLE=y` in `yupad43_test.conf` and append this to `yupad43_test.keymap`. It holds Left Ctrl during a pinch. Regular two-finger scrolling still sends just the wheel.

```dts
#include <dt-bindings/zmk/keys.h>
#include <zephyr/dt-bindings/input/input-event-codes.h>

/ {
    yupad_pinch_ctrl: yupad_pinch_ctrl {
        compatible = "zmk,input-processor-behaviors";
        #input-processor-cells = <0>;
        codes = <INPUT_BTN_7>;
        bindings = <&kp LCTRL>;
    };
};

&{/trackpad_listener} {
    input-processors = <&yupad_pinch_ctrl>, <&zip_scroll_scaler 1 16>;
};
```

## Startup

At startup, the driver checks the product ID, writes the configuration, and waits for ATI (automatic electrode calibration) to complete. Keep your fingers off the touch surface during startup.

[Back to the connection and usage guide](../README.en.md)
