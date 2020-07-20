# -*- coding: utf-8 -*-
"""
@file NormalMenuBar.py
@version 1.0
@author NSugi
@date 07/15/2020
@brief 
@details Tkinter:一般的に使うメニューバー簡易作成版
@warning 
@note 
"""

import sys
import serial
import binascii
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

Version = "1.0"
Open_type    = [('text_file','*.txt')] 
Default_dir = None

class NormalMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master)
        master.config(menu=self)

    def file_menu(self, new_cmd=None, open_cmd=None, save_cmd=None, saveas_cmd=None):
        def open_handler():
            file = filedialog.askopenfilenames(filetypes = Open_type)
            open_cmd(file)

        def save_handler():
            file = filedialog.asksaveasfilename(filetypes = Open_type)

        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label='New', command=new_cmd) if new_cmd!= None else ""
        file_menu.add_command(label='Open', command=open_handler) if open_cmd!= None else ""
        file_menu.add_command(label='Save', command=save_cmd) if save_cmd!= None else ""
        file_menu.add_command(label='Save As', command=save_handler) if saveas_cmd!= None else ""        
        self.add_cascade(label="File", menu=file_menu)

    def arduino_menu(self, connect_cmd=None, disconnect_cmd=None):
        arduino_menu = tk.Menu(self, tearoff=0)
        arduino_menu.add_command(label='Connect', command=connect_cmd) if connect_cmd!= None else ""
        arduino_menu.add_command(label='Disconnect', command=disconnect_cmd) if disconnect_cmd!= None else ""        
        self.add_cascade(label="Arduino", menu=arduino_menu)

    def log_menu(self, log_cmd=None):
        log_menu = tk.Menu(self, tearoff=0)
        log_menu.add_command(label="Log WIndow", command=log_cmd) if log_cmd!=None else ""
        self.add_cascade(label="Log", menu=log_menu)

    def version_menu(self):
        def push():
            tk.messagebox.showinfo("Version Infomation", Version)
        ver_menu = tk.Menu(self, tearoff=0)
        ver_menu.add_command(label="Version Infomation", command=push)
        self.add_cascade(label="Version", menu=ver_menu)


if __name__ == '__main__':
    def open( filename ):
        print(filename)

    def save( filename ):
        print(filename)

    def connect():
        print("connect")
    def disconnect():
        print("disconnect")
        
    win = tk.Tk()
    menu_bar=NormalMenu(win)
    menu_bar.file_menu(open_cmd=open, saveas_cmd=save)
    menu_bar.arduino_menu(connect_cmd=open, disconnect_cmd=save)
    menu_bar.log_menu()
    menu_bar.version_menu()
    win.mainloop()
