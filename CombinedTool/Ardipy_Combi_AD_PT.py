# -*- coding: utf-8 -*-
"""
@file Ardipy_ADGraph.py
@version 1.2
@author NomiSugi
@date 11/11/2021
@brief 
@details Ardipy用 Ardino AD Graph viewer(GUI:Tkinter)
@warning 
@note
"""
#==========================================================================
# IMPORTS
#==========================================================================
import sys
import binascii
import re
import time
import tkinter as tk
import tkinter.ttk as ttk
sys.path.append('../')
from Ardipy_Driver import Ardipy
sys.path.append('../Tool')
from Ardipy_Frame  import Ardipy_Frame
from IOLogWindow   import IOLogFrame
sys.path.append('../ADGraph')
from Ardipy_ADGraph  import ADGraph_Frame
sys.path.append('../PortControler')
from Ardipy_PortControler  import Port_Frame

from SelectableGraph import *
from StopWatch import *
import datetime

Ardipy_Combi_Ver = "1.4"

class AdgraphException(Exception):
    pass

class Combi_Frame(Ardipy_Frame):
    def __init__(self, master):
        self.log_win = tk.Toplevel()
        self.log = IOLogFrame(self.log_win)
        self.log_win.withdraw()
        def on_closing():
            self.log_win.withdraw()
        
        self.ardipy = Ardipy(self.log)
        super().__init__(master, self.ardipy)

        def onVersion():
            tk.messagebox.showinfo("Version", Ardipy_Combi_Ver)

        def onLogWindow():
            self.log_win.deiconify()

        menubar = tk.Menu(self)
        menubar.add_cascade(label="Vrsion", command=onVersion)
        menubar.add_cascade(label="LogWindow", command=onLogWindow)        
        master.config(menu=menubar)

        nb = ttk.Notebook(master)
        nb.pack(fill='both',expand=1)
        
        adgraph = ADGraph_Frame(nb, self.ardipy)
        portcnt = Port_Frame(nb, self.ardipy)

        nb.add(portcnt, text = 'PortControler')
        nb.add(adgraph, text = 'ADGraph')

if __name__ == "__main__":
    win = tk.Tk()
    cf = Combi_Frame(win)
    win.geometry("750x600")
    win.title("Ardipy Combination viewer(ADC,PORT)")
    win.mainloop()

            
