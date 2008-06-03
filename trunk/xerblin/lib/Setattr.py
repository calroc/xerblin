from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackType


class Setattr(StackLen(3), StackType(1, basestring), ExecutableWord):
    '''
    Implments setattr(object, name, value)
    '''

    __name__ = 'setattr'

    def execute(self, stack):
        obj, name, value = stack[2::-1]
        setattr(obj, name, value)
        del stack[:3]
