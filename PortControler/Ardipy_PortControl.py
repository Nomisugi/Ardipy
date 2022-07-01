# -*- coding: utf-8 -*-
"""
@file Ardipy_PortControl.py
@version 1.0
@author NomiSugi
@date 11/12/2021
@brief 
@details Ardipy用 Ardino Port Controler(GUI:Tkinter)
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
from BinEditor import *
from SelectableGraph import *

Ardipy_ADGraph = "1.2"

PortName = ["Port2","Port3","Port4","Port5","Port6","Port7","Port8","Port9"]

class PortCtrolException(Exception):
    pass

class PortControler(tk.Frame):
    def __init__(self, master, ardiyp):
        super().__init__(master)
        BinEditFrame( self )
        self.direction_bits = []
        self.state_bits = []        
        self.val = 0x00
        self.direction_frame = tk.Frame(self)
        self.direction_label = tk.Label(self.direction_frame, text=u'Direction')
        self.direction_label.pack(side='left', padx=10)
        self.direction_frame.pack(side='top')

        for i in PortName:
            btn = tk.Button(self.direction_frame,text=i+"\nIN", width=10,
                            relief='raised', command=self.callback(i))
            btn.pack(side='left')
            self.direction_bits.append(btn)

        self.state_frame = tk.Frame(self)
        state_label = tk.Label(self.state_frame, text=u'PortState ')
        state_label.pack(side='left', padx=10)
        self.state_frame.pack(side='top')

        for i in PortName:
            btn = tk.Button(self.state_frame,text=i+"\nNone", width=10,
                            relief='raised', command=self.callback_state(i))
            btn.pack(sid='left')
            self.state_bits.append(btn)
        
        
    def callback(self, i):
        def push():
            self.val ^= (1<<PortName.index(i))
            
            #All Button Delete
            for bit in self.direction_bits:
                bit.destroy()
            self.direction_bits.clear()

            #All Button ReCreate
            for j in range(8):
                if (self.val & (1<<j) > 0):
                    btn = tk.Button(self.direction_frame,text=PortName[j]+"\nOUT", width=10,
                                    relief='sunken',command=self.callback(PortName[j]) )
                else:
                    btn = tk.Button(self.direction_frame,text=PortName[j]+"\nIN", width=10,
                                    relief='raised',command=self.callback(PortName[j]) )
                btn.pack(sid='left')
                self.direction_bits.append(btn)
        return push

    def callback_state(self, i):
        def push():
            self.val ^= (1<<PortName.index(i))
            
            #All Button Delete
            for bit in self.state_bits:
                bit.destroy()
            self.state_bits.clear()

            #All Button ReCreate
            for j in range(8):
                if (self.val & (1<<j) > 0):
                    btn = tk.Button(self.state_frame,text=PortName[j]+"\nHIGH", width=10,
                                    relief='sunken',command=self.callback_state(PortName[j]) )
                else:
                    btn = tk.Button(self.state_frame,text=PortName[j]+"\nLOW", width=10,
                                    relief='raised',command=self.callback_state(PortName[j]) )
                btn.pack(sid='left')
                self.state_bits.append(btn)
        return push
    
    
class LogTest():
    def __init__(self):
        pass

    def print(self, str, state='MESSAGE'):
        pass

class Control_Frame(Ardipy_Frame):
    def __init__(self, master):
        self.log = LogTest()
        self.ardipy = Ardipy(self.log)
        super().__init__(master, self.ardipy)

        #Control Frame
        self.run_flag = True
        control_frame = tk.LabelFrame(master, text= "Port Control",relief = 'groove')
        port_frame = PortControler(control_frame, self.ardipy)
        port_frame.pack(side = 'top', fill = 'x')
#        start_button = tk.Button(control_frame, text="START/STOP", command=self.start)
#        start_button.pack(side = 'left')
        control_frame.pack(side = 'top', fill = 'x')

        graph_list = ["Port2", "Port3", "Port4", "Port5", "port6",
                      "Port7", "Port8", "Port9"]
        graph_frame = ttk.Frame(master)
        self.gf = SelectableGraph(graph_frame, graph_list)
        graph_frame.pack(side = 'right', fill = 'both')
        self.gf.setGraph_Y_Range(-1, 8)
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
            vals.append(self.ardipy.portIn_bit(2)/2)
            vals.append(self.ardipy.portIn_bit(3)/2+1)
            vals.append(self.ardipy.portIn_bit(4)/2+2)
            vals.append(self.ardipy.portIn_bit(5)/2+3)
            vals.append(self.ardipy.portIn_bit(6)/2+4)
            vals.append(self.ardipy.portIn_bit(7)/2+5)
            vals.append(self.ardipy.portIn_bit(8)/2+6)
            vals.append(self.ardipy.portIn_bit(9)/2+7)            
            self.gf.setValues( vals )
        self.master.after(100, self.update)
        return
    

if __name__ == "__main__":
    win = tk.Tk()
    cf = Control_Frame(win)
    win.geometry("750x600")
    win.title("Ardipy PortControl viewer")
    win.mainloop()

            
