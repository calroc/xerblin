from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackHasAttr


class push(StackLen(2), StackHasAttr(1, 'append'), ExecutableWord):
    '''
    Push the item on the top of the stack onto the list below it.
    '''
    def execute(self, stack):
        s, n = stack[-2:]
        s.append(n)
        stack.pop()
