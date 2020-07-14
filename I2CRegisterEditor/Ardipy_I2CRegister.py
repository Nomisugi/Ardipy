# -*- coding: utf-8 -*-
"""
@file Ardipy_I2CRegister.py
@version 1.2
@author NomiSugi
@date 07/14/2020
@brief 
@details Ardipy用 Ardino I2C Register viewer(GUI:Tkinter)
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
from HexSpinbox import *

sys.path.append('../Tool')
from IOLogWindow import *

Ardipy_I2CRegister = "1.0"
Register_File = "I2CDevice_default.ini"
#Register_File = "I2CDevice_INA226.ini"

class OtherException(Exception):
    pass

# https://teratail.com/questions/138122 参考 Tkinterスクロール面倒くさい
class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, master, *args, **kw):
        tk.Frame.__init__(self, master, *args, **kw)        

        # スクロールバーの作成
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set,height=800) #サイズ変更不可対応
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # ビューをリセット
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


class I2C_register(tk.LabelFrame):
    def __init__(self, master, ardipy, slave_addr, addr, word_num, default_val, rewrite_flag, note):
        super().__init__(master,relief='ridge')
        self.pack()
        self.addr = addr
        self.ardipy = ardipy
        self.slave_addr = slave_addr
        self.addr_txt = tk.Label(self, text = "0x{:02x}".format(addr))
        self.addr_txt.pack(padx=5, side = 'left')
        self.word_num = word_num

        self.read_str =tk.StringVar()
        if(self.word_num == 1):
            self.read_str.set("0x{:02x}".format(default_val))
        else:
            self.read_str.set("0x{:04x}".format(default_val))
        read_label = tk.Label(self, textvariable = self.read_str)
        read_label.pack( side = 'left')

        self.sp1 = HexSpinbox(self, bytenum=self.word_num, width=10)
        self.sp1.set(0)        

        self.sp1.pack(fill = 'x', padx=5, side = 'left')

        def read_button_on_click():
            self.read()
        read_button = tk.Button(self, text="read", command=read_button_on_click)
        read_button.pack(side='left')
        def write_button_on_click():
            self.write()
        write_button = tk.Button(self, text="write", command=write_button_on_click)
        write_button.pack(side='left')
        if(rewrite_flag == "R"):
            write_button['state'] = tk.DISABLED
        if(rewrite_flag == "W"):
            read_button['state'] = tk.DISABLED

        note_txt = tk.Label(self, text = note)
        note_txt.pack(padx=5, side = 'left', fill=tk.X)

    def read(self):
        if(self.word_num ==1 ):
            val= self.ardipy.i2cRead( self.slave_addr, self.addr )
        else:
            val= self.ardipy.i2cRead_word( self.slave_addr, self.addr )
        self.setReadVal(val)

    def getAddrVal(self):
        return int(self.addr_txt.cget("text"), 16)

    def write(self):
        if(self.word_num ==1 ):
            self.ardipy.i2cWrite( self.slave_addr, self.addr, int(self.sp1.get()))
        else:
            self.ardipy.i2cWrite_word( self.slave_addr, self.addr,int(self.sp1.get()))

    def setReadVal(self, val):
        if(self.word_num ==1 ):
            self.read_str.set("0x{:02x}".format(val))
        else:
            self.read_str.set("0x{:04x}".format(val))

    def getWordNum(self):
        return self.word_num
            
    def writeSet(self, val):
        print("set write")

    def save(self):
        save_txt = ""
        save_txt += str(self.addr)
        write_txt = self.sp1.get()
        return 

class Control_Frame(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, relief='ridge')


        #LogWindow
        self.log_win = tk.Toplevel()
        self.log = IOLogFrame(self.log_win)
        self.log_win.withdraw()
        def on_closing():
            self.log_win.withdraw()
        self.log_win.protocol("WM_DELETE_WINDOW", on_closing)

        sys.stdout=self.log

        self.ardipy = Ardipy(self.log)

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
        
        #Register Data Read
        slave_str = ''
        self.slave_addr = 0
        regs_datas = []
        regs_gui = []
        regs_count = 0
        rf=open(Register_File, 'r')
        for line in rf:
            line = line.replace('\n','')
            ar = line.split(',')
            if re.match('^SLAVE', line):
                slave_str = ar[1]
                self.slave_addr = int(slave_str, 16)
                continue
            if re.match('^REG', line):
                regs_datas.append(line);continue
            else:
                continue

        #Slave Address
        slave_frame = tk.LabelFrame(master, text= "Slave Address",relief = 'groove')
        slave_txt = tk.Entry(slave_frame, textvariable="0x00")
        slave_txt.insert(0, slave_str)
        slave_txt.pack(side='left')
        slave_frame.pack(side = 'top', fill = 'x')

        note_frame = tk.Frame(master)
        note_frame.pack(fill = 'x')
        note = tk.Label(note_frame, text ="  Addr  Read         Write                                     note")
        note.pack(side='left')

        self.scroll_frame = VerticalScrolledFrame(master)
        for reg in regs_datas:
            r = reg.split(',')
            regs_gui.append(I2C_register(self.scroll_frame.interior, self.ardipy, self.slave_addr, int(r[1],16),
                                int(r[2],16), int(r[3],16),r[4], r[5]))
        self.scroll_frame.pack(side='top', fill = tk.BOTH)

        def all_read_on_click():
            #Registers
            self.all_read.state = "disable"
            for regg in regs_gui:
                regg.read()
            self.all_read.state = "enable"
            
        self.all_read = tk.Button(slave_frame, text="All Read", command=all_read_on_click)
        self.all_read.pack(side = 'left')
        all_write = tk.Button(slave_frame, text="All Write")        
        all_write.pack(side = 'left')

        for regg in regs_gui:
            regg.pack(fill = 'x')

    def I2C_read(self, addr):
        return self.ardipy.i2cRead_word(slave_addr, addr)

    def close(self, event):
        print("close")

if __name__ == "__main__":
    win = tk.Tk()
    cf = Control_Frame(win)
    win.geometry("400x500")
    win.title("Ardipy I2C Register Editor")
    win.mainloop()

            
