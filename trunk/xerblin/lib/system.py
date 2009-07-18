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
import sys
import os
from time import time, ctime
from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackType


class sysexit(ExecutableWord):
    '''sys.exit
    Exit the system, i.e. quit xerblin.
    '''

    __name__ = 'sys.exit'

    def execute(self, stack):
        sys.exit()


class timedate(ExecutableWord):
    '''timedate
    Put a string representing the current time and date onto the stack.
    '''
    def execute(self, stack):
        stack.insert(0, ctime())


class Time(ExecutableWord):
    '''time
    Put the current time in seconds onto the stack.
    '''

    __name__ = 'time'

    def execute(self, stack):
        stack.insert(0, time())


class pwd(ExecutableWord):
    def execute(self, stack):
        stack.insert(0, os.getcwd())


class find(StackLen(1), StackType(0, basestring), ExecutableWord):
    def execute(self, stack):
        data = os.popen('find -name "%s"' % stack[0]).read()
        stack[0] = data


class ls(ExecutableWord):

    def _stackok(self, stack):
        if stack:
            p = stack[0]
            assert isinstance(p, basestring), \
                   "TOS must be a string, or the stack must be empty"
            assert os.path.exists(p), "path '%s' doesn't exist" % p

    def execute(self, stack):
        if not stack:
            it = ''
        else:
            it = stack[0]
        data = os.popen('ls "%s"' % it).read()
        stack[0] = data
