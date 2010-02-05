#!/usr/bin/env python
import xerblin
import unittest
from string import whitespace

class TestInterpeter(unittest.TestCase):

    def setUp(self):
        self.interp = xerblin.Interpreter(stack=[])

    def testinterpret(self):
        i = self.interp.interpret
        s = self.interp.stack

        for n in (1, 1.0, [], {}, (), object, object()):
            self.assertRaises(AssertionError, i, n)

        self.assertEqual([], s, `s`)

        i('23')
        self.assertEqual([23], s)

        i('23.0')
        self.assertEqual([23, 23.0], s)

        i('Nop')
        self.assertEqual([23, 23.0], s)

        self.assertRaises(xerblin.UnknownWordError, i, 'notme')

        # Test that blankspace is discerned as command separators.
        for spc in whitespace:
            del s[:]
            self.assertEqual([], s)

            i('23%s2.3' % spc)
            self.assertEqual([23, 2.3], s)

    def testexecute(self):
        e = self.interp.execute_name

        self.assertRaises(xerblin.UnknownWordError, e, 'notme')

        e('Nop')

    def testexecute_word(self):
        e = self.interp.execute_word

        e(xerblin.Nop)


    def test_become(self):
        b = self.interp._become

        d = self.interp.dictionary
        s = self.interp.stack

        D = d.copy()
        S = [23, 18, 1.999999, 'str', xerblin.Nop]

        d.clear()

        self.assertEqual([], s)
        self.assertEqual({}, d)

        b(S, D)

        self.assertEqual(S, s)
        self.assertEqual(D, d)

        
class TestObject(unittest.TestCase):

    def setUp(self):
        self.object = xerblin.Object()

    def testHasExecute(self):
        self.assert_('execute' in self.object.dictionary)

    def testExecute(self):

        S = []

        class x(xerblin.ExecutableWord):
            def execute(self, stack):
                S.append(repr(stack))

        self.object.dictionary['x'] = x()
        self.object.stack.extend(range(23,26))

        stack = [1, 2, 3, 'x']
        self.object.execute(stack)

        self.assertEqual(S[0], '[23, 24, 25, [1, 2, 3]]')











if __name__ == '__main__':
    unittest.main()
