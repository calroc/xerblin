from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class div(StackLen(2), ExecutableWord):
    '''
    Divide the second integer on the stack by the integer on the top of
    the stack.
    '''

    def execute(self, stack):
        tos, second = stack[:2]
        result = second / tos #may cause TypeError's, etc...
        stack[:2] = [result]
