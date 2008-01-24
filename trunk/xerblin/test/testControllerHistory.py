#!/usr/bin/env python
from xerblin.util.controller import HistoryList
import unittest


class DummyCLI:
    value = ''
    def get(self): return self.value
    def set(self, value): self.value = value


class TestControllerHistory(unittest.TestCase):

    def setUp(self):
        self.cli = DummyCLI()
        self.hist = HistoryList(self.cli)

    def testStartsEmpty(self):
        self.assertEqual(0, len(self.hist))

    def testPrevFromEmpty(self):
        self.assertEqual(self.cli.get(), self.hist.prev())

    def testNextFromEmpty(self):
        self.assertEqual(self.cli.get(), self.hist.next())

    def testAppendNoDuplicates(self):
        self.hist.append('hey')
        self.hist.append('hey')
        self.assertEqual(1, len(self.hist))

    def testAppendBringsDuplicatesToEnd(self):
        self.hist.append('hey')
        self.hist.append('there')
        self.hist.append('hey')
        self.assertEqual(2, len(self.hist))
        self.assertEqual(['there', 'hey'], self.hist)


class TestControllerHistoryAppend(unittest.TestCase):

    def setUp(self):
        self.cli = DummyCLI()
        self.hist = HistoryList(self.cli)
        self.current_command = self.cli.get()
        for char in 'hey':
            self.hist.append(char)

    def testPrevFromSome(self):
        self.assertEqual('y', self.hist.prev())
        self.assertEqual(self.hist[-1], self.current_command)
        self.assertEqual('e', self.hist.prev())
        self.assertEqual('h', self.hist.prev())
        self.assertEqual('h', self.hist.prev())

    def testNextFromSome(self):
        self.assertEqual(self.current_command, self.hist.next())

    def testNextFromSomeWithPrev0(self):
        self.assertEqual(self.current_command, self.hist.next())
        self.assertEqual('y', self.hist.prev())
        self.assertEqual(self.current_command, self.hist.next())

    def testNextFromSomeWithPrev1(self):
        self.assertEqual(self.current_command, self.hist.next())
        self.assertEqual('y', self.hist.prev())
        self.assertEqual('e', self.hist.prev())
        self.assertEqual('y', self.hist.next())
        self.assertEqual(self.current_command, self.hist.next())

    def testNextFromSomeWithPrev2(self):
        self.assertEqual(self.current_command, self.hist.next())
        self.assertEqual('y', self.hist.prev())
        self.assertEqual('e', self.hist.prev())
        self.assertEqual('h', self.hist.prev())
        self.assertEqual('h', self.hist.prev())
        self.assertEqual('e', self.hist.next())
        self.assertEqual('y', self.hist.next())
        self.assertEqual(self.current_command, self.hist.next())

    def testMixed(self):
        self.assertEqual(self.current_command, self.hist.next())
        self.assertEqual(self.current_command, self.hist.next())
        self.assertEqual(self.current_command, self.hist.next())
        self.assertEqual('y', self.hist.prev())
        self.assertEqual(self.current_command, self.hist.next())
        self.assertEqual('y', self.hist.prev())
        self.assertEqual('e', self.hist.prev())
        self.assertEqual('y', self.hist.next())
        self.assertEqual(self.current_command, self.hist.next())
        self.assertEqual('y', self.hist.prev())
        self.assertEqual(self.current_command, self.hist.next())
        self.assertEqual('y', self.hist.prev())
        self.assertEqual('e', self.hist.prev())
        self.assertEqual('h', self.hist.prev())
        self.assertEqual('h', self.hist.prev())
        self.assertEqual('e', self.hist.next())
        self.assertEqual('y', self.hist.next())
        self.assertEqual(self.current_command, self.hist.next())
        self.assertEqual('y', self.hist.prev())
        self.assertEqual(self.current_command, self.hist.next())
        self.assertEqual('y', self.hist.prev())
        self.assertEqual('e', self.hist.prev())
        self.assertEqual('y', self.hist.next())
        self.assertEqual(self.current_command, self.hist.next())
        self.assertEqual('y', self.hist.prev())
        self.assertEqual(self.current_command, self.hist.next())
        self.assertEqual('y', self.hist.prev())
        self.assertEqual('e', self.hist.prev())
        self.assertEqual('h', self.hist.prev())
        self.assertEqual('h', self.hist.prev())
        self.assertEqual('e', self.hist.next())
        self.assertEqual('y', self.hist.next())
        self.assertEqual(self.current_command, self.hist.next())
        self.assertEqual(self.current_command, self.hist.next())
        self.assertEqual(self.current_command, self.hist.next())

    def testAppendResetsHistoryPointer(self):
        self.assertEqual('y', self.hist.prev())
        self.assertEqual('e', self.hist.prev())
        self.hist.append('there')
        self.assertEqual('there', self.hist.prev())
        self.assertEqual('y', self.hist.prev())
        self.assertEqual('e', self.hist.prev())
        self.assertEqual('h', self.hist.prev())
        self.assertEqual('h', self.hist.prev())


if __name__ == '__main__':
    unittest.main()
