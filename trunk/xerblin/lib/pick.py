from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackType


class pick(StackLen(1), StackType(0, int), ExecutableWord):
    '''
    Take an int N from the Stack and copy the Nth remaining item (counting
    from zero) and duplicate it to the top of the Stack.
    '''

    def _stackok(self, stack):
        super(pick, self)._stackok(stack)
        assert 0 <= stack[-1] < (len(stack) - 1)

    def execute(self, stack):
        n = int(stack.pop())
        stack.append(stack[-(n + 1)])
