from xerblin import ExecutableWord, SimpleInterpreter
from xerblin.base import BracketedExecuteWord
from xerblin.util.stackcheckers import StackLen, StackType


class InvokeString(
    StackLen(2),
    StackType(0, basestring),
    StackType(1, SimpleInterpreter),
    ExecutableWord
    ):
    def execute(self, stack):
        command, interp = stack[:2]
        del stack[:2]
        try:
            interp.interpret(command)
        except:
            stack[:0] = [command, interp]
            raise


class InvokeWord(
    StackLen(1),
    StackType(0, ExecutableWord),
    ExecutableWord
    ):
    def execute(self, stack):
        BracketedExecuteWord(stack, stack.pop(0))
