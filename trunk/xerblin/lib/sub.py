from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class sub(StackLen(2), ExecutableWord):
    '''
    Subtract the integer on the top of the stack from the integer below it.
    '''

    def execute(self, stack):
        second, tos = stack[-2:]
        result = second - tos #may cause TypeError's, etc...
        stack.append(result)
        del stack[-3:-1]
