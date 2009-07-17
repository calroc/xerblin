from xerblin import ExecutableWord, Object
from xerblin.messaging import ListModel
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.util.backtime import listBackupFiles, restorePrevious


class ListHistory(ExecutableWord):
    '''ListHistory
    List the available save files.
    '''
    def execute(self, stack):
        files = ListModel([fn for i, fn in sorted(listBackupFiles())])
        stack.insert(0, files)


class LoadHistory(
    StackLen(2),
    StackType(0, str),
    StackType(1, Object),
    ExecutableWord
    ):

    def execute(self, stack):
        filename, interp = stack[:2]
        restorePrevious(interp, filename)
