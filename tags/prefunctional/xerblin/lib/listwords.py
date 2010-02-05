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
from xerblin.util.stackcheckers import StackLen, StackHasAttr


class reverse(StackLen(1), ExecutableWord):
    '''push
    Push the item on the top of the stack onto the list below it.
    '''
    def execute(self, stack):
        n = stack[0]
        n[:] = list(reversed(n))


class pop(StackLen(1), StackHasAttr(0, 'pop'), ExecutableWord):
    '''pop
    Pop a value from the list on the top of the stack.
    '''
    def execute(self, stack):
        stack.insert(0, stack[0].pop(0))


class push(StackLen(2), StackHasAttr(1, 'append'), ExecutableWord):
    '''push
    Push the item on the top of the stack onto the list below it.
    '''
    def execute(self, stack):
        n, s = stack[:2]
        s.insert(0, n)
        del stack[0]
