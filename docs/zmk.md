# ZMKで使う

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

設定例は1本指でカーソル、2本指で縦横スクロールを操作します。スクロール量は **0（標準）** を基準とします。カーソル・スクロールの慣性は無効です。

## 起動と校正

起動時は製品番号の確認、設定書込み、ATI（電極の自動校正）の完了待ちを行います。起動中はタッチ面から指を離してください。

校正完了後のATI品質警告があっても、入力を継続します。警告による起動停止や再校正の繰り返しは行いません。ログを有効にすると警告の発生・解消を記録します。通信できない場合や校正が完了しない場合は初期化に失敗します。警告を許容する処理は、断線やはんだ不良を修復するものではありません。

ICが動作中にリセットされた場合の設定再適用は未対応です。反応がなくなった場合は電源を入れ直してください。

[接続・使い方へ戻る](../README.md)

