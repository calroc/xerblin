from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackHasAttr


class pop(StackLen(1), StackHasAttr(0, 'pop'), ExecutableWord):
    '''
    Pop a value from the list on the top of the stack.
    '''
    def execute(self, stack):
        stack.insert(0, stack[0].pop(0))
