# ZMKで使う

日本語 | [English](zmk.en.md)

[zmk-driver-yupad43](https://github.com/yuchamichami/zmk-driver-yupad43) を使用します。yuPad43の電極設定と初期化処理を含むZMKモジュールです。

[firmware/xiao-example](../firmware/xiao-example/) にXIAO nRF52840用のshield、conf、keymap、west.ymlを収録しています。基準はZMK v0.3.0です。別キーボードへの移植ではI²CバスとGPIOを変更し、ホスト側に既存のinput-listenerがある場合は二重登録を避けてください。

| 実機確認時のXIAO配線 | GPIO |
| --- | --- |
| SDA | P0.16 |
| SCL | P1.00 |
| RDY | P1.10（active-low） |
| RSTの配線先 | P1.11 / D6。ドライバはソフトリセットを使用し、reset-gpiosによる駆動はしていません。 |

この例は標準のD4/D5 I²C配線ではありません。P1.11と競合するUART0を無効にしています。キーマップのD0〜D2は未割当です。

ドライバは別リポジトリです。付属の `west.yml` は検証基準のコミットを固定して取得します。

既存のwest環境では、設定例のmanifestを取り込んで `west update` を実行してください。手動で取得したモジュールを使う場合は、以下の `ZMK_EXTRA_MODULES` にその保存先を指定します。

```sh
west build -s zmk/app -b xiao_ble -d build/yupad43 -- \
  -DSHIELD=yupad43_test \
  -DZMK_CONFIG=/absolute/path/to/yuPad43/firmware/xiao-example \
  -DZMK_EXTRA_MODULES=/absolute/path/to/zmk-driver-yupad43
```

Zephyr SDKとwestの依存取得が済んだ環境で実行してください。この設定例はUSB用で、BLEは無効です。

XIAO用shieldの `Kconfig.defconfig` にはUSB起動に必要な設定が含まれるため、移植時も引き継いでください。

## カーソルとスクロール

1本指でカーソルを動かし、2本指で縦横にスクロールします。2本指で軽く弾くと、指を離した後も少しスクロールが続きます。止めたいときはパッドに触れてください。

設定例の座標範囲は1300 × 1192、スクロール量は **0（標準）** です。縦横の倍率はZMKの `zip_scroll_scaler 1 16` で設定します。カーソル慣性とピンチ操作は無効です。

### ピンチでズームする

Ctrl＋ホイールでズームできるアプリ向けの設定です。XIAOの `yupad43_test.conf` を `CONFIG_INPUT_IQS9151_2F_PINCH_ENABLE=y` に変更し、次を `yupad43_test.keymap` の末尾に追加します。ピンチ中だけ左Ctrlを押した状態になり、普通の2本指スクロールではホイールだけを送ります。

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

## 起動と校正

起動時は製品番号の確認、設定書込み、ATI（電極の自動校正）の完了待ちを行います。起動中はタッチ面から指を離してください。

[別のキーボードへの組み込み用プロンプト](zmk-integration-prompt.md)

[接続・使い方へ戻る](../README.md)

