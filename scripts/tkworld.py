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
        self._update_listbox(self.stack_view, iterStack(stack))

    def _updateDictionary(self, dictionary):
        words = (name for name, value in items(dictionary))
        self._update_listbox(self.dictionary_view, words)

    def _update_listbox(self, listbox, contents):
        contents = list(contents)
        listbox.delete(0, END)
        listbox.insert(0, *contents)
        listbox['height'] = max(10, len(contents) + 1)

    def _createWidgets(self, root):
        self.stack_view = Listbox(root)
        self.stack_view.grid()
        self.dictionary_view = Listbox(root)
        self.dictionary_view.grid(row=0, column=1)
        self.dictionary_view.bind("<Button-1>", self.command)

    def command(self, event):
        # Calculate the relative mouse coordinates as a '@x,y' string.
        i = '@%(x)i,%(y)i' % event.__dict__
        # Look up the word under the mouse.
        i = self.dictionary_view.index(i)
        word = self.dictionary_view.get(i)
        # Execute it.
        self.world.step([word])


if __name__ == "__main__":
    tk = Tk()
    tk.title('Xerblin TkShell')

    w = HistoryListWorld()
    w.step('23 18'.split())

    t = TkShell(tk)
    t.setWorld(w)

    tk.mainloop()
