from xerblin import ExecutableWord, SimpleInterpreter
from xerblin.util.stackcheckers import StackLen, StackType


class Inscribe(
    StackLen(2),
    StackType(0, SimpleInterpreter),
    StackType(1, ExecutableWord),
    ExecutableWord):
    '''
    Inscribe a named word into the dictionary, if there isn't already one
    with the same name.
    '''
    def execute(self, stack):
        word, interpreter = stack[-2:]
        name = word.name

        if name in interpreter.dictionary:
            print '%s already exists in Dictionary.' % name
        else:
            interpreter.dictionary[name] = word
            del stack[-2:]
            stack.append(name)
