from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class div(StackLen(2), ExecutableWord):
    '''div
    Divide the second number on the stack by the number on the top of the stack.  (i.e. if 1 and 2 are on the stack div gives 1/2 or 0.5)
    '''

    def execute(self, stack):
        tos, second = stack[:2]
        result = second * (1. / tos) #may cause TypeError's, etc...
        stack[:2] = [result]
