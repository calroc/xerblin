from xerblin import ExecutableWord


class false(ExecutableWord):
    '''
    Push False onto the stack.
    '''
    def execute(self, stack):
        stack.insert(0, False)
