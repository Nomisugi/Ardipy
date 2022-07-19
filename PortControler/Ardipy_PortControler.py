# -*- coding: utf-8 -*-
"""
@file Ardipy_PortControl.py
@version 1.2
@author NomiSugi
@date 6/30/2022
@brief 
@details Ardipy用 Ardino Port Controler(GUI:Tkinter)
@warning 
@note
"""
#==========================================================================
# IMPORTS
#==========================================================================
import sys
import os
import binascii
import re
import time
import tkinter as tk
import tkinter.ttk as ttk
#sys.path.append('../')
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Ardipy_Driver import Ardipy
sys.path.append('../Tool')
from Ardipy_Frame  import Ardipy_Frame
from BinEditor import *
from SelectableGraph import *

Ardipy_ADGraph = "1.2"

PortName = ["Port2","Port3","Port4","Port5","Port6","Port7","Port8","Port9"]
LT = ["solid", "dashed", "dashdot", "dotted"]

class PortCtrolException(Exception):
    pass

class PortControler(tk.Frame):
    def __init__(self, master, ardipy):
        super().__init__(master)
        BinEditFrame( self )

        self.ardipy = ardipy
        self.direction_bits = []
        self.directions = 0x00
        self.state_bits = []
        self.states = 0x00
        self.direction_frame = tk.Frame(self)
        self.direction_label = tk.Label(self.direction_frame, text=u'Direction')
        self.direction_label.pack(side='left', padx=10)
        self.direction_frame.pack(side='top')

        for i in PortName:
            btn = tk.Button(self.direction_frame,text=i+"\nIN", width=10,
                            relief='raised', command=self.callback_direct(i))
            btn.pack(side='left')
            self.direction_bits.append(btn)

        self.state_frame = tk.Frame(self)
        state_label = tk.Label(self.state_frame, text=u'PortState ')
        state_label.pack(side='left', padx=10)
        self.state_frame.pack(side='top')

        for i in PortName:
            btn = tk.Button(self.state_frame,text=i+"\nLOW", width=10,
                            relief='raised', command=self.callback_state(i))
            btn.pack(sid='left')
            btn['state'] ='disabled'
            self.state_bits.append(btn)
        
        
    def callback_direct(self, i):
        try:
            def push():
                self.directions ^= (1<<PortName.index(i))
                #All Button Delete
                for bit in self.direction_bits:
                    bit.destroy()
                self.direction_bits.clear()

                #All Button ReCreate
                for j in range(8):
                    if (self.directions & (1<<j) > 0):
                        btn = tk.Button(self.direction_frame,text=PortName[j]+"\nOUT", width=10,
                                        relief='sunken',command=self.callback_direct(PortName[j]) )
                    else:
                        btn = tk.Button(self.direction_frame,text=PortName[j]+"\nIN", width=10,
                                        relief='raised',command=self.callback_direct(PortName[j]) )
                    btn.pack(sid='left')
                    self.direction_bits.append(btn)

                self.callback_state(i)
            return push
        except:
            tk.messagebox.showerror("Conection Error", "Not connected to Arduino UNO board")
            
    def callback_state(self, i):
        try:
            def push():
                self.states ^= (1<<PortName.index(i))
                #All Button Delete
                for bit in self.state_bits:
                    bit.destroy()
                self.state_bits.clear()

                #All Button ReCreate
                for j in range(8):
                    if (self.states & (1<<j) > 0):
                        btn = tk.Button(self.state_frame,text=PortName[j]+"\nHIGH", width=10,
                                        relief='sunken',command=self.callback_state(PortName[j]) )
                    else:
                        btn = tk.Button(self.state_frame,text=PortName[j]+"\nLOW", width=10,
                                        relief='raised',command=self.callback_state(PortName[j]) )
                    btn.pack(sid='left')
                    self.state_bits.append(btn)

            #port output
            df = self.directions & (1<<PortName.index(i))
            sf = self.states & (1<<PortName.index(i))

            for j in range(len(self.state_bits)):
                if (self.directions & (1<<j) > 0):
                    self.state_bits[j]['state'] ='normal'
                else:
                    self.state_bits[j]['state'] ='disabled'

            if df > 0:
                if sf > 0:
                    self.ardipy.portOut_bit(PortName.index(i)+2, 1)
                else:
                    self.ardipy.portOut_bit(PortName.index(i)+2, 0)

            return push
        except:
            tk.messagebox.showerror("Conection Error", "Not connected to Arduino UNO board")

    def is_States(self):
        return self.states

    def is_Directions(self):
        return self.directions

    def is_Output(self):
        return self.output

class PortViewer(tk.Frame):
    def __init__(self, master, ardipy):
        super().__init__(master)
        self.ardipy = ardipy
        #Control Frame
        self.run_flag = True
        graph_list = ["Port2", "Port3", "Port4", "Port5", "port6",
                      "Port7", "Port8", "Port9"]
        self.types = [LT[0],LT[0],LT[0],LT[0],LT[0],LT[0],LT[0],LT[0]]
        graph_frame = ttk.Frame(master)

        self.port_frame = PortControler(graph_frame, self.ardipy)
        self.port_frame.pack(side = 'top', fill = 'x')

        self.gf = SelectableGraph(graph_frame, graph_list, [" "] + PortName)
        graph_frame.pack(side = 'right', fill = 'both')
        self.gf.setGraph_Y_Range(-1, 8)

        self.gf.setLineType(self.types)
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
            for i in range(len(PortName)):
                directs = self.port_frame.is_Directions()
                if( ( directs & 1<<i) == 0):
                    vals.append(self.ardipy.portIn_bit(i+2)/2+i)
                    self.types[i] = LT[0]
                else:
                    if ((self.port_frame.is_States() & 1<< i) == 0):
                        vals.append(0+i)
                    else:
                        vals.append(0.5+i)                    
                    self.types[i] = LT[1]
            self.gf.setValues( vals )
        self.gf.setLineType(self.types)
        self.master.after(100, self.update)
        return
    
class LogTest():
    def __init__(self):
        pass

    def print(self, str, state='MESSAGE'):
        pass

class Port_Frame(tk.Frame):
    def __init__(self, master, ardipy):
        super().__init__(master)

        #Control Frame
        self.run_flag = True
        self.ardipy = ardipy
        label_frame = tk.LabelFrame(self, text= "Port Control",relief = 'groove')
        label_frame.pack(side = 'top', fill = 'x')

        port_view = PortViewer(label_frame, self.ardipy)
        port_view.pack(side = 'top', fill = 'x')


class Control_Frame(Ardipy_Frame):
    def __init__(self, master):
        self.log = LogTest()
        self.ardipy = Ardipy(self.log)
        super().__init__(master, self.ardipy)

        port_frame = Port_Frame(master, self.ardipy)
        port_frame.pack(side = 'top', fill = 'x')        


if __name__ == "__main__":
    win = tk.Tk()
    cf = Control_Frame(win)
    win.geometry("750x600")
    win.title("Ardipy PortControl viewer")
    win.mainloop()

            
