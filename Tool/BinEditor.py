# -*- coding: utf-8 -*-
"""
@file BinEditor.py
@version 1.0
@author NSugi
@date 07/15/2020
@brief 
@details Bin editor using Button funtion
@warning 
@note Tkinter
"""

import sys
import tkinter as tk

class BinEditFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.val = 0x00
        self.bits = []
        for i in range(8):
            btn = tk.Button(self,text=str(i), relief='raised', command=self.callback(i))
            btn.pack(sid='right')
            self.bits.append(btn)
        print("start")

    def callback(self, i):
        def push():
            self.val ^= (1<<i)
            print(self.val)

            #All Button Delete
            for bit in self.bits:
                bit.destroy()
            self.bits.clear()

            #All Button ReCreate
            for j in range(8):
                if (self.val & (1<<j) > 0):
                    btn = tk.Button(self,text=str(j), relief='sunken',
                                    command=self.callback(j) )
                else:
                    btn = tk.Button(self,text=str(j), relief='raised',
                                    command=self.callback(j) )
                btn.pack(sid='right')
                self.bits.append(btn)
        return push
        

if __name__ == "__main__":
    print("BinEditor")
    win = tk.Tk()
    be = BinEditFrame(win)
    be.pack()
    win.mainloop()
