#!/usr/bin/env python
import unittest
from Tkinter import END, INSERT

from xerblin import Nop
from xerblin.lib.widgets.textviewer import (
    ParagraphModel,
    WordViewer,
    TextViewer,
    )
from xerblin.messaging import (
    ModelMixin,
    NotifyMessage,
    Viewer,
    ListModel,
    )


class TestParagraphModelProperty(unittest.TestCase):

    def setUp(self):
        self.p = ParagraphModel('noname')

    def testSetGet(self):
        self.p.value = '23'
        self.assertEqual('23', self.p.value)

    def testSetMakesString(self):
        self.p.value = 23
        self.assertEqual('23', self.p.value)


class TestParagraphModelNotify(unittest.TestCase):

    def setUp(self):
        self.p = ParagraphModel('noname')
        self.p.root = self
        self.flag = False

    def testSetCallsNotify(self):
        self.p.value = 23
        self.assertEqual(True, self.flag)

    def handle(self, message):
        self.flag = True
        self.assert_(isinstance(message, NotifyMessage))
        self.assertEqual(message.model, self.p)
        self.assertEqual(message.method_name, 'set')
        self.assertEqual(message.args, ('23',))


class TestParagraphModelInsert(unittest.TestCase):

    def setUp(self):
        self.p = ParagraphModel('noname')
        self.p.value = 'Hey there'
        self.p.root = self
        self.flag = False

    def test(self):
        self.p.insert(4, "it's ")
        self.assertEqual(True, self.flag)

    def handle(self, message):
        self.flag = True
        s = "Hey it's there"
        self.assert_(isinstance(message, NotifyMessage))
        self.assertEqual(message.model, self.p)
        self.assertEqual(message.method_name, 'insert')
        self.assertEqual(message.args, (4, "it's "))
        self.assertEqual(self.p.value, s)


class TestTextViewerWithParagraphModels(unittest.TestCase):

    def setUp(self):
        self.p = ParagraphModel('noname')
        self.p.value = 'Hello world!'
        self.m = ListModel([self.p])
        self.t = TextViewer(self.m)

    def testInitialText(self):
        text = self.t.text.get('0.0', END)
        self.assertEqual(1, len(self.t.children))
        self.assertEqual(text, 'Hello world!\n')

    def testRemoveItemFromModel(self):
        self.m.pop()
        self.assertEqual(0, len(self.t.children))
        text = self.t.text.get('0.0', END)
        self.assertEqual(text, '\n')

    def testAddItemToModel(self):
        self.m.append(self.p)
        self.assertEqual(2, len(self.t.children))
        text = self.t.text.get('0.0', END)
        self.assertEqual(text, 'Hello world!Hello world!\n')

    def testModelItemChanges(self):
        hey = 'Hey there you darling World you!'
        self.p.value = hey
        text = self.t.text.get('0.0', END)
        self.assertEqual(text, hey + '\n')

    def testPutObject(self):
        self.t.text.mark_set(INSERT, '1.6')
##        self.t.text.putThing('there ')
        text = self.t.text.get('0.0', END)
        self.assertEqual(text, 'Hello there world!\n')

    def testPutObjectAtEnd(self):
        self.t.text.mark_set(INSERT, END)
##        self.t.text.putThing('there ')
        text = self.t.text.get('0.0', END)
        self.assertEqual(text, 'Hello world!there \n')

    def testPutObjectAnyOldPlace(self):
        self.t.text.insert(END, 'Hello world!')
        self.t.text.mark_set(INSERT, '1.6')
##        self.t.text.putThing('there ')
        text = self.t.text.get('0.0', END)
        self.assertEqual(text, 'Hello there world!\n')


class TestTextViewerWithParagraphModelsTags(unittest.TestCase):

    def setUp(self):
        self.p = ParagraphModel('noname')
        self.p.value = 'Hello world!'
        self.m = ListModel([self.p])
        self.t = TextViewer(self.m)
        self.expected_tag = self._getTag()

    def _getTag(self):
        return 'paragraph_%i' % id(list(self.t.children)[0])

    def testParagraphModelHasTag(self):
        tags = self.t.text.tag_names()
        self.assert_(self.expected_tag in tags)

        begin, end = self.t.text.tag_ranges(self.expected_tag)
        text = self.t.text.get(begin, end)
        self.assertEqual(text, 'Hello world!')

    def testRemovalRemovesTag(self):
        self.m.pop()

        tag_ranges = self.t.text.tag_ranges(self.expected_tag)
        self.assertEqual((), tag_ranges)

        tags = self.t.text.tag_names()
        self.assert_(self.expected_tag not in tags)

    def testAddItemToModel(self):
        self.m.append(self.p)
        ktags = [kid.tag for kid in self.t.children]
        ttags = self.t.text.tag_names()
        for tag in ktags:
            self.assert_(tag in ttags)

    def testModelItemChangesTag(self):
        hey = 'Hey there you darling World you!'
        self.p.value = hey

        tags = self.t.text.tag_names()
        self.assert_(self.expected_tag not in tags)

        tag = self._getTag()
        begin, end = self.t.text.tag_ranges(tag)
        text = self.t.text.get(begin, end)
        self.assertEqual(text, hey)


class TestTextViewerWithWords(unittest.TestCase):

    def setUp(self):
        self.w = Nop
        self.m = ListModel([self.w])
        self.t = TextViewer(self.m)

    def testInitialValues(self):
        text = self.t.text.get('0.0', END)
        self.assertEqual(text, '\n')

        dump = self.t.text.dump('0.0', END)
        D = dict((n[0], n) for n in dump)

        self.assert_('window' in D)

        widget_name = D['window'][1]
        widget = self.t.text.nametowidget(widget_name)
        self.assertEqual(widget['text'], 'Nop')

    def testRemoveWordFromModel(self):
        self.m.pop()

        dump = self.t.text.dump('0.0', END)
        D = dict((n[0], n) for n in dump)

        self.assert_('window' not in D)

    def testAddWordToModel(self):
        self.m.append(self.w)

        dump = self.t.text.dump('0.0', END)

        widgets = [
            name
            for type_, name, index in dump
            if type_ == 'window'
            ]
        self.assert_(len(widgets) == 2)





if __name__ == '__main__':
    unittest.main()


