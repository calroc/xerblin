'''
    Copyright (C) 2004 - 2009 Simon Forman

    This file is part of Xerblin.

    Xerblin is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

'''
from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.messaging import ListModel


class drop(StackLen(1), ExecutableWord):
    '''drop
    Remove and discard the top item from the stack.
    '''

    def execute(self, stack):
        del stack[0]


class dup(StackLen(1), ExecutableWord):
    '''dup
    Duplicate a reference to the top item on the stack.
    '''

    def execute(self, stack):
        stack.insert(0, stack[0])


class over(StackLen(2), ExecutableWord):
    '''over
    Copy the second item down in the stack to the top of the stack.
    '''

    def execute(self, stack):
        stack.insert(0, stack[1])


class pick(StackLen(1), StackType(0, int), ExecutableWord):
    '''pick
    Take an integer N from the Stack and copy the Nth remaining item (counting f
    '''

    def _stackok(self, stack):
        super(pick, self)._stackok(stack)
        assert 0 <= stack[0] < (len(stack) - 1)

    def execute(self, stack):
        n = stack[0] + 1
        stack[0] = stack[n]


class rot(StackLen(3), ExecutableWord):
    '''rot
    Rotate the top three items on the stack.
    '''

    def execute(self, stack):
        stack.insert(0, stack.pop(2))


class swap(StackLen(2), ExecutableWord):
    '''swap
    Swap the places of the top two items on the stack.
    '''

    def execute(self, stack):
        second, tos = stack[:2]
        stack[:2] = tos, second


class tuck(StackLen(2), ExecutableWord):
    '''tuck
    Take the top item on the stack and tuck a copy of it under the second item on the stack.
    '''

    def execute(self, stack):
        stack.insert(2, stack[0])


class meta(ExecutableWord):
    '''meta
    Replace the contents of the stack with a list containing them.
    '''
    def execute(self, stack):
        n = ListModel(stack)
        del stack[:]
        stack.insert(0, n)


class unmeta(StackLen(1), ExecutableWord):
    '''unmeta
    Take a list from the top of the stack and put it's contents on the stack.
    '''

    def _stackok(self, stack):

        super(unmeta, self)._stackok(stack)

        try:
            for n in stack[0]: break

        #The following except block catches the TypeError raised if N can't
        #be iterated on, i.e. is not a sequence.
        except TypeError, e:

            if str(e) == 'iteration over non-sequence':
                raise AssertionError, "the second item down in the Stack isn't a sequence."

            else:
                raise e

    def execute(self, stack):
        s = stack.pop(0)
        try:
            stack[0:0] = s
        except:
            stack.insert(0, s)
            raise


class dotess(ExecutableWord):
    '''
    The '.s' word from Forth. Print the stack to stdout.
    '''

    __name__ = '.s'

    def execute(self, stack):
        print stack


class emit(ExecutableWord):
    '''emit
    Print TOS, and drop it.
    '''

    def execute(self, stack):
        print stack[0]
        del stack[0]
