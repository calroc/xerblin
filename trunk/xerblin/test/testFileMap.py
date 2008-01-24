#!/usr/bin/env python
import unittest
from xerblin.util.fsmap import FSMap
from xerblin import Object, ExecutableWord, SequentialExecutableWord

from os import walk, remove, rmdir
from os.path import join, exists, isfile, isdir
from tempfile import mkdtemp
from md5 import md5


TMP = '/tmp'


class TestFileSystemMap(unittest.TestCase):

    def setUp(self):
        self.object = Object()
        self.tmpdir = mkdtemp('.fs', 'xerblin.', TMP)
        print 'created working dir', self.tmpdir
        self.path = join(self.tmpdir, 'savehere')

    def testSynchronizeToFreshDir(self):
        path = self.path
        self.assert_(not exists(path))
        self.object.toPath(path)
        self.assert_(exists(path))
        self.assert_(exists(join(path, 'stack')))
        self.assert_(exists(join(path, 'dictionary')))

    def testSynchronizeStackToFreshDir(self):
        path = self.path
        self.object.stack.extend(range(3))
        self.object.toPath(path)

        stack_item_0_path = join(path, 'stack', '0')
        self.assert_(exists(stack_item_0_path), stack_item_0_path)
        self.assert_(isdir(stack_item_0_path), stack_item_0_path)

        stack_item_1_path = join(path, 'stack', '1')
        self.assert_(exists(stack_item_1_path), stack_item_1_path)
        self.assert_(isdir(stack_item_1_path), stack_item_1_path)

        stack_item_2_path = join(path, 'stack', '2')
        self.assert_(exists(stack_item_2_path), stack_item_2_path)
        self.assert_(isdir(stack_item_2_path), stack_item_2_path)

    def testSynchronizeStackIntToFreshDir(self):
        self._testStack(2, '2', 'integer\n')

    def testSynchronizeStackFloatToFreshDir(self):
        self._testStack(3.0, '3.0', 'float\n')

    def testSynchronizeStackStringToFreshDir(self):
        S = 'hey there'
        self._testStack(S, md5(S).hexdigest(), S)

    def testSynchronizeStackSequentialExecutableWordToFreshDir(self):
        S = SequentialExecutableWord()
        S.append(SequentialExecutableWord())
        self.object.stack.append(S)
        self.object.toPath(self.path)

        fn = join(self.path, 'stack', '0', 'name')
        self.assert_(exists(fn), fn)
        self.assert_(isfile(fn), fn)
        self.assertEquals('SequentialExecutableWord', open(fn).read())

        fn = join(self.path, 'stack', '0', 'type')
        self.assert_(exists(fn), fn)
        self.assert_(isfile(fn), fn)
        self.assertEquals('SequentialExecutableWord', open(fn).read())

        fn = join(self.path, 'stack', '0', '0')
        self.assert_(exists(fn), fn)
        self.assert_(isdir(fn), fn)

        fn = join(self.path, 'stack', '0', '0', 'name')
        self.assert_(exists(fn), fn)
        self.assert_(isfile(fn), fn)
        self.assertEquals('SequentialExecutableWord', open(fn).read())

        fn = join(self.path, 'stack', '0', '0', 'type')
        self.assert_(exists(fn), fn)
        self.assert_(isfile(fn), fn)
        self.assertEquals('SequentialExecutableWord', open(fn).read())

    def _testStack(self, item, fn, value):
        path = self.path
        self.object.stack.append(item)
        self.object.toPath(path)

        fn = join(path, 'stack', '0', fn)
        self.assert_(exists(fn), fn)
        self.assert_(isfile(fn), fn)
        self.assertEquals(value, open(fn).read())

    def tearDown(self):
        rmdirFORCE(self.tmpdir)


def rmdirFORCE(path):
    print 'recursively removing', path
    for root, dirs, files in walk(path, topdown=False):
        for name in files:
            fn = join(root, name)
            print 'removing file', fn
            remove(fn)
        for name in dirs:
            d = join(root, name)
            print 'removing dir', d
            rmdir(d)
    print 'removing dir', path
    rmdir(path)


if __name__ == '__main__':
    unittest.main()
