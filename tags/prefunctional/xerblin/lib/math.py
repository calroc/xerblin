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


class add(StackLen(2), ExecutableWord):
    '''add
    Add two numbers together.
    '''

    def execute(self, stack):
        tos, second = stack[:2]
        result = second + tos #may cause TypeError's, etc...
        stack[:2] = [result]


class sub(StackLen(2), ExecutableWord):
    '''sub
    Subtract the number on the top of the stack from the number below it.
    '''

    def execute(self, stack):
        tos, second = stack[:2]
        result = second - tos #may cause TypeError's, etc...
        stack[:2] = [result]


class mul(StackLen(2), ExecutableWord):
    '''mul
    Multiply two numbers together.
    '''

    def execute(self, stack):
        tos, second = stack[:2]
        result = second * tos #may cause TypeError's, etc...
        stack[:2] = [result]


class div(StackLen(2), ExecutableWord):
    '''div
    Divide the second number on the stack by the number on the top of the stack.  (i.e. if 1 and 2 are on the stack div gives 1/2 or 0.5)
    '''

    def execute(self, stack):
        tos, second = stack[:2]
        result = second * (1. / tos) #may cause TypeError's, etc...
        stack[:2] = [result]


class mod(StackLen(2), ExecutableWord):
    '''mod
    Find the remainder if you divide the second number by the first.
    '''

    def execute(self, stack):
        tos, second = stack[:2]
        result = second % tos #may cause TypeError's, etc...
        stack[:2] = [result]
