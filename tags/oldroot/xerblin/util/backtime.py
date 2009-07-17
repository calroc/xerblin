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


Crude serialization support.

'''
from cPickle import dump, load
from os import listdir, mkdir
from os.path import join, expanduser, isdir, split, exists
from glob import iglob
from xerblin.util.log import log


FILENAME_PATTERN = 'xerblin.%i.pickle'


DEFAULT_PATH = expanduser('~/.xerblin/pickles')


if DEFAULT_PATH.startswith('~'):
    # expanduser() failed, let's NOT guess at a save dir.
    DEFAULT_PATH = False
    log.warning("Failed to locate save dir $HOME/.xerblin/pickles")

else:
    # Create the dir unless it exists.

    def mkdirs(path, mode=0755):
        '''
        Recursively create dirs.
        '''
        if isdir(path):
            return
        mkdirs(split(path)[0], mode) # Create the head path.
        log.debug('Making %s...', path)
        mkdir(path, mode)

    mkdirs(DEFAULT_PATH)
    log.debug('Using %s as save directory.', DEFAULT_PATH)


def attemptBackup(I, path=DEFAULT_PATH):
    '''
    Try to write I to a unique pickle file at path.
    '''

    # Fake save for debugging.
    if __debug__:
        log.debug('fake attemptBackup(I) %s', str(I))
        return

    # Handle DEFAULT_PATH == False, i.e. no save dir.
    if not path:
        return

    # Create a unique filename.
    n = getMaxN(path) + 1
    fn = join(path, FILENAME_PATTERN % n)

    assert not exists(fn), 'File already exists!? %s' % fn
    F = open(fn, 'w')

    try:
        dump(I, F)
    except:
        log.exception('Dumping %s to %s', str(I), fn)
    else:
        log.debug('wrote %s', fn)
    finally:
        F.close()


def listBackupFiles(path=DEFAULT_PATH):
    '''
    Return a generator that yields all correctly named files in path.
    (I.e. xerblin.*.pickle)
    '''
    pattern = join(path, FILENAME_PATTERN.replace('%i', '*', 1))
    G = (split(fn)[1] for fn in iglob(pattern))
    return ((int(fn[8:-7]), fn) for fn in G)


def restorePrevious(I, filename, path=DEFAULT_PATH):
    '''
    Given an Interpreter and a pickle file name, try to restore the state
    in the pickle file.
    '''
    filename = join(path, filename)
    F = open(filename)
    try:
        II = load(F)
    except:
        log.exception('Loading from %s', filename)
    else:
        I._become(II.stack, II.dictionary)
        log.debug('Loaded %s', filename)
    finally:
        F.close()


def getMaxN(path):
    '''
    Given a path return an integer of the highest numbered save file in
    the directory.  Return -1 on error.
    '''
    try:
        n = max(i for i, fn in listBackupFiles(path))
    except ValueError:
        n = -1
    return n

