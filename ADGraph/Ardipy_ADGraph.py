# -*- coding: utf-8 -*-
"""
@file Ardipy_ADGraph.py
@version 1.1
@author NomiSugi
@date 07/6/2020
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
from SelectableGraph import *

PlotNum = 80

Ardipy_ADGraph = "1.2"

class AdgraphException(Exception):
    pass

class Control_Frame(Ardipy_Frame):
    def __init__(self, master):
        self.log = None
        self.ardipy = Ardipy(self.log)
        super().__init__(master, self.ardipy)

        #Control Frame
        self.run_flag = True
        control_frame = tk.LabelFrame(master, text= "Control",relief = 'groove')
        start_button = tk.Button(control_frame, text="START/STOP", command=self.start)
        start_button.pack(side = 'left')
        control_frame.pack(side = 'top', fill = 'x')

        graph_list = ["AD0", "AD1", "AD2", "AD3", "AD4", "AD5"]
        graph_frame = ttk.Frame(master)
        self.gf = SelectableGraph(graph_frame, graph_list)
        graph_frame.pack(side = 'right', fill = 'both')
        self.gf.setGraph_Y_Range(-1, 6)
        self.update()

    def start(self):
        self.run_flag = not self.run_flag
        if( self.run_flag ):
            self.gf.start()
        else:
            self.gf.stop()
            
    def update(self):
        vals = []
        if (self.ardipy.isConnect() & self.run_flag):
            vals.append(self.ardipy.adRead(0) * (5/1024))
            vals.append(self.ardipy.adRead(1) * (5/1024))
            vals.append(self.ardipy.adRead(2) * (5/1024))
            vals.append(self.ardipy.adRead(3) * (5/1024))
            vals.append(self.ardipy.adRead(4) * (5/1024))
            vals.append(self.ardipy.adRead(5) * (5/1024))
            self.gf.setValues( vals )
        self.master.after(100, self.update)
        return
    

if __name__ == "__main__":
    win = tk.Tk()
    cf = Control_Frame(win)
    win.geometry("800x600")
    win.title("Ardipy ADC Graph viewer")
    win.mainloop()

            
