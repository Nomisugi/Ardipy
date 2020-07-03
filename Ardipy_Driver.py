# -*- coding: utf-8 -*-
"""
@file Arduino_Driver01.py
@version 1.0
@author NSugi
@date 06/26/2020
@brief 
@details ArduinoとPythonの簡易接続用ドライバ
@warning 
@note Arduinoに"Ardipy.ino"を書き込んでおく必要あり
      Thread Serialの相性が悪いため、クリティカルセクションで実装
      改行コードなど機種問題も多いため、readlineなどは使わず "!"が改行目印
      Python version3以降対応
      Ardipyとのversionを合わせる必要ありversion=[major version].[minor version]
      major versionが一緒であれば互換性ありで動作可能
"""
#==========================================================================
# IMPORTS
#==========================================================================
import sys
import serial
import binascii
import time

Arduino_FW_Version = "1.0"

class ConnectException(Exception):
    pass

class Ardipy:
    def __init__(self, log):
        self.log = log
        self.ser = serial.Serial()
        self.ser.baudrate = 921600
        
    #==========================================================================
    # MAIN PROGRAM
    #==========================================================================
    def autoConnect(self):
        for i in range(100):
            com_str = 'COM%d'%i
            try:
                self.ser.port = com_str
                self.ser.open()
                break
            except:
                i = i
        time.sleep(2)
        if self.ser.port == 'COM99':
            raise ConnectException()

        #Version Check
        if( self.versionCheck() == False ):
            raise ConnectException()
        return com_str

    def connect(self, comm_num):
        try:
            self.ser.port = comm_num
            self.ser.open()
        except:
            raise ConnectException()
        time.sleep(2)
        if( ar.versionCheck() == False ):
            raise ConnectException()

    def disconnect(self):
        self.ser.close()

    def reset(self):
        self.ser.write(str.encode("!"))
        data = self.ser.read(5)
        
    def i2cWrite(self, slave_addr, addr, data):
        str = "I2W:%02x:%02x:%02x:1!" % (slave_addr, addr, data)
        self.ser.write(str)
        str = self.ser.read(5)
        if( str.decode('utf-8') != '----!'):
            return True
        else:
            return False

    def i2cRead(self, slave_addr, addr):
        data = "I2R:%02x:%02x!:1" % (slave_addr, addr)
        self.ser.write(str.encode(data))
        data = self.ser.read(1)
        n = self.ser.inWaiting()
        if n: data = data + ser.read(n)
        data2 = data.decode('utf-8')
        data3 = data2.replace('!', '')
        return int(data3, 16)

    def i2cWrite_word(self, slave_addr, addr, data):
        str = "I2W:%02x:%02x:%02x:2!" % (slave_addr, addr, data)
        self.ser.write(str)
        str = self.ser.read(5)
        if( str.decode('utf-8') != '----!'):
            return True
        else:
            return False

    def i2cRead_word(self, slave_addr, addr):
        data = "I2R:%02x:%02x:2!" % (slave_addr, addr)
        self.ser.write(str.encode(data))
        data = self.ser.read(1)
        n = self.ser.inWaiting()
        if n: data = data + self.ser.read(n)
        data2 = data.decode('utf-8')
        data3 = data2.replace('!', '')
        return int(data3, 16)

    def adRead(self, port_num):
        data = "ADR:%02x!" % (port_num)
        self.ser.write(str.encode(data))
        data = self.ser.read(5)
        data2 = data.decode('utf-8')
        data3 = data2.replace('!', '')
        return int(data3, 16)

    def versionCheck(self):
        self.ser.write(str.encode('VER!'))
        data = self.ser.read(5)
#        sdata = self.readline()
        sdata = data.decode('utf-8')

        if(sdata.split('.')[0] != Arduino_FW_Version.split('.')[0] ):
            return False
        return True
        
    def sleep(self, ms):
        time.sleep(ms)

    def power(self, flag):
        print("power")

    def test(self):
        print("test")

    def readline(self):
        s = ''
        while self.ser.inWaiting():
            d = self.ser.read()
            if( d == '!'):
                return s
            s += d
        
if __name__ == "__main__":
    print("Arduino Driver Test")
    log = ""
    ar = Ardipy(log)
    ar.autoConnect()

    #I2C Check( for INA226)
    val = ar.i2cRead_word(0x40, 0x00)
    print(val)
    ar.reset()

    #AD Check
    val = ar.adRead(0x00)
    print(val)
        
            
