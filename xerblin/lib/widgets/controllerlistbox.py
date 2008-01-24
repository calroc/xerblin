from Tkinter import Listbox, SINGLE
from Tkdnd import dnd_start


class SourceWrapper:
    def __init__(self, source, widget, index=None):
        self.source = source
        self.widget = widget
        self.index = index

    def dnd_end(self, target, event):
        try:
            self.widget.clear()
        except AttributeError:
            pass
        pass


class DraggyListbox(Listbox):

    def __init__(self, master=None, **kw):

        # Get our stack.
        self.stack = kw.pop('items')

        # Override any passed in selectmode.
        kw['selectmode'] = SINGLE

        Listbox.__init__(self, master, **kw)

        self.bind('<Button-1>', self.startDrag)
        self.bind('<ButtonRelease-1>', self.clear)

    def clear(self, event=None):
        i = self.curselection()
        if i:
            i = int(i[0])
            self.selection_clear(i)

    def startDrag(self, event):
        i = self.nearest(event.y)
        if i >= 0:
            self.selection_set(i)
            source = self.stack[i]
            source = SourceWrapper(source, self, i)
            event.num = 1 # Don't ask. (See Tkdnd.py)
            dnd_start(source, event)
        return "break"


class ControllerListbox(DraggyListbox):

    def __init__(self, master=None, **kw):
        DraggyListbox.__init__(self, master, **kw)
        self._dragIndex = -1

    def dnd_accept(self, source, event):
        self.focus_force()
        return self

    def dnd_enter(self, source, event):
##        print 'dnd_enter', self, source, event
        pass

    def dnd_motion(self, source, event):
        if self._dragIndex >= 0:
            self.delete(self._dragIndex)
        I = self.nearest(event.y_root - self.winfo_rooty())
        self._dragIndex = I
        self.insert(I, '---')
##        print 'dnd_motion'#, self, source, event
        pass

    def dnd_leave(self, source, event):
        if self._dragIndex >= 0:
            self.delete(self._dragIndex)
            self._dragIndex = -1
##        print 'dnd_leave', self, source, event
        pass

    def dnd_commit(self, source, event):
        if self._dragIndex >= 0:
            self.delete(self._dragIndex)
            self._dragIndex = -1
##        print 'dnd_commit', repr(self), source, event
        y = event.y_root - self.winfo_rooty()
        i = self.nearest(y)

        try:
            if self is source.widget:

                # Don't duplicate something by dropping it on itself.
                if i == source.index:
                    return

                # Instead, move it by removing it before the pending append.
                del self.stack[source.index]
                if i > source.index:
                    i -= 1

            self.stack.insert(i, source.source)

        finally:
            self.clear()

