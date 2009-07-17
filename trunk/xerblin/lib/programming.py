from xerblin import ExecutableWord, Object
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.messaging import ListModel
from xerblin.util.models import Variable


class createObject(ExecutableWord):
    '''createObject
    Create a new empty Object.
    '''
    def execute(self, stack):
        stack.insert(0, Object(stack=ListModel()))


class Constant(ExecutableWord):
    #
    # Push a constant value onto the stack.
    #
    # Note that this class will raise an exception when the
    # xerblin.lib.__init__ machinery tries to instantiate it without args.
    # This keeps it from showing up in the 'words' dict, yet it lives at
    # module top-level where [un]pickle can find it.
    #
    def __init__(self, name, value):
        ExecutableWord.__init__(self, name)
        self.value = value

    def execute(self, stack):
        stack.insert(0, self.value)


class constant(StackLen(2), StackType(0, basestring), ExecutableWord):
    '''constant
    Given value and a name on the stack create a named constant.
    '''
    def execute(self, stack):
        new_constant = Constant(stack[0], stack[1])
        stack[:2] = [new_constant]


class variable(StackLen(1), StackType(0, basestring), ExecutableWord):
    '''variable
    Create a named variable.
    '''
    def execute(self, stack):
        new_var = Variable(stack[0])
        stack[0] = new_var


class Set(StackLen(2), StackType(1, Variable), ExecutableWord):
    '''set
    Set a value to a variable.
    '''
    __name__ = 'set'
    def execute(self, stack):
        item, var = stack[:2]
        var.value = item
        del stack[:2]


class get(StackLen(1), StackType(0, Variable), ExecutableWord):
    '''get
    Get the value of a variable.
    '''
    def execute(self, stack):
        stack[0] = stack[0].value
