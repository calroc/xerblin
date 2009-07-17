from xerblin import (
    ExecutableWord,
    BranchExecutableWord,
    LoopExecutableWord,
    SequentialExecutableWord,
    Object,
    )
from xerblin.messaging import ListModel
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.lib.programming import Variable
from xerblin.lib.widgets.widgetwrapper import MakeViewer
from xerblin.lib.widgets.TextViewer import TextViewer

from webbrowser import open_new_tab


class Open(StackLen(2), StackType(1, Object), ExecutableWord):
    '''open

    "open" the item on TOS.

Takes two items, an Object (i.e. self) then the item to open.  The Object is needed because most of the time opening an item will mean opening a TextViewer and that requires a context Object.

Currently, The following behavior is hard-coded:

For:        Do:

Words => Open a TextViewer on their doc string.  (You can edit this and the changes will stick around.  This way you can take notes on words.)

Text => If it starts with http:// or https:// try opening it in a webbrowser, otherwise open a TextViewer.

Numbers => Open a TextViewer on their string representation.

    '''

    __name__ = 'open'

    def execute(self, stack):
        item, self.interpreter = stack[:2]
        self.handled = False

        try:
            if isinstance(item, basestring):
                self.handleBasestring(item)

            elif isinstance(item, ExecutableWord):
                self.handleExecutableWord(item)

            if self.handled:
                del stack[:2]

        finally:
            del self.interpreter

    def handleBasestring(self, S):
        if self._isURL(S):
            open_new_tab(S)
        else:
            v = Variable(S)
            v.value = S
            self.openText(S[:25], v)
        self.handled = True

    def handleExecutableWord(self, word):

        # Allow word classes to define an open() method that will handle
        # "opening" of the word instances for us.
        if hasattr(word, 'open'):
            word.open(self.interpreter)
            self.handled = True
            return


        # Otherwise, look for an explicit doc attribute, which should be
        # a Text.
        try:
            doc = word.doc

        except AttributeError:
            # Didn't have one huh?  Let's fix that now.

            # If it's a constructed "ComboWord" without a doc attr, we
            # make one by using its repr.  The user can add notes as
            # desired.  This will require some nice way to add docs to
            # words made by makewords... *sigh*.  If you're making words
            # in a script and you want to add a doc attr you can use the
            # s2t word to turn a string into a Text, then set that as the
            # word's doc attr using the setattr word.  Now if only there
            # were a good way to make strings in a script...
            if isinstance(word, (
                BranchExecutableWord,
                LoopExecutableWord,
                SequentialExecutableWord,
                )):
                doc = word.name + '\n\n' + repr(word)

            elif isinstance(word, Object):
                doc = word.name

            # or then just use the python doc string.
            else:
                doc = word.__doc__

            v = Variable(word.name)
            v.value = doc
            doc = word.doc = v

        self.openText(word.name + ' Doc', doc)
        self.handled = True

    def openText(self, name, text):
        # Make, and throw away, a TextViewer for the doc object.
        MakeViewer(
            name,
            text,
            TextViewer,
            viewer_options={'interpreter':self.interpreter},
            )

    def _isURL(self, url):
        return url.startswith('http://') or url.startswith('https://')


