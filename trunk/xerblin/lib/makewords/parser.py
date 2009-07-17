from xerblin import (
    SequentialExecutableWord,
    LoopExecutableWord,
    BranchExecutableWord,
    UnknownWordError,
    )
from xerblin.util.spark import (
    GenericScanner,
    GenericParser,
    GenericASTTraversal,
    )
from xerblin.lib.programming import Constant


class Token:

    def __init__(self, type_, attr=None):
        self.type = type_
        self.attr = attr

    def __cmp__(self, o):
        return cmp(self.type, o)

    def __repr__(self):
        return '%s' % (self.attr or self.type)


class AST:

    def __init__(self, type_, attr='', initial_kids=None):

        if isinstance(type_, Token):
            self.type = type_.type
            self.attr = type_.attr

        else:
            self.type = type_
            self.attr = attr
            if isinstance(attr, AST) and hasattr(attr, 'InscribeMe'):
                self.InscribeMe = attr.InscribeMe

        self._kids = initial_kids or []

    def __getitem__(self, i):
        return self._kids[i]

    def __len__(self):
        return len(self._kids)

    def __setslice__(self, low, high, seq):
        self._kids[low:high] = seq

    def __cmp__(self, o):
        return cmp(self.type, o)

    def __repr__(self):
        if self.attr:
            return '<AST %s: %s>' % (self.type, self.attr)
        else:
            return '<AST %s>' % self.type

    def pprint(self, indent_level=0, tab='    '):
        fmt = '%s<type: %s, attr: %s>'
        print fmt % (indent_level * tab, self.type, self.attr)
        for n in self._kids:
            n.pprint(indent_level + 1, tab)


class Scanner(GenericScanner):
    
    def tokenize(self, input):
        self.rv = []
        GenericScanner.tokenize(self, input)
        return self.rv
    
    def t_whitespace(self, s):
        r'\s+ '
        pass
        
    def t_op(self, s):
        r'[=*@&]'
        self.rv.append(Token(type_=s))
        
    def t_symbol(self, s):
        r'[^=*@&\s]+'
        self.rv.append(Token(type_='symbol', attr=s))
        
    def t_string(self, s):
        r'"(.*?)(?<!\\)"'
        assert s.startswith('"') and s.endswith('"')
        s = s[1:-1]
        self.rv.append(Token(type_='string', attr=s))


class Parser(GenericParser):

    def __init__(self, start='begin'):
        GenericParser.__init__(self, start)

    def p_begin(self, args):
        '''
            begin ::= foolist
            foolist ::= foolist foo
            foolist ::= foo
            foo ::= seq
            foo ::= loop
            foo ::= branch
        '''
        n = len(args)
        if n == 1:
            args = args[0]

        elif n == 2 and isinstance(args[0], list):
            args[:1] = args[0]

        return args

    def p_seq(self, args):
        '''
            seq ::= newsym = symlist
        '''
        self._TokensToAST(args)
        return self._proc(args, '=', 'seq')

    def p_loop(self, args):
        '''
            loop ::= newsym @ symlist
        '''
        self._TokensToAST(args)
        return self._proc(args, '@', 'loop')

    def p_branch(self, args):
        '''
            branch ::= newsym & symbol symbol
        '''
        assert len(args) == 4
        assert args[1].type == '&'

        self._TokensToAST(args)
        return AST('branch', args[0], args[2:])

    def p_symlist(self, args):
        '''
            symlist ::= symlist string
            symlist ::= symlist symbol
            symlist ::= string
            symlist ::= symbol
        '''
        n = len(args)

        if n == 1:
            return AST(args[0])

        if n == 2:
            if isinstance(args[0], list): args[:1] = args[0]
            self._TokensToAST(args)
            return args

    def p_newsym(self, args):
        '''
            newsym ::= * symbol
            newsym ::= symbol
        '''
        n = len(args)

        if n == 1:
            return AST(args[0])

        if n == 2:
            assert args[0].type == '*'
            A = AST(args[1])
            A.InscribeMe = True
            return A

    def _TokensToAST(self, args):
        for i, a in enumerate(args[:]):
            if isinstance(a, Token) and a.type in ('symbol', 'string'):
                args[i] = AST(a)

    def _proc(self, args, op, type_):
        assert len(args) == 3
        assert args[1].type == op

        return AST(type_, args[0], args[2])


class XerblinWordBuilderTraversal(GenericASTTraversal):

    def __init__(self):
        GenericASTTraversal.__init__(self, None)

    def reset(self, interp):
        self.new = []
        self.namespace = interp.dictionary.copy()

    def nextWord(self, ast):
        self.ast = ast
        self.name = ast.attr.attr
        self.body = []
        self.word = None

        self.postorder()

        if getattr(ast, 'InscribeMe', False):
            self.new.append(self.word)

        self.namespace[self.name] = self.word
        
    def makeWords(self, ASTs, interp):
        self.reset(interp)
        for n in ASTs:
            self.nextWord(n)
        for w in self.new:
            interp.dictionary[w.name] = w

    def n_symbol(self, node):
        try:
            val = int(node.attr)
            N = Constant('-noname-int-constant-%i' % val, val)
        except ValueError:
            try:
                val = float(node.attr)
                N = Constant('-noname-float-constant-%s' % val, val)
            except ValueError:
                try:
                    N = self.namespace[node.attr]
                except KeyError, data:
                    raise UnknownWordError(data)

        self.body.append(N)

    def n_string(self, node):
        self.body.append(Constant('-noname-string-constant-', node.attr))

    def n_seq(self, node):
        assert self.name == node.attr.attr
        self.word = SequentialExecutableWord(self.name, self.body)

    def n_loop(self, node):
        assert self.name == node.attr.attr
        self.word = LoopExecutableWord(self.name, self.body)

    def n_branch(self, node):
        assert self.name == node.attr.attr

        word1, word0 = self.body
        self.word = BranchExecutableWord(self.name)
        self.word.word1 = word1
        self.word.word0 = word0

    def default(self, node):
        pass
