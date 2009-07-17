from xerblin import ExecutableWord, Object, SimpleInterpreter
from xerblin.base import BracketedExecuteWord
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.messaging import ListModel
from xerblin.util.models import Variable


class createObject(ExecutableWord):
    '''createObject
    Create a new empty Object.
    '''
    def execute(self, stack):
        stack.insert(0, Object(stack=ListModel()))


class Getattr(StackLen(2), StackType(0, basestring), ExecutableWord):
    '''getattr
    Implements getattr(object, name) => value
    '''

    __name__ = 'getattr'

    def execute(self, stack):
        name, obj = stack[:2]
        value = getattr(obj, name)
        stack[:2] = [value]


class Setattr(StackLen(3), StackType(1, basestring), ExecutableWord):
    '''setattr
    Implments setattr(object, name, value)
    '''

    __name__ = 'setattr'

    def execute(self, stack):
        obj, name, value = stack[2::-1]
        setattr(obj, name, value)
        del stack[:3]


class getitem(StackLen(2), ExecutableWord):
    '''getitem
    Given an object and key on the stack return object[key].
    '''
    def execute(self, stack):
        key, obj = stack[:2]
        value = obj.__getitem__(key)
        stack[:2] = [value]


class setitem(StackLen(3), ExecutableWord):
    '''setitem
    Given an object, key and value on the stack do:
        object[key] = value

    key and value are consumed, but object remains on the stack.
    '''
    def execute(self, stack):
        obj, key, value = stack[2::-1]
        obj.__setitem__(key, value)
        del stack[:2]


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


class InvokeString(
    StackLen(2),
    StackType(0, basestring),
    StackType(1, SimpleInterpreter),
    ExecutableWord
    ):
    def execute(self, stack):
        command, interp = stack[:2]
        del stack[:2]
        try:
            interp.interpret(command)
        except:
            stack[:0] = [command, interp]
            raise


class InvokeWord(
    StackLen(1),
    StackType(0, ExecutableWord),
    ExecutableWord
    ):
    def execute(self, stack):
        BracketedExecuteWord(stack, stack.pop(0))
