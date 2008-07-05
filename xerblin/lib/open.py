from xerblin import ExecutableWord
from xerblin.messaging import ListModel
from xerblin.util.stackcheckers import StackLen
from webbrowser import open_new_tab


class Open(StackLen(1), ExecutableWord):
    '''
    "Open" the item on TOS.
    '''

    __name__ = 'open'

    def execute(self, stack):
        item = stack[0]
        self.handled = False

        if isinstance(item, basestring):
            self.handleBasestring(item)

        elif isinstance(item, ExecutableWord):
            self.handleExecutableWord(item)

        if self.handled:
            del stack[0]

    def handleBasestring(self, S):
        if self._isURL(S):
            open_new_tab(S)
            self.handled = True

    def handleExecutableWord(self, word):

        # Allow word classes to define an open() method that will handle
        # "opening" of the word instances for us.
        if hasattr(word, 'open'):
            word.open()
            self.handled = True
            return

        # Otherwise, look for an explicit doc attribute, or then just use
        # the python doc string.
        try:
            doc = word.doc
        except AttributeError:
            doc = word.__doc__

        print doc

    def _isURL(self, url):
        return url.startswith('http://') or url.startswith('https://')

