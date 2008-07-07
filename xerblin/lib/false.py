from xerblin import ExecutableWord


class false(ExecutableWord):
    '''false
    Push Boolean false onto the stack.
    '''
    def execute(self, stack):
        stack.insert(0, False)
