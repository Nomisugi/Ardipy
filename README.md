# Ardipy
ArduinoとPythonを接続させて、I2CやSPI Port、ADなどをPCから操作させる事を目的とするドライバ
ArduinoをAardvarkのようなI2CとPythonのインターフェースとして利用可能です。

プログラム構成は以下となります
1. Ardipy.ino        Arudino UNO用 UARTコントロール用ソフト
2. Ardipy_driver.py  Python ドライバ(Arduino UNO)との通信
3. Ardipy_I2CRegister.py   Ardipy : Python3サンプルソフト( I2C Register Controler ) 
4. Ardipy_ADGraph.py       Ardipy : Python3サンプルソフト( ADC Graph viewer )  (動作確認用 (ADC1, ADC2のみチェック)
5. Ardipy_PortControler.py Ardipy : Python3サンプルソフト( Port Controler )  [準備中]

---GUI付属部品--- <BR>
HexSpinbox (Tkinter用 hex spinbox) <BR>
LogWindow  (Tkinter用 log 出力窓) [準備中]<BR>
<BR>
  
---現状の問題点・課題点---<BR>
UART, I2Cなどの速度設定は固定(pymate, frmateなどの使用も検討中)<BR>
SPI, PWMなどは未実装<BR>
I2CRegister : writeデータのセーブロード未実装<BR>
I2CRegister : Deviceの切り替え方法など検討中<BR>

---Pymate, Frmate対応----<BR>
  一応Pymateにも対応してみたいと思います<BR>
  Pymateは色々なことが出来すぎるので、小難しくなっているため<BR>
  Ardipyは簡潔な通信を目指します。<BR>
  そのため、細かい設定(I2C速度変更、ADポート設定ON/OFF)は出省きます。<BR>
  どうしても細かい設定をしたい場合は、Pymateを使うか、Ardino側のプログラムを<BR>
  弄るなどして、対応した方が早いです。<BR>
