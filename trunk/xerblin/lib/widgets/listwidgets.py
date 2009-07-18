'''
    Copyright (C) 2004 - 2009 Simon Forman

    This file is part of Xerblin.

    Xerblin is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

'''
from Tkinter import BOTH, Listbox, SINGLE
from Tkdnd import dnd_start
from xerblin.messaging import ModelMixin, Viewer, ListModel


class SourceWrapper:
    '''
    Helper object for drag and drop.
    '''
    def __init__(self, source, widget, index=None):
        '''
        source is the object being dragged, widget is the container thats
        initialing the drag operation, and index s thu index of the item
        in the widget's model object (which presumably is a ListModel
        containing the source object.)
        '''
        self.source = source
        self.widget = widget
        self.index = index

    def dnd_end(self, target, event):
        try:
            self.widget.clear()
        except AttributeError:
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
        pass

    def dnd_motion(self, source, event):
        I = self.nearest(event.y_root - self.winfo_rooty())
        if self._dragIndex >= 0:
            self.delete(self._dragIndex)
        self._dragIndex = I
        self.insert(I, '---')

    def dnd_leave(self, source, event):
        if self._dragIndex >= 0:
            self.delete(self._dragIndex)
            self._dragIndex = -1

    def dnd_commit(self, source, event):
        i = self._dragIndex

        if i >= 0:
            self.delete(i)
            self._dragIndex = -1

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


class AbstractSequenceViewer(Viewer):

    def __init__(self, model, kcache=None):
        if kcache is None:
            kcache = {}
        Viewer.__init__(self, model)
        kcache[id(model)] = self
        self.update(kcache)

    def handle(self, message):
        if not self._checkMessage(message):
            return False
        res = message.model is self.model or self._dispatch(message)
        if res:
            self.update()
        return res

    def update(self, kidCache=None):
        '''
        Update our contents.
        '''

        old_kids = dict((id(kid.model), kid) for kid in self.children)

        if kidCache is not None:
            kidCache.update(old_kids)
            old_kids = kidCache

        new_kids = []

        for item in self.model:
            try:
                kid = old_kids[id(item)]
            except KeyError:

                if isinstance(item, ListModel):
                    kid = AbstractSequenceViewer(item, kidCache)

                elif isinstance(item, ModelMixin):
                    kid = Viewer(item)

                else:
                    continue

                old_kids[id(item)] = kid

            new_kids.append(kid)

        self.replaceChildren(new_kids)


class SequenceViewer(AbstractSequenceViewer):

    type_descriptors = {
        str:     'string:',
        unicode: 'Unicode:',
        int:     'int:',
        float:   'float:',
        list:    'list:',
        dict:    'dict:',
        tuple:   'tuple:'
        }
    other = 'other:'

    _longest = max(map(len, type_descriptors.values() + [other]))

    #Create our format string.
    fmt = '%%-%is %%s' % _longest

    def __init__(self, model, tkparent=None, parent=None, **kw):
        kw['items'] = model
        kw.setdefault('width', 55)
        self.lb = DraggyListbox(tkparent, **kw)
        self.lb.pack(expand=True, fill=BOTH)
        AbstractSequenceViewer.__init__(self, model)
        if parent is None:
            parent = ModelMixin.root
        parent.addChild(self)

    def _format(self, n):
        '''
        Return a string with a type and description of n.
        '''
        type_name = self.type_descriptors.get(type(n))
        if not type_name:
            try:
                type_name = n.__class__.__name__
                type_name = type_name[:self._longest - 3] + '..:'
            except AttributeError:
                type_name = self.other
        return self.fmt % (type_name, n)

    def _stack2view(self, stack):
        # Get up to 100 chars of each formated version of stack's contents.
        return [n[:100] for n in map(self._format, stack)]

    def update(self, kc=None):
        '''
        Update our contents.

        This implementation simply throws out all the current contents
        and puts in the new. It could be more efficient, but this works
        fairly well and is very simple.
        '''

        super(SequenceViewer, self).update(kc)

        stack = self._stack2view(self.model)

        #Get rid of the old contents.
        self.lb.delete(0, 'end')

        #And put in the new.
        self.lb.insert(0, *stack)

    def __getstate__(self):
        master = self.lb.winfo_toplevel()
        model = self.model
        return model, master

    def __setstate__(self, state):
        model, master = state
        self.__init__(model, master)


class SequenceController(SequenceViewer):

    def __init__(self, model, tkparent=None, **kw):
        kw['items'] = model
        kw.setdefault('width', 55)
        self.lb = ControllerListbox(tkparent, **kw)
        self.lb.pack(expand=True, fill='both')
        AbstractSequenceViewer.__init__(self, model)
        ModelMixin.root.addChild(self)

