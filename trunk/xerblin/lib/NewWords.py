'''
Defines the commands to create new combo words on the stack.

There are three words defined:

NewBranchWord - Put a new branch word on the stack.
NewLoopWord   - Put a new loop word on the stack.
NewSeqWord    - Put a new sequential word on the stack

'''
from xerblin import (
    ExecutableWord,
    BranchExecutableWord,
    LoopExecutableWord,
    SequentialExecutableWord,
    )


#############################################
###    Combo Words
#############################################


class NewBranchWord(ExecutableWord):
    '''
    Put a new branch word on the stack.
    '''
    def execute(self, stack):
        stack.append(BranchExecutableWord())


class NewLoopWord(ExecutableWord):
    '''
    Put a new loop word on the stack.
    '''
    def execute(self, stack):
        stack.append(LoopExecutableWord())


class NewSeqWord(ExecutableWord):
    '''
    Put a new sequential word on the stack.
    '''
    def execute(self, stack):
        stack.append(SequentialExecutableWord())
