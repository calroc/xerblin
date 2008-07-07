from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackType


class pick(StackLen(1), StackType(0, int), ExecutableWord):
    '''pick
    Take an integer N from the Stack and copy the Nth remaining item (counting from zero) and duplicate it to the top of the Stack.
    '''

    def _stackok(self, stack):
        super(pick, self)._stackok(stack)
        assert 0 <= stack[0] < (len(stack) - 1)

    def execute(self, stack):
        n = stack[0] + 1
        stack[0] = stack[n]
