from xerblin import ExecutableWord, Object
from xerblin.messaging import ListModel


class createObject(ExecutableWord):
    '''
    Create a new empty Object.
    '''
    def execute(self, stack):
        stack.insert(0, Object(stack=ListModel()))