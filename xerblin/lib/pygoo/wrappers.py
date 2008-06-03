from Tkinter import Button
from xerblin.lib.pygoo.tkplot import Graph


class GraphWrapper(object):

    def __init__(self, frame, **options):
        title = options.get('title', 'Graph')
        xlabel = options.get('xlabel', 'X-Axis')
        ylabel = options.get('ylabel', 'Y-Axis')

        self.graph = Graph(frame, title, xlabel, ylabel)
        self.grid = self.graph.tkcanvas.grid

    def setTitle(self, value):
        self.graph.setTitle(value)

    def setXLabel(self, value):
        self.graph.setXLabel(value)

    def setYLabel(self, value):
        self.graph.setYLabel(value)

    def setPlot(self, value):
        self.graph.addPlot(*value)

    def clear(self):
        self.graph.clearPlot()

    title = property(None, setTitle)
    xlabel = property(None, setXLabel)
    ylabel = property(None, setYLabel)
    plot = property(clear, setPlot)

    


##class CallbackVariable(Variable):
##    '''
##    Connects a Variable to a callback.
##    '''
##
##    def __init__(self, name, initial_value, cb):
##        super(CallbackVariable, self).__init__(name, initial_value)
##        self.cb = cb
##
##    def setValue(self, value):
##        super(CallbackVariable, self).setValue(value)
##        self.cb(value)
##
##    value = property(Variable.getValue, setValue)


class CommandWrapper:
    def __init__(self, obj, command):
        self.obj = obj
        self.command = command
    def __call__(self):
        self.obj.interpret(self.command)
    def __repr__(self):
        return '<CommandWrapper: %r>' % (self.command,)

class ButtonWrapper(Button):
    def __setitem__(self, key, value):
        if key != 'command':
            Button.__setitem__(self, key, value)
            return
        if isinstance(value, CommandWrapper):
            self._command = value
            Button.__setitem__(self, key, value)
        else:
            self._command.command = value
    def __getitem__(self, key):
        if key != 'command':
            Button.__getitem__(self, key)
            return
        return self._command.command

##    # Build an initial dictionary for our new Object.
##    D = dict(
##
##        widget=Constant('widget', button),
##
####        source=Constant('source', source),
##
##        text=CallbackVariable(
##            'text',
##            button['text'],
##            lambda text: setitem(button, 'text', text)
##            ),
##
##        command=CallbackVariable(
##            'command',
##            button['command'],
##            lambda command: setitem(button, 'command', command)
##            ),
##
##        )


if __name__ == '__main__':
    from Tkinter import _default_root, mainloop, Toplevel
    g = GraphWrapper(
        Toplevel(_default_root),
        title='a',
        xlabel='b',
        ylabel='c'
        )

    g.grid()
    ##g.graph.tkcanvas.update()

    g.plot = ([1], [1], 'ro')

##    mainloop()


