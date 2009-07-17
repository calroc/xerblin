from xerblin import ExecutableWord, Object
from xerblin.messaging import ListModel
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.lib.makewords.parser import (
    Scanner,
    Parser,
    XerblinWordBuilderTraversal,
    )


scanner = Scanner()
parser = Parser()
wordbuilder = XerblinWordBuilderTraversal()


class makewords(
    StackLen(2),
    StackType(0, str),
    StackType(1, Object),
    ExecutableWord
    ):

    def execute(self, stack):
        s, interp = stack[:2]
        toks = scanner.tokenize(s)
        ASTs = parser.parse(toks)
        if not isinstance(ASTs, list):
            ASTs = [ASTs]
        wordbuilder.makeWords(ASTs, interp)
        stack[:2] = [ListModel(n.name for n in wordbuilder.new)]


__all__ = ['makewords']
