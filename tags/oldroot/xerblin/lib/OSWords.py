import os
from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen, StackType


class pwd(ExecutableWord):
    def execute(self, stack):
        stack.insert(0, os.getcwd())


class find(StackLen(1), StackType(0, basestring), ExecutableWord):
    def execute(self, stack):
        data = os.popen('find -name "%s"' % stack[0]).read()
        stack[0] = data


class ls(ExecutableWord):

    def _stackok(self, stack):
        if stack:
            p = stack[0]
            assert isinstance(p, basestring), \
                   "TOS must be a string, or the stack must be empty"
            assert os.path.exists(p), "path '%s' doesn't exist" % p

    def execute(self, stack):
        if not stack:
            it = ''
        else:
            it = stack[0]
        data = os.popen('ls "%s"' % it).read()
        stack[0] = data
