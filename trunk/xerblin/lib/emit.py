from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class emit(ExecutableWord):
    '''emit
    Print TOS, and drop it.
    '''

    def execute(self, stack):
        print stack[0]
        del stack[0]
