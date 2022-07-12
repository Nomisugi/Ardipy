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
from SelectableGraph import *
from StopWatch import *
import datetime

Ardipy_ADGraph = "1.4"

class AdgraphException(Exception):
    pass

class ADGraph_Frame(tk.Frame):
    def __init__(self, master, ardipy):
        super().__init__(master)

        self.ardipy = ardipy
        self.collection_interval = 100
        self.sw1 = StopWatch("sw1")        
        self.sw1.start()
        #Control Frame
        self.run_flag = True
        control_frame = tk.LabelFrame(self, text= "Control",relief = 'groove')
        start_button = tk.Button(control_frame, text="START/STOP", command=self.start)
        start_button.pack(side = 'left')
        interval_label1 = tk.Label(control_frame, text=u'  Collection interval')
        interval_label1.pack(side='left')
        self.interval_txt = tk.Entry(control_frame, justify=tk.RIGHT, width=5)
        self.interval_txt.pack(side='left')
        self.interval_txt.insert(0, str(self.collection_interval))
        interval_label2 = tk.Label(control_frame, text=u'ms')
        interval_label2.pack(side='left')
        interval_button = tk.Button(control_frame, text="SET", command = self.frame_set)
        interval_button.pack(side = 'left')
        control_frame.pack(side = 'top', fill = 'x')

        graph_list = ["AD0", "AD1", "AD2", "AD3", "AD4", "AD5"]
        graph_frame = ttk.Frame(self)
        self.gf = SelectableGraph(graph_frame, graph_list)
        graph_frame.pack(side = 'right', fill = 'both')
        self.gf.setGraph_Y_Range(-1, 6)
        self.update()

    def frame_set(self):
        val = int(self.interval_txt.get())
        if( val > 10000 ): val = 10000
        if( val < 1 ): val = 1
        self.interval_txt.delete(0, 10)
        self.interval_txt.insert(0, str(val))
        self.collection_interval = val
        pass

    def start(self):
        self.run_flag = not self.run_flag
        if( self.run_flag ):
            self.gf.start()
        else:
            self.gf.stop()
            
    def update(self):
        before_time  = self.sw1.stop()
        
        vals = []
        if (self.ardipy.isConnect() & self.run_flag):
            vals.append(self.ardipy.adRead(0) * (5/1024))
            vals.append(self.ardipy.adRead(1) * (5/1024))
            vals.append(self.ardipy.adRead(2) * (5/1024))
            vals.append(self.ardipy.adRead(3) * (5/1024))
            vals.append(self.ardipy.adRead(4) * (5/1024))
            vals.append(self.ardipy.adRead(5) * (5/1024))
            self.gf.setValues( vals )

        current_time  = self.sw1.stop()
        interval = current_time - before_time
        interval = self.collection_interval - int(interval*1000)
        self.master.after(interval, self.update)
        return

class Control_Frame(Ardipy_Frame):
    def __init__(self, master):
        self.log = None
        self.ardipy = Ardipy(self.log)
        super().__init__(master, self.ardipy)

        adgraph = ADGraph_Frame(master, self.ardipy)
        adgraph.pack(side = 'top', fill = 'x')

if __name__ == "__main__":
    win = tk.Tk()
    cf = Control_Frame(win)
    win.geometry("750x600")
    win.title("Ardipy ADC Graph viewer")
    win.mainloop()

            
