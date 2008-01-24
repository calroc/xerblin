from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class getitem(StackLen(2), ExecutableWord):
    '''
    Given an object and key on the stack replace the key with object[key].
    '''
    def execute(self, stack):
        obj, key = stack[-2:]
        value = obj.__getitem__(key)
        stack[-1] = value
