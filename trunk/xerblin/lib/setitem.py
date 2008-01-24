from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class setitem(StackLen(3), ExecutableWord):
    '''
    Given an object, key and value on the stack do:
        object[key] = value

    key and value are consumed, but object remains on the stack.
    '''
    def execute(self, stack):
        obj, key, value = stack[-3:]
        obj.__setitem__(key, value)
        del stack[-2:]
