# Ardipy
ArduinoとPythonを接続させて、I2CやSPI Port、ADなどを操作させる事を目的とするドライバ
ArduinoをAardvarkのようなI2CとPythonのインターフェースとして使えることを目指します。
速度は全く期待できないので、リアルタイム性が必要な場合は使うのが難しいです。

プログラム構成は以下となります
1. Ardipy.ino        Arudino UNO用 UARTコントロール用ソフト
2. Ardipy_driver.py  Python ドライバ(Arduino UNO)との通信
3. Ardipy_sample.py  Pythonサンプルソフト( Register Controler )  [準備中]

