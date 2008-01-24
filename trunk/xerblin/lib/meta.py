from xerblin import ExecutableWord
from xerblin.messaging import ListModel
from copy import copy


class meta(ExecutableWord):
    '''
    Replace the contents of the stack with a list containing them.
    '''
    def execute(self, stack):
        n = ListModel(stack)
        del stack[:]
        stack.append(n)
