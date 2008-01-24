#!/usr/bin/env python
import unittest
from xerblin import SequentialExecutableWord, Nop
from xerblin.messaging import ModelMixin, NotifyMessage, Viewer, ListModel


class TestModelMixin(unittest.TestCase):

    def setUp(self):
        self.m = ModelMixin()
        self.m.root = self

    def testNotify(self):
        self.m.notify('method', 'args')

    def handle(self, message):
        self.assert_(isinstance(message, NotifyMessage))
        self.assertEqual(message.model, self.m)
        self.assertEqual(message.method_name, 'method')
        self.assertEqual(message.args, 'args')


class TestListModel(unittest.TestCase):

    def setUp(self):
        self.l = ListModel()
        self.l.root = self

    def testAppend(self):
        self.method_name = 'append'
        self.args = ('23',)
        self.l.append(self.args[0])

    def handle(self, message):
        self.assert_(isinstance(message, NotifyMessage))
        self.assertEqual(message.model, self.l)
        self.assertEqual(message.method_name, self.method_name)
        self.assertEqual(message.args, self.args)


class TestSequentialExecutableWord(unittest.TestCase):

    def setUp(self):
        self.l = SequentialExecutableWord('noname')
        self.l.root = self

    def testAppend(self):
        self.method_name = 'append'
        self.args = (Nop,)
        self.l.append(self.args[0])

    def handle(self, message):
        self.assert_(isinstance(message, NotifyMessage))
        self.assertEqual(message.model, self.l)
        self.assertEqual(message.method_name, self.method_name)
        self.assertEqual(message.args, self.args)


class TestViewer(unittest.TestCase):

    def setUp(self):
        self.m = ModelMixin()
        self.v = Viewer(self.m)

    def testHandleOwnMessage(self):
        m = NotifyMessage(self.m, None, None)
        self.assertEqual(True, self.v.handle(m))

    def testHandleAlienMessage(self):
        m = NotifyMessage(None, None, None)
        self.assertEqual(False, self.v.handle(m))

    def testHandleSameMessageTwiceReturnsFalse(self):
        m = NotifyMessage(self.m, None, None)
        self.assertEqual(True, self.v.handle(m))
        self.assertEqual(False, self.v.handle(m))


class TestViewerChidren(unittest.TestCase):

    def setUp(self):
        self.m0 = ModelMixin()
        self.m1 = ModelMixin()
        self.v0 = Viewer(self.m0)
        self.v1 = Viewer(self.m1)
        self.v0.addChild(self.v1)
        self.message = NotifyMessage(self.m1, None, None)

    def testHandleKidMessage(self):
        self.assertEqual(True, self.v0.handle(self.message))

    def testRemoveChild(self):
        self.v0.removeChild(self.v1)
        self.assertEqual(False, self.v0.handle(self.message))

    def testReplaceChildren(self):
        self.v0.replaceChildren([])
        self.assertEqual(False, self.v0.handle(self.message))

    def testHandleSameKidMessageTwiceReturnsFalse(self):
        self.assertEqual(True, self.v0.handle(self.message))
        self.assertEqual(False, self.v0.handle(self.message))


if __name__ == '__main__':
    unittest.main()


