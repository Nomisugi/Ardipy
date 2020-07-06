# Ardipy
ArduinoとPythonを接続させて、I2CやSPI Port、ADなどをPCから操作させる事を目的とするドライバ
ArduinoをAardvarkのようなI2CとPythonのインターフェースとして利用可能です。

プログラム構成は以下となります
1. Ardipy.ino        Arudino UNO用 UARTコントロール用ソフト
2. Ardipy_driver.py  Python ドライバ(Arduino UNO)との通信
3. Ardipy_I2CRegister.py   Ardipy : Python3サンプルソフト( I2C Register Controler ) 
4. Ardipy_ADGraph.py       Ardipy : Python3サンプルソフト( ADC Graph viewer )  [準備中]
5. Ardipy_PortControler.py Ardipy : Python3サンプルソフト( Port Controler )  [準備中]

-付属部品[準備中]
HexSpinbox (Tkinter用 hex spinbox)
LogWindow  (Tkinter用 log 出力窓)

現状の問題点・課題点
UART, I2Cなどの速度設定は固定
SPI, PWMなどは未実装
I2CRegister : Tkinter SpinboxがHEX未対応のため使いづらい
I2CRegister : writeデータのセーブロード未実装
I2CRegister : Deviceの切り替え方法など検討中
