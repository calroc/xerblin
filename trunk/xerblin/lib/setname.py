from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackType


class setname(StackLen(2), StackType(0, basestring), ExecutableWord):
    '''setname
    Given an object on the stack and a string, set the 'name' attribute of the object to the value of the string.  The name is taken off the stack but the object remains.
    '''
    def execute(self, stack):
        name, obj = stack[:2]
        setattr(obj, 'name', name)
        stack.pop(0)
