from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackType


class Getattr(StackLen(2), StackType(0, basestring), ExecutableWord):
    '''
    Implements getattr(object, name) => value
    '''

    __name__ = 'getattr'

    def execute(self, stack):
        name, obj = stack[:2]
        value = getattr(obj, name)
        stack[:2] = [value]
