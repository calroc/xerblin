'''
defines the commands to create new combo words on the stack.

There are three words defined:

NewBranchWord - Put a new branch word on the stack.
NewLoopWord   - Put a new loop word on the stack.
NewSeqWord    - Put a new sequential word on the stack

makemacrosequence - Given a name and a list of words create a
    SequenceWord.
'''
from xerblin import (
    ExecutableWord,
    BranchExecutableWord,
    LoopExecutableWord,
    SequentialExecutableWord,
    )
from xerblin.util.stackcheckers import StackLen, StackType


class NewBranchWord(ExecutableWord):
    '''Put a new branch word on the stack.'''
    def execute(self, stack):
        stack.insert(0, BranchExecutableWord())


class NewLoopWord(ExecutableWord):
    '''Put a new loop word on the stack.'''
    def execute(self, stack):
        stack.insert(0, LoopExecutableWord())


class NewSeqWord(ExecutableWord):
    '''Put a new sequential word on the stack.'''
    def execute(self, stack):
        stack.insert(0, SequentialExecutableWord())


class makemacrosequence(
    StackLen(2),
    StackType(0, basestring),
    ExecutableWord
    ):
    '''Given a name and list of words on the stack, create a new SeqWord.

This is a quick way to make a new word. You still have to execute the
Inscribe word to put your new word into the dictionary.

Now you can 'lookup' a series of words, stacking them on the stack in the
order you want them to execute, and click 'meta' to make a list, then
select the name you want your new word to have and copy it onto the
stack.

Once you have the list of words and the name on the stack you can click
'makemacrosequence' then 'Inscribe' and your new word is ready.
'''
    def _all_ExecutableWords(self, N):
        '''Test if everything in N is an ExecutableWord.'''
        try:
            for n in N:
                assert isinstance(n, ExecutableWord), \
       "'%s' in the second item down in the Stack isn't an ExecutableWord" % n

        #The following except block catches the TypeError raised if N can't
        #be iterated on, i.e. is not a sequence.
        except TypeError, e:

            if str(e) == 'iteration over non-sequence':
                raise AssertionError, "the second item down in the Stack isn't a sequence"

            else:
                raise e

    def _stackok(self, stack):
        super(makemacrosequence, self)._stackok(stack)
        self._all_ExecutableWords(stack[1])

    def execute(self, stack):
        name, words = stack[:2]
        s = SequentialExecutableWord(name)
        s.extend(words)
        stack[:2] = [s]
