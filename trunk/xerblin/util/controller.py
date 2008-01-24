from Tkinter import *
from tkFont import Font


class HistoryList(list):

    def __init__(self, commandline):
        self.index = -1
        self.commandline = commandline

    def prev(self):
        try:
            res = self[self.index]
        except IndexError:
            if self.index == -1:
                res = self.commandline.get()
            else:
                res = self[0]
        else:
            if self.index == -1:
                self.append(self.commandline.get())
                self.index -= 1
            self.index -= 1
        return res

    def next(self):
        if self.index == -1:
            res = self.commandline.get()
        else:
            self.index += 2
            if self.index == 0:
                self.index = -1
            res = self[self.index]
            self.index -= 1
        return res

    def append(self, item):
        item = item.strip()
        try:
            self.remove(item)
        except ValueError:
            pass
        if self.index != -1:
            self.index = -1
            self[self.index] = item
        else:
            list.append(self, item)


class XerblinController(Frame):
    '''
    A GUI CLI for a Xerblin Object
    '''

    def __init__(self, interpreter, master=None, **kw):
        Frame.__init__(self, master, **kw)
        self._createWidgets()
        self.interpreter = interpreter
        self.hist = HistoryList(self.commandline)

    ##################################################
    ##
    ##    GUI Event Callbacks
    ##

    def interpret(self, event=None):
        self.interpreter.interpret(self.getCommandLine())

    def pushString(self, event=None):
        self.interpreter.stack.append(self.getCommandLine())

    def lookup(self, event=None):
        s = self.getCommandLine()

        if s:
            s = s.split()
        else:
            return

        words = [
            word
            for word in map(self.interpreter.dictionary.get, s)
            if word is not None
            ]
                     
        if words:
            self.interpreter.stack.extend(words)

    def opendoc(self, event=None):
        self.interpreter.stack.append(self.getCommandLine())
        self.interpreter.interpret("opendoc")

    def previousCommand(self, event=None):
        self.commandline.set(self.hist.prev())

    def nextCommand(self, event=None):
        self.commandline.set(self.hist.next())

    ##
    ##################################################

    def getCommandLine(self, reset=True):
        command = self.commandline.get().strip()

        if reset:
            self.commandline.set('')
            self.hist.append(command)

        return command

    def _createWidgets(self):
        self.font = Font(
            self,
            family="helvetica",
            size=20,
            weight="bold",
            )
        self._createCommandLine(self)

    def _createCommandLine(self, frame):
        self.commandline = StringVar()
        self._commandline = Entry(
            frame,
            width=64,
            font=self.font,
            textvariable = self.commandline,
            )
        self._commandline.bind('<Return>', self.interpret)
        self._commandline.bind('<Shift-Return>', self.pushString)
        self._commandline.bind('<Control-Return>', self.lookup)
        self._commandline.bind('<Alt-Return>', self.opendoc)
        self._commandline.bind('<Up>', self.previousCommand)
        self._commandline.bind('<Down>', self.nextCommand)
        self._commandline.pack(expand=True, fill='both')
        self._commandline.focus_set()


if __name__ == '__main__':
    from xerblin import Object
    from xerblin.lib import words
    from xerblin.messaging import ListModel

    interpreter = Object(
        name='Xerblin',
        dictionary=words,
        stack=ListModel()
        )
    C = XerblinController(interpreter)
    C._root().title('Xerblin')
    C.pack(expand=True, fill=BOTH)
    C.mainloop()
