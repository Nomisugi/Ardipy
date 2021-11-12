
import sys
import tkinter as tk
import tkinter.ttk as ttk
sys.path.append('../')
from Ardipy_Driver import Ardipy
sys.path.append('../Tool')
from IOLogWindow import *

class Ardipy_Frame(ttk.LabelFrame):
    def __init__(self, master, ardipy):
        super().__init__(master, relief='ridge')
        log = ''
        self.ardipy = ardipy

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

        
class TestFrame(Ardipy_Frame):
    def __init__(self, master):
        log = ''
        self.ardipy = Ardipy(log)
        super().__init__(master, self.ardipy)

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

        #Test view
        Static1 = tk.Label(text=u'test', foreground='#ff0000', background='#ffaacc')
        Static1.place(x=0, y=10)        
    

if __name__ == "__main__":
    win = tk.Tk()
    cf = TestFrame(win)
    win.geometry("800x600")
    win.title("Ardipy Test")
    win.mainloop()

        
