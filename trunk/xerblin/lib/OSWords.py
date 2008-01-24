import os
from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackType


class pwd(ExecutableWord):
    def execute(self, stack):
        stack.append(os.getcwd())


class find(StackLen(1), StackType(0, basestring), ExecutableWord):
    def execute(self, stack):
        data = os.popen('find -name "%s"' % stack[-1]).read()
        stack.append(data)
        stack.pop(-2)


class ls(ExecutableWord):

    def _stackok(self, stack):
        if stack:
            p = stack[-1]
            assert isinstance(p, basestring), \
                   "TOS must be a string, or the stack must be empty"
            assert os.path.exists(p), "path '%s' doesn't exist" % p

    def execute(self, stack):
        if not stack:
            it = ''
        else:
            it = stack[-1]
        data = os.popen('ls "%s"' % it).read()
        stack.append(data)
        stack.pop(-2)
