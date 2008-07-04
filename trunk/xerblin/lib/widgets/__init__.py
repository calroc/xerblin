from xerblin import ExecutableWord, SimpleInterpreter
from xerblin.messaging import ListModel
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.util.models import Text
from xerblin.lib.widgets.widgetwrapper import MakeViewer
from xerblin.lib.widgets.listwidgets import (
    ViewerMakerMixin,
    SequenceController,
    )
from xerblin.lib.widgets.TextViewer import TextViewer


class getstack(
    StackLen(1),
    StackType(0, SimpleInterpreter),
    ExecutableWord
    ):
    '''
    Given an Interpreter on the stack get its stack.
    '''
    def execute(self, stack):
        interpreter = stack[0]
        stack[0] = interpreter.stack


class listviewer(
    ViewerMakerMixin,
    StackLen(1),
    StackType(0, ListModel),
    ExecutableWord
    ):
    '''
    Given a ListModel on the stack open a ListViewer on it.
    '''
    def execute(self, stack):
        model = stack[0]
        name = "ListViewer %s" % (id(model),)
        stack[0] = self._makeViewer(model, name, SequenceController)


class textviewer(
    StackLen(2),
    StackType(0, (Text, basestring)),
    StackType(1, SimpleInterpreter),
    ExecutableWord
    ):
    '''
    Given a ListModel on the stack open a ListViewer on it.
    '''
    def execute(self, stack):
        model, interpreter = stack[:2]
        if not isinstance(model, Text):
            model = Text('noname', str(model))
        name = "TextViewer %s" % (id(model),)
        viewer = MakeViewer(
            name,
            model,
            TextViewer,
            viewer_options={'interpreter':interpreter},
            )
        stack[:2] = [viewer]


class s2t(StackLen(1), StackType(0, str), ExecutableWord):
    '''
    Convert a string to a Text.
    '''
    def execute(self, stack):
        s = stack[0]
        p = Text('noname', s)
        stack[0] = p


__all__ = [
    'getstack',
    'listviewer',
    'textviewer',
    's2t',
    ]
