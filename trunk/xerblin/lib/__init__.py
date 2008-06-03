from os import listdir
from os.path import isdir, join
from imp import find_module, load_module
from xerblin import (
    ExecutableWord,
    BranchExecutableWord,
    LoopExecutableWord,
    SequentialExecutableWord,
    Object,
    )

# Don't load these.
exclude = [
    '__init__.py',
    'skeletonlib.py',
    'metas.py',
    ]

exclude_word_classes = set((
    ExecutableWord,
    BranchExecutableWord,
    LoopExecutableWord,
    SequentialExecutableWord,
    Object,
    ))


# Get the current path.  (I forget why you can't just say "path = __path__"...)
path = globals()['__path__']


# Path to xerblin.lib.
p = path[0]


# Generate all *.py in p.
submodules = (
    fn
    for fn in listdir(p)
    if fn not in exclude and (fn.endswith('.py') or isdir(join(p, fn)))
    )
# The only actual 'export' of this (xerblin.lib) module: xerblin.lib.words
W = {}


def loadModuleWords(M, W):
    '''
    Find all ExecutableWords in module M and put them in dict W.
    (Overwrite existing names.)
    '''
    for name in dir(M):
        if name.startswith('_'):
            continue
        item = getattr(M, name)
        try:
            if issubclass(item, ExecutableWord) and \
               item not in exclude_word_classes:
                item = item()
                W[item.name] = item
        except:
            pass

def _yieldExecutableWords(d):
    for n in d.values():
        try:
            if issubclass(n, ExecutableWord) and \
               n not in exclude_word_classes:
                yield n
        except:
            pass


def loadPackageWords(package_name, W):
    s =  'from xerblin.lib.%s import *' % package_name
    l = {}
    exec s in globals().copy(), l
    for e in _yieldExecutableWords(l):
        try:
            w = e()
        except:
            pass
        else:
            W[w.name] = w


for submodule in submodules:
        if submodule.endswith('.py'):
            try:
                submodule = submodule[:-3]

                loadPackageWords(submodule, W)

##                f, fn, description = find_module(submodule, path)
##
##                submodule = 'xerblin.lib.' + submodule
##                Mod = load_module(submodule, f, fn, description)
##
##                loadModuleWords(Mod, W)

            except ImportError:
                pass

        else:
            if submodule == '.svn':
                continue
            loadPackageWords(submodule, W)

words = W
