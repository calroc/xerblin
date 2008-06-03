from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class getitem(StackLen(2), ExecutableWord):
    '''
    Given an object and key on the stack return object[key].
    '''
    def execute(self, stack):
        key, obj = stack[:2]
        value = obj.__getitem__(key)
        stack[:2] = [value]
