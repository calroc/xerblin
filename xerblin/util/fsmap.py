from os import makedirs
from os.path import join, exists
from md5 import md5


class FSMap:
    pass


class FSMapObjectMixin:

    def toPath(self, path):
        '''
        Store self to a directory at path, creating it if necessary.
        '''
        if not exists(path):
            stackd, dictd = join(path, 'stack'), join(path, 'dictionary')
            makedirs(stackd)
            makedirs(dictd)

        _seq2path(self.stack, stackd)

        for name, value in self.dictionary.iteritems():
            path = join(dictd, name)
            makedirs(path)
            _dispatch(path, value)


class FSMapSeqWordMixin:

    def toPath(self, path):
        '''
        Store self to a directory at path, which must exist.
        '''
        fn = join(path, 'name')
        open(fn, 'w').write(self.name)

        fn = join(path, 'type')
        open(fn, 'w').write('SequentialExecutableWord')

        _seq2path(self, path)


def _seq2path(seq, path):
    for n, item in enumerate(seq):

        npath = join(path, str(n))
        makedirs(npath)
        _dispatch(npath, item)


def _dispatch(path, item):
        T = type(item)

        if T in (int, long):
            itempath = join(path, str(item))
            open(itempath, 'w').write('integer\n')
            
        elif T is float:
            itempath = join(path, str(item))
            open(itempath, 'w').write('float\n')

        elif T is str:
            itempath = join(path, md5(item).hexdigest())
            open(itempath, 'wb').write(item)

        else:
            try:
                f = item.toPath
            except AttributeError:
                pass
##                print item, 'has no toPath() method.'
            else:
                f(path)

