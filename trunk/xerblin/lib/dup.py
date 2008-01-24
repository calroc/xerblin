from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class dup(StackLen(1), ExecutableWord):
    '''
    Duplicate a reference to the top item on the stack.
    '''

    def execute(self, stack):
        stack.append(stack[-1]) #faster than k += [k[-1]]?
