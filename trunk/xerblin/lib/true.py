from xerblin import ExecutableWord


class true(ExecutableWord):
    '''
    Push True onto the stack.
    '''
    def execute(self, stack):
        stack.insert(0, True)
