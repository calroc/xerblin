from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class mod(StackLen(2), ExecutableWord):
    '''
    Find the remainder if you divide the second integer by the first.
    '''

    def execute(self, stack):
        second, tos = stack[-2:]
        result = second % tos #may cause TypeError's, etc...
        stack.append(result)
        del stack[-3:-1]
