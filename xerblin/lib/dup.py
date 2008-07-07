from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class dup(StackLen(1), ExecutableWord):
    '''dup
    Duplicate a reference to the top item on the stack.
    '''

    def execute(self, stack):
        stack.insert(0, stack[0])
