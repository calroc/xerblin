from xerblin import ExecutableWord
from xerblin.messaging import ListModel


class meta(ExecutableWord):
    '''meta
    Replace the contents of the stack with a list containing them.
    '''
    def execute(self, stack):
        n = ListModel(stack)
        del stack[:]
        stack.insert(0, n)
