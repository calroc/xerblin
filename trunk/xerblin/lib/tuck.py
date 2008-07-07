from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class tuck(StackLen(2), ExecutableWord):
    '''tuck
    Take the top item on the stack and tuck a copy of it under the second item on the stack.
    '''

    def execute(self, stack):
        stack.insert(2, stack[0])
