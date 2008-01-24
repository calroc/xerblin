from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class rot(StackLen(3), ExecutableWord):
    '''
    Rotate the top three items on the stack.
    '''

    def execute(self, stack):
        stack.append(stack.pop(-3))
