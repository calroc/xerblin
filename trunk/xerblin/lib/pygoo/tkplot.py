#!/usr/bin/env python
'''
Embed a matplotlib graph in a Tkinter Frame
'''
import matplotlib
matplotlib.use('TkAgg')


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Graph:
    '''
    An utterly unsophisticated gadget whose only purpose is to embed a
    matplotlib IV graph in a Tk Frame widget for display in the GUI.

    Initialize it with the Frame widget it should embed in:

    p = Graph(someFrameWidget)

    '''
    def __init__(self, frame, title, xlabel, ylabel):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self._makePlot()
        self.canvas = FigureCanvasTkAgg(
            self.f,
            master=frame
            )
        self.tkcanvas = self.canvas.get_tk_widget()
        self.clearPlot()

    def _makePlot(self):
        self.f = Figure(figsize=(5, 4))
        self.a = self.f.add_subplot(111)

    def clearPlot(self, event=None):
        '''
        Redraw the plot without any (previously added) curves.
        '''
        self.a.clear()
        self.a.set_title(self.title)
        self.a.set_xlabel(self.xlabel)
        self.a.set_ylabel(self.ylabel)
        self.canvas.show()

    def addPlot(self, x_data, y_data, *a):
        '''
        Plot the data on the graph.  Data is simply handed off to the
        internal matplotlib plot's plot() method, so see that for details,
        but in this case it should be a two series of X and Y data. I.e.:

        (v0, v1, ..., vn), (i0, i1, ..., in))

        '''
        self.a.plot(x_data, y_data, *a)
        self.canvas.show()

    def setTitle(self, value):
        self.title = value
        self.a.set_title(self.title)
        self.canvas.show()

    def setXLabel(self, value):
        self.xlabel = value
        self.a.set_xlabel(self.xlabel)
        self.canvas.show()

    def setYLabel(self, value):
        self.ylabel = value
        self.a.set_ylabel(self.ylabel)
        self.canvas.show()

##data = range(-5, 6), [(n*n - 1000)/1000. for n in range(-50, 51, 10)]

if __name__ == '__main__':
    from Tkinter import Tk

    root = Tk()
    root.wm_title("Embedding in TK")

    plot = Graph(root, 'IV Graph', 'V (Voltage)', 'I (Current)')
    plot.tkcanvas.pack(expand=True, fill='both')

##    root.mainloop()
