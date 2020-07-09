# -*- coding: utf-8 -*-
"""
@file IOLogWindows.py
@version 1.0
@author NSugi
@date 07/09/2020
@brief 
@details Tkinter:Input/Outpu用 Logwindow
@warning 
@note Tkinterでは通常ログなどリアルタイムに出力できないためDEBUG用
      エレガントなソースにできない...tkinterに苦戦...

"""
#==========================================================================
# IMPORTS
#==========================================================================
import sys
import serial
import binascii
import time
import tkinter as tk
from tkinter import scrolledtext

TEXT_COLORS = {
    'MESSAGE' : 'black',
    'INPUT' : 'blue',
    'OUTPUT' : 'green',
    'ERROR' : 'red',
    'DEBUG' : 'yellow'    
    }

class IOLogWindow(tk.Frame):
    def __init__(self, master=None):    
        tk.Frame.__init__(self, master)
        master.title("Log Window")

        #view/hide choice
        select_frame = tk.LabelFrame(master, text= "Log text selection",relief = 'groove')

        #MESSAGE
        var1 = tk.BooleanVar()
        schk1 = tk.Checkbutton(select_frame, variable=var1, text='MESSAGE',
           command=lambda : self.hide('MESSAGE') if var1.get() else self.view('MESSAGE')
        )
        schk1.pack(side='left')

        #INPUT
        var2 = tk.BooleanVar()
        schk2 = tk.Checkbutton(select_frame, variable=var2, text='INPUT',
           command=lambda : self.hide('INPUT') if var2.get() else self.view('INPUT')
        )
        schk2.pack(side='left')

        #OUTPUT
        var3 = tk.BooleanVar()
        schk3 = tk.Checkbutton(select_frame, variable=var3, text='OUTPUT',
           command=lambda : self.hide('OUTPUT') if var3.get() else self.view('OUTPUT')
        )
        schk3.pack(side='left')

        #ERROR
        var4 = tk.BooleanVar()
        schk4 = tk.Checkbutton(select_frame, variable=var4, text='ERROR',
           command=lambda : self.hide('ERROR') if var4.get() else self.view('ERROR')
        )
        schk4.pack(side='left')

        select_frame.pack(side = 'top', fill = 'x')

        
        self.txt = scrolledtext.ScrolledText(win)
        self.txt.pack(fill=tk.BOTH, expand=1)
        for key in TEXT_COLORS:
            self.txt.tag_config(key, foreground=TEXT_COLORS[key])

    def print(self, str, state='MESSAGE'):
        self.txt.insert(tk.END, str+'\n', state)

    def hide(self, tag):
        self.txt.tag_config(tag, elide=True)

    def view(self, tag):
        self.txt.tag_config(tag, elide=False)


if __name__ == '__main__':
    win = tk.Tk()
    io=IOLogWindow(win)
    io.print("Message")
    io.print("--ERROR--", 'ERROR')
    io.print("--INPUT--", 'INPUT')
    io.print("--OUTPUT--", 'OUTPUT')
    io.print("消えたり消えなかったり")    
    win.mainloop()
    
