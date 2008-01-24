from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class swap(StackLen(2), ExecutableWord):
    '''
    Swap the places of the top two items on the stack.
    '''

    def execute(self, stack):
        second, tos = stack[-2:]
        stack[-2:] = tos, second
