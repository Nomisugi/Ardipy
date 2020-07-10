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
sys.path.append('../')
from Ardipy_Driver import Ardipy
sys.path.append('../Tool')
from IOLogWindow import *

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as animation
import numpy as np

PlotNum = 80

Ardipy_ADGraph = "1.0"
Initial_File = "ADCGraph.ini"

class OtherException(Exception):
    pass

class GraphWindow(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master,relief='ridge')
        self.pack()
        fig = Figure(figsize=(10.0, 8.0))  #graph size
        canvas = FigureCanvasTkAgg(fig, master=master)
        self.run_flag = False
        self.view_flags = [True,True,True,True,True,True,True,True]
        self.x = np.arange(0, 40, 0.5)  # x軸(固定の値)
        self.y1 = np.zeros(PlotNum)
        self.y2 = np.zeros(PlotNum)
        self.l = np.arange(0, 5, 0.1)   # 表示期間(FuncAnimationで指定する関数の引数になる)
        plt = fig.add_subplot(111)
        plt.set_position([0.07,0.05,0.9,0.9])
        plt.set_ylim([-0.2,5.5])
        ani = animation.FuncAnimation(fig, self.animate, self.l,
                                      init_func=self.init, interval=5, blit=True,
        )
        self.line1, = plt.plot(self.y1)
        self.line2, = plt.plot(self.y1)
        self.line1.visible = False
        canvas.get_tk_widget().pack()

        #補助線
        for i in range(6):
            plt.hlines([i], 0, PlotNum, "blue", linestyles='dashed',linewidth = 0.5, alpha = 0.5)
            plt.hlines([i+0.5], 0, PlotNum, "blue", linestyles='dashed',linewidth = 0.5, alpha = 0.2)
        
    def animate(self, i):
        if self.run_flag:
            self.line1.set_ydata(self.y1)  # update the data.
            self.line2.set_ydata(self.y2)  # update the data.
        else:
            self.line1.visible = False
        return self.line1, self.line2,

    def init(self):  # only required for blitting to give a clean slate.
        self.line1.set_ydata(self.y1)
        self.line2.set_ydata(self.y2)
        return self.line1,

    def setValues(self, y1, y2):
        self.y1 = np.insert(self.y1, 0, y1)
        self.y1 = np.delete(self.y1, PlotNum)
        self.y2 = np.insert(self.y2, 0, y2)
        self.y2 = np.delete(self.y2, PlotNum)

    def start(self):
        if self.run_flag:
            self.run_flag = False
        else:
            self.run_flag = True

    def view(self, num):
        print(num)
        if self.view_flags[num]:
            self.view_flags[num] = False
            self.line1.visible = False
        else:
            self.view_flags[num] = True
            self.line1.visible = False

class Control_Frame(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, relief='ridge')
        log = ''
        self.ardipy = Ardipy(log)

        #LogWindow
        self.log_win = tk.Toplevel()
        self.log = IOLogFrame(self.log_win)
        self.log_win.withdraw()
        def on_closing():
            self.log_win.withdraw()
        self.log_win.protocol("WM_DELETE_WINDOW", on_closing)

        #Menu Bar
        menubar = tk.Menu(master)
        master.configure(menu = menubar)
        helps = tk.Menu(menubar, tearoff = False)
        def open_log():
            self.log_win.deiconify()
        menubar.add_command(label='LogWindow', command=open_log)
        
        #Arduino Control
        arduino_frame = tk.LabelFrame(master, text= "Arduino",relief = 'groove')
        arduino_txt = tk.Entry(arduino_frame)
        arduino_txt.insert(0, "disconnect")
        arduino_txt.pack(side='left')
        arduino_frame.pack(side = 'top', fill = 'x')
        def connect_on_click():
            try:
                str = self.ardipy.autoConnect()
            except:
                print("connect error")
            arduino_txt.delete(0, tk.END)
            arduino_txt.insert(0, "connect:"+str)
            self.ardipy.reset()
        connect_button = tk.Button(arduino_frame, text="Connect", command=connect_on_click)
        connect_button.pack(side = 'left')
        def disconnect_on_click():
            self.ardipy.disconnect()
            arduino_txt.delete(0, tk.END)                
            arduino_txt.insert(0, "disconnect")
        disconnect_button = tk.Button(arduino_frame, text="Disconnect", command=disconnect_on_click)
        disconnect_button.pack(side = 'left')

        #Control Frame
        control_frame = tk.LabelFrame(master, text= "Control",relief = 'groove')
        start_button = tk.Button(control_frame, text="START/STOP", command=lambda:self.graph.start())
        start_button.pack(side = 'left')
        control_frame.pack(side = 'top', fill = 'x')
#        sc1 = SimpleCheck(control_frame, text="AD0", flag=True,
#                        command=lambda:self.graph.view(0))
#        sc1.pack(side = 'left')

        self.graph = GraphWindow(master)
        self.update()

    def update(self):
        if self.ardipy.isConnect():
            self.graph.setValues((self.ardipy.adRead(0) * (5/1024)),
                                 (self.ardipy.adRead(1))* (5/1024))
        self.master.after(50, self.update)

    

if __name__ == "__main__":
    win = tk.Tk()
    cf = Control_Frame(win)
    win.geometry("800x600")
    win.title("Ardipy ADC Graph viewer")
    win.mainloop()

            
