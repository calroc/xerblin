'''
Provide Level 1 Messaging.
'''
from xerblin.util.log import log


class Viewer(object):
    '''
    Base class for Viewers, defines handle() and children API.
    '''

    def __init__(self, model):
        self.model = model
        self.children = set()
        self._current_message = None

    def handle(self, message):
        if not self._checkMessage(message):
            return False

        return message.model is self.model or self._dispatch(message)

    def addChild(self, child):
        assert isinstance(child, Viewer), repr(child)
        self.children.add(child)

    def removeChild(self, child):
        self.children.discard(child)

    def replaceChildren(self, new_kids):
        self.children.clear()
        self.children.update(new_kids)

    def kidsWho(self, predicate):
        return (kid for kid in self.children if predicate(kid))

    def _dispatch(self, message):
        res = False
        for kid in self.children:
            res |= kid.handle(message)
        return res

    def _checkMessage(self, message):
        if message is self._current_message:
            return False
        self._current_message = message
        return True


class RootViewer(Viewer):
    def handle(self, message):
        model, method, args = (
            message.model,
            message.method_name,
            message.args
            )
        t, i = model.__class__.__name__, id(model)
        print '%s %i . %s %r' % (t, i, method, args)
        return Viewer.handle(self, message)


class NotifyMessage:

    def __init__(self, model, method_name, args):
        self.model = model
        self.method_name = method_name
        self.args = args

    def __repr__(self):
        return repr((self.model, self.method_name, self.args))


class ModelMixin:
    '''
    Gives classes a notify() method and deals with attaching them to the
    root viewer.
    '''

    root = Viewer(None)

    def notify(self, method_name, args):
        message = NotifyMessage(self, method_name, args)
        if __debug__:
            self_id = '<%s: %s => %s>' % (
                self.__class__.__name__,
                id(self),
                repr(self)
                )
            log.debug('notify %s', str((self_id, method_name, args)))
        self.root.handle(message)


class ListModel(ModelMixin, list):
    """
    List that calls notify() when it's changed.
    """

    # All of the following methods extend list's methods to call
    # notify() above. These are all the methods of list that can
    # change a list.
    #
    # (Note, these all return values even though many of them don't,
    # that's because I made them from a template, and it doesn't hurt.)
 
    def __setitem__(self, *args):
        res = super(ListModel, self).__setitem__(*args)
        self.notify('__setitem__', args)
        return res

    def __delitem__(self, *args):
        res = super(ListModel, self).__delitem__(*args)
        self.notify('__delitem__', args)
        return res

    def __setslice__(self, *args):
        res = super(ListModel, self).__setslice__(*args)
        self.notify('__setslice__', args)
        return res

    def __delslice__(self, *args):
        res = super(ListModel, self).__delslice__(*args)
        self.notify('__delslice__', args)
        return res

    def __iadd__(self, *args):
        res = super(ListModel, self).__iadd__(*args)
        self.notify('__iadd__', args)
        return res

    def __imul__(self, *args):
        res = super(ListModel, self).__imul__(*args)
        self.notify('__imul__', args)
        return res

    def append(self, *args):
        res = super(ListModel, self).append(*args)
        self.notify('append', args)
        return res

    def insert(self, *args):
        res = super(ListModel, self).insert(*args)
        self.notify('insert', args)
        return res

    def remove(self, *args):
        res = super(ListModel, self).remove(*args)
        self.notify('remove', args)
        return res

    def extend(self, *args):
        res = super(ListModel, self).extend(*args)
        self.notify('extend', args)
        return res

    def pop(self, i=-1):
        res = super(ListModel, self).pop(i)
        self.notify('pop', (i,))
        return res

    def reverse(self):
        super(ListModel, self).reverse()
        self.notify('reverse', ())

    def sort(self, *args):
        super(ListModel, self).sort(*args)
        self.notify('sort', args)

    def __getstate__(self): return list(self)
    def __setstate__(self, state): self[:] = state


if __name__ == '__main__':

    # Toplevel window.
    root = ModelMixin.root

    some_object = ListModel()

##    # Broadcast to root when changed.
##    some_object.addBroadcastRoot(root)

    # This object gets "viewed".
    v = Viewer(some_object)
    # Root knows of its children.
    root.addChild(v)

    # Two views on our object.
    vv = Viewer(some_object)
    root.addChild(vv)


    some_object.append('bananas')
    some_object.extend(('fruits', 'nuts', 'berries'))
    some_object.remove('fruits')



