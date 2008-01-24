from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackType


class setname(StackLen(2), StackType(0, basestring), ExecutableWord):
    '''
    Given an object on the stack and a string, set the 'name' attribute
    of the object to the value of the string.
    '''
    def execute(self, stack):
        obj, name = stack[-2:]
        setattr(obj, 'name', name)
        stack.pop()
