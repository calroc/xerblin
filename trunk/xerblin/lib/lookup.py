from xerblin import ExecutableWord, Object
from xerblin.util.stackcheckers import StackLen, StackType


class lookup(
    StackLen(2),
    StackType(0, basestring),
    StackType(1, Object),
    ExecutableWord
    ):
    '''lookup
    Look up a word in the dictionary.  Requires an Object and a text string.
    '''
    def execute(self, stack):
        '''Look up a word in the dictionary. Returns None if not found.'''
        name, interp = stack[:2]
        word = interp.dictionary.get(name)
        stack[:2] = [word]
