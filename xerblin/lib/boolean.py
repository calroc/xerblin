from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class boolean(StackLen(1), ExecutableWord):
    '''
    Replace the top item on the stack with its Boolean value.
    '''

    def execute(self, stack):
        stack[0] = bool(stack[0])


class Not(StackLen(1), ExecutableWord):
    '''
    Replace the top item on the stack with its Boolean value.
    '''
    __name__ = 'not'
    def execute(self, stack):
        stack[0] = not stack[0]


class And(StackLen(2), ExecutableWord):
    '''
    Replace the top item on the stack with its Boolean value.
    '''
    __name__ = 'and'
    def execute(self, stack):
        stack[:2] = [stack[0] and stack[1]]


class Or(StackLen(2), ExecutableWord):
    '''
    Replace the top item on the stack with its Boolean value.
    '''
    __name__ = 'or'
    def execute(self, stack):
        stack[:2] = [stack[0] or stack[1]]
