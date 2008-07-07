from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class over(StackLen(2), ExecutableWord):
    '''over
    Copy the second item down in the stack to the top of the stack.
    '''

    def execute(self, stack):
        stack.insert(0, stack[1])
