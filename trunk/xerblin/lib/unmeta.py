from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen


class unmeta(StackLen(1), ExecutableWord):
    '''
    Take a list from the top of the stack and put it's contents on the stack.
    '''

    def _stackok(self, stack):

        super(unmeta, self)._stackok(stack)

        try:
            for n in stack[-1]: break

        #The following except block catches the TypeError raised if N can't
        #be iterated on, i.e. is not a sequence.
        except TypeError, e:

            if str(e) == 'iteration over non-sequence':
                raise AssertionError, "the second item down in the Stack isn't a sequence"

            else:
                raise e

    def execute(self, stack):
        m, s = stack[:-1], stack[-1]
        m.extend(s)
        stack[:] = m
