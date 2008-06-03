from Tkinter import Toplevel, BOTH

from xerblin.messaging import ModelMixin, Viewer, ListModel
from xerblin.lib.widgets.controllerlistbox import (
    DraggyListbox,
    ControllerListbox,
    )
from xerblin.lib.widgets.widgetwrapper import MakeViewer


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


def _format(n):
    '''
    Return a string with a type and description of n.
    '''
    type_name = type_descriptors.get(type(n))
    if not type_name:
        try:
            type_name = n.__class__.__name__
            type_name = type_name[:_longest - 3] + '..:'
        except AttributeError:
            type_name = other
    return fmt % (type_name, n)


def stack2view(stack):
    # Get up to 100 chars of each formated version of stack's contents.
    return [n[:100] for n in map(_format, stack)]


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

    def __init__(self, model, tkparent=None, parent=None, **kw):
        kw['items'] = model
        kw.setdefault('width', 55)
        self.lb = DraggyListbox(tkparent, **kw)
        self.lb.pack(expand=True, fill=BOTH)
        AbstractSequenceViewer.__init__(self, model)
        if parent is None:
            parent = ModelMixin.root
        parent.addChild(self)

    def update(self, kc=None):
        '''
        Update our contents.

        This implementation simply throws out all the current contents
        and puts in the new. It could be more efficient, but this works
        fairly well and is very simple.
        '''

        super(SequenceViewer, self).update(kc)

        stack = stack2view(self.model)

        #Put TOS (Top Of Stack) on the top of the list.
##        stack.reverse()

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


class ViewerMakerMixin:

    def _makeViewer(self, model, name, class_=SequenceViewer):
        viewer = MakeViewer(name, model, class_)
        return viewer

