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
from xerblin.util.stackcheckers import StackLen


class true(ExecutableWord):
    '''true
    Push Boolean true onto the stack.
    '''
    def execute(self, stack):
        stack.insert(0, True)


class false(ExecutableWord):
    '''false
    Push Boolean false onto the stack.
    '''
    def execute(self, stack):
        stack.insert(0, False)


class boolean(StackLen(1), ExecutableWord):
    '''boolean
    Replace the top item on the stack with its Boolean value.
    '''

    def execute(self, stack):
        stack[0] = bool(stack[0])


class Not(StackLen(1), ExecutableWord):
    '''not
    Replace the top item on the stack with its opposite Boolean value.
    '''
    __name__ = 'not'
    def execute(self, stack):
        stack[0] = not stack[0]


class And(StackLen(2), ExecutableWord):
    '''and
    Boolean AND of the top two items on the stack.
    '''
    __name__ = 'and'
    def execute(self, stack):
        stack[:2] = [stack[0] and stack[1]]


class Or(StackLen(2), ExecutableWord):
    '''or
    Boolean OR of the top two items on the stack.
    '''
    __name__ = 'or'
    def execute(self, stack):
        stack[:2] = [stack[0] or stack[1]]

