from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackType


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
