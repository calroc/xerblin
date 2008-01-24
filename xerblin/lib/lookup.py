from xerblin import ExecutableWord, Object
from xerblin.util.stackcheckers import StackLen, StackType


class lookup(
    StackLen(2),
    StackType(0, basestring),
    StackType(1, Object),
    ExecutableWord
    ):
    '''
    Look up a word in the dictionary.
    '''
    def execute(self, stack):
        '''Look up a word in the dictionary. Returns None if not found.'''
        interp, name = stack[-2:]
        word = interp.dictionary.get(name)
        stack[-2:] = [word]
