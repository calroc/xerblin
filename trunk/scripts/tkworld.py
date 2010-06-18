#!/usr/bin/env python
'''
A simple Tkinter GUI.
'''
from Tkinter import *
from xerblin.btree import items
from xerblin.stack import iterStack
from xerblin.world import HistoryListWorld


class TkShell:

    def __init__(self, root):
        self._createWidgets(root)

    def setWorld(self, world):
        self.world = world
        world.changeView(self.view)

    def view(self, interpreter):
        stack, dictionary = interpreter
        self._updateStack(stack)
        self._updateDictionary(dictionary)

    def _updateStack(self, stack):
        print 'Stack:'
        for item in iterStack(stack):
            print ' ', item
        print '------\n'

    def _updateDictionary(self, dictionary):
        print 'Dictionary:'
        for name, value in items(dictionary):
            print name,
        print

    def _createWidgets(self, root):
        pass


if __name__ == "__main__":

    w = HistoryListWorld()

    t = TkShell(None)
    t.setWorld(w)

    while True:
        try:
            command = raw_input('> ').split()
        except EOFError:
            break
        w.step(command)
