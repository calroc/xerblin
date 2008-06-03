from Tkinter import Text, Toplevel, Frame, END


class SaveyText(Text):

    _saveDelay = 400

    def __init__(self, P, master=None,  **kw):
        Text.__init__(self, master, **kw)
        self.P = P
        self.insert(END, P.value)
        self._save = None
        self._clearModifiedFlag()
        self.bind('<<Modified>>', self._beenModified)

    def _beenModified(self, event):
        if self._resetting_modified_flag:
            return
        self._clearModifiedFlag()
        self.save()

    def _clearModifiedFlag(self):
        self._resetting_modified_flag = True
        try:
            self.tk.call(self._w, 'edit', 'modified', 0)
        finally:
            self._resetting_modified_flag = False

    def save(self):
        '''
        Call _saveFunc() after a certain amount of idle time.

        Called by _beenModified().
        '''
        self._cancelSave()
        self._saveAfter(self._saveDelay)

    def forceSave(self):
        self._cancelSave()
        self._saveFunc()

    def _saveFunc(self):
        self._save = None
        text = self.get('0.0', 'end -1 chars')
        self.P.value = text

    def _saveAfter(self, delay):
        '''
        Trigger a cancel-able call to _saveFunc() after delay milliseconds.
        '''
        self._save = self.after(delay, self._saveFunc)

    def _cancelSave(self):
        if self._save:
            self.after_cancel(self._save)
            self._save = None


class Editor(Frame):

    def __init__(self, P, master=None, **kw):
        Frame.__init__(self, master, **kw)
        self.P = P
        self._createWidgets()

    def _createWidgets(self):
        self.T = SaveyText(
            self.P,
            self,
            bg='white',
            width=73,
            height=10,
            wrap='word',
            undo=True,
            )
        self.T.pack(expand=True, fill='both')
        self.T.focus_set()


def editParagraphModel(model):
    T = Toplevel()
    T.title('Editing %s' % (model.name,))
    E = Editor(model, T)
    E.pack(expand=True, fill='both')

    def destroy(event=None):
        E.T.forceSave()
        T.destroy()

    T.protocol("WM_DELETE_WINDOW", destroy)


if __name__ == '__main__':
    from xerblin.util.models import Text
    P = Text('noname')
    P.value = 'Hey there baby!'
##    t = SaveyText(P)
    E = Editor(P)
    E.pack(expand=True, fill='both')
    E.mainloop()
##    t.pack(expand=True, fill='both')
##    t.mainloop()
    
