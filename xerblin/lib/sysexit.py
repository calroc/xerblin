import sys
from xerblin import ExecutableWord


class sysexit(ExecutableWord):
    '''
    Exit the system, i.e. quit xerblin.
    '''

    __name__ = 'sys.exit'

    def execute(self, stack):
        sys.exit()
