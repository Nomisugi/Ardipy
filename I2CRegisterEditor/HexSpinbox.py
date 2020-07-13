# -*- coding: utf-8 -*-
"""
@file HexSpinbox.py
@version 1.1
@author NSugi
@date 07/07/2020
@brief 
@details SpinboxのHEX版
@warning 
@note Tkinter癖がありすぎて作るの疲れた
"""

import binascii
import tkinter as tk

class HexSpinboxChar(tk.Spinbox):
    def __init__(self, *args, **kwargs):
        self.var = tk.StringVar()
        super().__init__(*args, **kwargs, textvariable=self.var, from_=0,to=0xff,
                         increment=1, command=self.cange )

    def set(self, val):
        self.var.set("0x{:02x}".format(int(val)))
        
    def get(self):
        hstr = super().get()
        return int(hstr, 16)

    def cange(self):
        val = super().get()
        self.set(val)

class HexSpinboxWord(tk.Spinbox):
    def __init__(self, *args, **kwargs):
        self.var = tk.StringVar()
        super().__init__(*args, **kwargs, textvariable=self.var, from_=0,to=0xffff,
                         increment=1, command=self.cange )

    def set(self, val):
        self.var.set("0x{:04x}".format(int(val)))
        
    def get(self):
        hstr = super().get()
        return int(hstr, 16)

    def cange(self):
        val = super().get()
        self.set(val)

#Multi Byte 
class HexSpinbox(tk.Spinbox):
    def __init__(self, *args, **kwargs):
        self.var = tk.StringVar()
        self.bytenum = kwargs.pop('bytenum')
        max_val = 0x1<<(self.bytenum*8)
        super().__init__(*args, **kwargs, textvariable=self.var, from_=0,to=max_val,
                         increment=1, command=self.cange )

    def set(self, val):
        s = "0x{:0%dx}" % (self.bytenum*2)
        self.var.set(s.format(int(val)))
        
    def get(self):
        hstr = super().get()
        return int(hstr, 16)

    def cange(self):
        val = super().get()
        self.set(val)

#Binary
class BinSpinbox(tk.Spinbox):
    def __init__(self, *args, **kwargs):
        self.var = tk.StringVar()
        super().__init__(*args, **kwargs, textvariable=self.var, from_=0,to=0xff,
                         increment=1, command=self.cange )
        self.val = 0

    def set(self, val):
        self.val = val
        self.var.set("0b{:08b}".format(int(val)))

    def get(self):
        hstr = self.var().get()
        return int(hstr, 2)

    def cange(self):
        val = super().get()
        print(val)
        if(val == '1'):
            self.val = self.val+1
            if(self.val > 0xff):
                self.val = 0x00
        else:
            if(self.val == 0x00 ):
                self.val = 0xff
            else:
                self.val = self.val-1
        self.set(self.val)


if __name__ == "__main__":
    print("HexSpinbox")
    win = tk.Tk()
    sptxt1 = tk.StringVar()
    sptxt1.set(10)
    sp = tk.Spinbox(win,textvariable=sptxt1,from_=-10,to=10,increment=1)
    sp.pack()

    hsp = HexSpinboxChar(win)
    hsp.set(0x55)
    hsp.pack()

    hwsp = HexSpinboxWord(win)
    hwsp.set(0xAAAA)
    hwsp.pack()

    h4 = HexSpinbox(win, bytenum=2)
    h4.set(0xAA55)
    h4.pack()

    b1 = HexSpinbox(win)
    b1.set(0xAA)
    b1.pack()
    
    win.geometry("200x200")
    win.title("Spinbox test")
    win.mainloop()
