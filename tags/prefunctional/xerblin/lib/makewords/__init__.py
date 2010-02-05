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


This package/module exports a single command word 'makewords' which uses
a simple "Little Language" to define a shorthand for creating compound
commands.
'''
from xerblin import ExecutableWord, Object
from xerblin.messaging import ListModel
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.lib.makewords.parser import (
    Scanner,
    Parser,
    XerblinWordBuilderTraversal,
    )


scanner = Scanner()
parser = Parser()
wordbuilder = XerblinWordBuilderTraversal()


class makewords(
    StackLen(2),
    StackType(0, str),
    StackType(1, Object),
    ExecutableWord
    ):

    def execute(self, stack):
        s, interp = stack[:2]
        toks = scanner.tokenize(s)
        ASTs = parser.parse(toks)
        if not isinstance(ASTs, list):
            ASTs = [ASTs]
        wordbuilder.makeWords(ASTs, interp)
        stack[:2] = [ListModel(n.name for n in wordbuilder.new)]


__all__ = ['makewords']
