from time import time, ctime
from xerblin import ExecutableWord


class timedate(ExecutableWord):
    '''timedate
    Put a string representing the current time and date onto the stack.
    '''
    def execute(self, stack):
        stack.insert(0, ctime())


class Time(ExecutableWord):
    '''time
    Put the current time in seconds onto the stack.
    '''

    __name__ = 'time'

    def execute(self, stack):
        stack.insert(0, time())
