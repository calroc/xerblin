from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.util.models import Variable


class variable(StackLen(1), StackType(0, basestring), ExecutableWord):
    '''
    Create a named variable.
    '''
    def execute(self, stack):
        new_var = Variable(stack[-1])
        stack[-1] = new_var


class Set(StackLen(2), StackType(1, Variable), ExecutableWord):
    '''
    Set a value to a variable.
    '''
    __name__ = 'set'
    def execute(self, stack):
        var, item = stack[-2:]
        var.value = item
        del stack[-2:]


class get(StackLen(1), StackType(0, Variable), ExecutableWord):
    '''
    Get the value of a variable.
    '''
    def execute(self, stack):
        stack[-1] = stack[-1].value
