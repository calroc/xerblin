'''
    Copyright (C) 2004 - 2008 Simon Forman

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
from xerblin.messaging import ModelMixin


class Variable(ModelMixin, ExecutableWord):
    '''
    Pushes itself onto the stack, use 'set' and 'get' to manipulate its value.
    '''

    def __init__(self, name):
        ExecutableWord.__init__(self, name)
        self.inner_value = None

    def getValue(self):
        return self.inner_value

    def setValue(self, value):
        self.inner_value = value
        self.notify('set', (value,))

    value = property(getValue, setValue)

    def execute(self, stack): stack.insert(0, self)


class TypedVariable(Variable):
    '''
    Contains a typed value.
    '''

    _type = None

    def __init__(self, name, initial_value=None):
        ExecutableWord.__init__(self, name)
        self.inner_value = self._type(initial_value)

    def setValue(self, value):
        value = self._type(value)
        Variable.setValue(self, value)

    value = property(Variable.getValue, setValue, doc='A string value.')


class Text(TypedVariable):
    '''
    Contains a string value, but has Nop execute().
    '''

    _type = str

    def execute(self, stack):
        pass

    def __repr__(self):
        return "<Text: %r>" % self.inner_value[:23]


class NumberVariable(TypedVariable):
    '''
    Contains an integer value.
    '''

    _type = int

    def __repr__(self):
        return "<Int: %i>" % self.inner_value
