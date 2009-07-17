'''
    Copyright (C) 2004 - 2008 Simon Forman

    This file is part of Xerblin.

    Xerblin is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


This package loads words from modules and subpackages automatically.

Any subclass of ExecutableWord that can be successfully instantiated
without arguments will be.
'''
from os import listdir
from os.path import isdir, join
from xerblin import (
    ExecutableWord,
    BranchExecutableWord,
    LoopExecutableWord,
    SequentialExecutableWord,
    Object,
    )
from xerblin.util.log import log
from xerblin.lib.programming import Constant, Variable


# Don't load these modules.
exclude = [
    '__init__.py',
    'skeletonlib.py',
    'metas.py',
    ]


# Don't try to instantiate these classes.
exclude_word_classes = set((
    ExecutableWord,
    BranchExecutableWord,
    LoopExecutableWord,
    SequentialExecutableWord,
    Object,
    Constant,
    Variable,
    ))


def _isExecutableWordClass(e):
    try:
        return (
            issubclass(e, ExecutableWord)
            and
            e not in exclude_word_classes
            )
    except:
        return False # Don't care, don't care, DON'T care.


def loadPackageWords(package_name, W):
    '''
    Find all ExecutableWords in package or module and put them in dict W.
    (Overwrite existing names.)
    '''

    # A teensy bit o' security...
    if not package_name.isalnum():
        log.warning(
            'wtf!? non-alphanumeric package name: %s',
            package_name
            )
        return

    statement = 'from xerblin.lib.%s import *' % package_name
    locals_ = {}

    # Import the module or package.
    exec statement in globals().copy(), locals_

    # Extract and "inscribe" the Word classes.
    for name, e in locals_.iteritems():

        # Politely ignore private items.
        if name.startswith('_'):
            continue

        if not _isExecutableWordClass(e):
            continue

        try:
            w = e()

        except:
            # Don't really care ATM what the issue was, just log it.
            log.exception(
                "Problem loading %s in module xerblin.lib.%s",
                name,
                package_name
                )

        else:
            W[w.name] = w


# Get the current path.  (I forget why you can't just say "path = __path__"...)
path = globals()['__path__']


# Path to xerblin.lib.
p = path[0]


# Generate all *.py modules and subpackages in p.
submodules = (
    fn
    for fn in listdir(p)
    if fn not in exclude and (fn.endswith('.py') or isdir(join(p, fn)))
    )


# The only actual 'export' of this (xerblin.lib) module: xerblin.lib.words
# All instantiated words will be put into this dict.  It's named "W" here
# because of some sort of naming conflict.  We rebind it to "words" at
# the end.
W = {}


# Here we go, load 'em up!
for submodule in submodules:

    if submodule.endswith('.py'):
        loadme = submodule[:-3]
    elif submodule == '.svn':
        continue
    else:
        loadme = submodule

    try:
        loadPackageWords(loadme, W)
    except ImportError:
        log.exception("Problem importing %s", join(p, submodule))

words = W
