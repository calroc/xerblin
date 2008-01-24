from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class dotess(ExecutableWord):
    '''
    The '.s' word from Forth. Print the stack to stdout.
    '''

    __name__ = '.s'

    def execute(self, stack):
        print stack
