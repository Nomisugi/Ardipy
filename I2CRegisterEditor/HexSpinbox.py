# -*- coding: utf-8 -*-
"""
@file HexSpinbox.py
@version 1.0
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
        

if __name__ == "__main__":
    print("HexSpinbox")
    win = tk.Tk()
    sptxt1 = tk.StringVar()
    sptxt1.set(10)
    sp = tk.Spinbox(win,textvariable=sptxt1,from_=-10,to=10,increment=1)
    sp.pack()

    hsp = HexSpinboxChar(win)
    hsp.set(0x55)
    print(hsp.get())
    hsp.pack()

    hwsp = HexSpinboxWord(win)
    hwsp.set(0xAAAA)
    print(hwsp.get())
    hwsp.pack()
    

    win.geometry("200x200")
    win.title("HexSpinbox test")
    win.mainloop()