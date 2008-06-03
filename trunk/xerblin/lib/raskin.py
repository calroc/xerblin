from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen
from math import *

class calc(StackLen(1), ExecutableWord):
    '''
    Calculate the expression on TOS.
    '''

    def execute(self, stack):
        expression = stack[0]
        result = eval(expression)
        stack[0] = result
