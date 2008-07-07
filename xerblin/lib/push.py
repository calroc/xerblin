from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackHasAttr


class push(StackLen(2), StackHasAttr(1, 'append'), ExecutableWord):
    '''push
    Push the item on the top of the stack onto the list below it.
    '''
    def execute(self, stack):
        n, s = stack[:2]
        s.insert(0, n)
        del stack[0]
