# Ardipy
ArduinoとPythonを接続させて、I2CやSPI Port、ADなどをPCから操作させる事を目的とするドライバ
ArduinoをAardvarkのようなI2CとPythonのインターフェースとして利用可能です。
速度は全く期待できないので、リアルタイム性が必要な場合は使うのが難しいです。

プログラム構成は以下となります
1. Ardipy.ino        Arudino UNO用 UARTコントロール用ソフト
2. Ardipy_driver.py  Python ドライバ(Arduino UNO)との通信
3. Ardipy_sample.py  Pythonサンプルソフト( Register Controler )  [準備中]

現状の問題点
UART, I2Cなどの速度設定は固定
SPI, PWMなどは未実装
