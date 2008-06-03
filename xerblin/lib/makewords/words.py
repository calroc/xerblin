from xerblin import ExecutableWord, Object
from xerblin.messaging import ListModel
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.lib.makewords.parser import (
    Scanner,
    Parser,
    XerblinWordBuilderTraversal,
    )


class makewords(
    StackLen(2),
    StackType(0, str),
    StackType(1, Object),
    ExecutableWord
    ):

    def execute(self, stack):
        s, interp = stack[:2]
        toks = Scanner().tokenize(s)
        ASTs = Parser().parse(toks)
        if not type(ASTs) is list: ASTs = [ASTs]
        X = XerblinWordBuilderTraversal(interp)
        X.makeWords(ASTs)
        stack[:2] = [ListModel(n.name for n in X.new)]
