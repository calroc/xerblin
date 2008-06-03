from xerblin import ExecutableWord
from xerblin.messaging import ModelMixin


class Variable(ModelMixin, ExecutableWord):
    '''
    Pushes itself onto the stack, use 'set' and 'get' to manipulate its value.
    '''

    def __init__(self, name):
        ExecutableWord.__init__(self, name)
        self._value = None

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value
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
        self._value = self._type(initial_value)

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
        return "<Text: %r>" % self._value[:23]


class NumberVariable(TypedVariable):
    '''
    Contains an integer value.
    '''

    _type = int

    def __repr__(self):
        return "<Int: %i>" % self._value


