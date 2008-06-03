from xerblin import ExecutableWord, SimpleInterpreter
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.messaging import ListModel


class words(StackLen(1), StackType(0, SimpleInterpreter), ExecutableWord):
    '''
    Given an Interpreter on the stack replace it with a list of its words.
    '''
    def execute(self, stack):
        stack[0] = ListModel(
            sorted(
                stack[0].dictionary.keys(),
                key=lambda s: s.lower()
                )
            )
