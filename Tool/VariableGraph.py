import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
import math

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as animation

class GraphFrame(ttk.Frame):
    def __init__(self, master, graph_num):
        #Graph view
        fig = Figure()
        canvas = FigureCanvasTkAgg(fig, master=master)
        self.x = np.arange(0, 10, 0.1)
        self.y_datas = []
        for y in range(graph_num):
            print(y)
            self.y_datas.append( np.zeros(100) )
        l = np.arange(0, 10, 0.01)
        plt = fig.add_subplot(111)
        plt.set_ylim([-2, 2])
        plt.set_position([0.07, 0.05, 0.9, 0.9])
        self.lines = []
        for y in range(graph_num):
            yp, = plt.plot(self.y_datas[y])
            self.lines.append( yp, )

        ani = animation.FuncAnimation(fig, self.animate, l,
                                      interval=20, blit=True,
        )
        canvas.get_tk_widget().pack()

    def animate(self, i):
        count = 0
        for line in self.lines:
            line.set_ydata(self.y_datas[count])
            count+=1
        return self.lines[0:]

    def setValues(self, vals):
        count = 0
        for val in vals:
            self.y_datas[count] = np.append(self.y_datas[count], val)
            self.y_datas[count] = np.delete(self.y_datas[count], 0)
            count+=1

class DataUpdateGraph(ttk.Frame):
    def __init__(self, master):
        self.test_count = 0
        self.graph_num = 3
        #Selectable lines
        self.master = master

        graph_frame = ttk.Frame(self)
        self.gf =GraphFrame(graph_frame, self.graph_num)
        graph_frame.pack(side = 'right', fill = 'x')

        self.update()

    def update(self):
        vals = []
        vals.append( math.sin(math.radians(10*self.test_count)))
        vals.append( math.cos(math.radians(10*self.test_count)))
        vals.append( math.tan(math.radians(10*self.test_count)))                
        self.gf.setValues( vals )
        self.test_count+=1
        self.master.after(100, self.update)


if __name__ == "__main__":
    win = tk.Tk()
    gh = DataUpdateGraph(win)
    win.mainloop()
    
