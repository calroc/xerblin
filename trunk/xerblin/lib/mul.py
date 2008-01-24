from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class mul(StackLen(2), ExecutableWord):
    '''
    Multiply two integers together.
    '''

    def execute(self, stack):
        second, tos = stack[-2:]
        result = second * tos #may cause TypeError's, etc...
        stack.append(result)
        del stack[-3:-1]
