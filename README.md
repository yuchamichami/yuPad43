# yuPad43

IQS9151搭載タッチパッド **yuPad43** の接続・ファーム組込み資料です。
対象は10 RX × 9 TX、4層、板厚1.0 mmのモデルです。

[接続・組込みガイド](index.html)をブラウザで開いてください。
HTMLはダウンロード後に直接開けます。

## 収録内容

| ファイル・フォルダ | 内容 |
| --- | --- |
| [index.html](index.html) | 接続、ZMK、他ファームへの移植、出力データ、ケース設計 |
| [yuPad43-underside.svg](yuPad43-underside.svg) | 配線を省いた裏面図 |
| [yuPad43-mechanical.svg](yuPad43-mechanical.svg) | 外形・穴・コネクタの寸法図 |
| [yuPad43-mechanical.json](yuPad43-mechanical.json) | 機械寸法と部品包絡 |
| [yuPad43-case-envelope.step](yuPad43-case-envelope.step) | ケース検討用の簡略モデル |
| [yuPad43-profile.json](yuPad43-profile.json) | 初期設定ブロックと上書き設定 |
| [register-writes.csv](register-writes.csv) | 初期設定の基礎ブロック一覧 |
| [decode_frame.py](decode_frame.py) | 取得済み28バイトフレームの解釈例 |
| [yuPad43-zmk-driver](yuPad43-zmk-driver) | この基板向けの参考ドライバ |
| [yuPad43-zmk-xiao](yuPad43-zmk-xiao) | XIAO nRF52840用ZMK設定例 |

## 対応範囲

資料は販売準備中の組込み用基準版です。保存版ファームではUSBでの動作実績がありますが、
校正警告、複数個体での出荷判定、BLE、異常時の復旧には確認を残しています。
名称変更後のファーム再ビルド・実機書込みは未実施です。

外形は43.3 × 40.3 mm、板厚は1.0 mmです。
モデルの総厚3.0 mmは公称値で、はんだ・製造公差・カバー・接着材・ケーブル・ラッチ開閉空間を含みません。
STEPは基板外形と部品包絡のみで、回路図・配線・電極・Gerberは収録していません。

旧13 × 12版、2枚重ね版、CoreX用パッドとは設定が異なります。
純正TPS43用ドライバの無変更での動作を保証するものではありません。

## 使用ソフトウェア・ライセンス

ZMK用ドライバは [ShiniNet / zmk-driver-iqs9151](https://github.com/ShiniNet/zmk-driver-iqs9151)
（MIT License）を基に、yuPad43向けの電極設定・初期化設定・ATI通信処理を変更しています。

Copyright (c) 2026 ShiniNet

ライセンス全文は [THIRD-PARTY-LICENSE.txt](THIRD-PARTY-LICENSE.txt)、
出典は [source-notice.txt](source-notice.txt) を参照してください。
第三者コードのライセンスはその対象コードに適用され、基板設計の公開・利用許諾を意味しません。
