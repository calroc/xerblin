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

    def execute(self, stack): stack.append(self)


class Text(Variable):
    '''
    Contains a string value, but has Nop execute().
    '''
    def __init__(self, name, initial_value=''):
        ExecutableWord.__init__(self, name)
        self._value = str(initial_value)

    def setValue(self, value):
        value = str(value)
        Variable.setValue(self, value)

    value = property(Variable.getValue, setValue, doc='A string value.')

    def execute(self, stack):
        pass

    def __repr__(self):
        return "<Text: %r>" % self._value[:23]


