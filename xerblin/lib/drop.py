from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class drop(StackLen(1), ExecutableWord):
    '''
    Remove and discard the top item from the stack.
    '''

    def execute(self, stack):
        stack.pop()
