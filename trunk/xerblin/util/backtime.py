from cPickle import dump, load
from os import listdir
from os.path import join, expanduser


FILENAME_PATTERN = 'xerblin.%i.pickle'
DEFAULT_PATH = expanduser('~/xerblin/pickles')


def attemptBackup(I, path=DEFAULT_PATH):
    if __debug__:
        print 'fake attemptBackup(I)', I
        return
    n = getMaxN(path) + 1
    fn = join(path, FILENAME_PATTERN % n)
    F = open(fn, 'w')
    try:
        dump(I, F)
    finally:
        F.close()
    print 'wrote', fn


def restorePrevious(I, path=DEFAULT_PATH):
    n = getMaxN(path)
    if n < 0:
        print 'No previous backup!'
        return
    fn = join(path, FILENAME_PATTERN % n)
    F = open(fn)
    try:
        II = load(F)
    finally:
        F.close()
    I._become(II.stack, II.dictionary)
    print 'Loaded', fn


def getMaxN(path):
    try:
        n = max(
            int(fn[8:-7])
            for fn in listdir(path)
            if fn.startswith('xerblin.') and fn.endswith('.pickle')
            )
    except ValueError:
        n = -1
    return n


