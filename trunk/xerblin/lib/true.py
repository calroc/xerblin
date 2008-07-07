from xerblin import ExecutableWord


class true(ExecutableWord):
    '''true
    Push Boolean true onto the stack.
    '''
    def execute(self, stack):
        stack.insert(0, True)
