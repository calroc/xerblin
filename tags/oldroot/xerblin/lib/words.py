from xerblin import ExecutableWord, SimpleInterpreter
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.messaging import ListModel


class words(StackLen(1), StackType(0, SimpleInterpreter), ExecutableWord):
    '''words
    Given an Object on the stack replace it with a list of its words.
    '''
    def execute(self, stack):
        stack[0] = (
            'Words\n'
            'This is a list of words currently in the dictionary. '
            'Open (right-left click) a word to view its documentation.'
            '\n\n'
            + ' '.join(
            sorted(
                stack[0].dictionary.keys(),
                key=lambda s: s.lower()
                )
            ))
