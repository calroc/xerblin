from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class sub(StackLen(2), ExecutableWord):
    '''sub
    Subtract the number on the top of the stack from the number below it.
    '''

    def execute(self, stack):
        tos, second = stack[:2]
        result = second - tos #may cause TypeError's, etc...
        stack[:2] = [result]
