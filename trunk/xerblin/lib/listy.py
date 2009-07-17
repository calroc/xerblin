from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackHasAttr
from xerblin.messaging import ListModel


class reverse(StackLen(1), ExecutableWord):
    '''push
    Push the item on the top of the stack onto the list below it.
    '''
    def execute(self, stack):
        n = stack[0]
        n[:] = list(reversed(n))


class pop(StackLen(1), StackHasAttr(0, 'pop'), ExecutableWord):
    '''pop
    Pop a value from the list on the top of the stack.
    '''
    def execute(self, stack):
        stack.insert(0, stack[0].pop(0))


class push(StackLen(2), StackHasAttr(1, 'append'), ExecutableWord):
    '''push
    Push the item on the top of the stack onto the list below it.
    '''
    def execute(self, stack):
        n, s = stack[:2]
        s.insert(0, n)
        del stack[0]
