from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class sub(StackLen(2), ExecutableWord):
    '''
    Subtract the integer on the top of the stack from the integer below it.
    '''

    def execute(self, stack):
        tos, second = stack[:2]
        result = second - tos #may cause TypeError's, etc...
        stack[:2] = [result]
