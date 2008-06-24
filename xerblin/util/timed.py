

class Timed:
    '''
    This class handles saving after changes for the root viewer class.
    Call trigger() as often as you want, and it will call the callback
    delay ms after the last call to trigger().
    '''

    def __init__(self, tk, callback, delay=450):
        self.tk = tk
        self.callback = callback
        self.delay = delay

    def trigger(self):
        self._cancelSave()
        self._saveAfter(self.delay)

    def _saveFunc(self):
        self._save = None
        self.callback()

    def _cancelSave(self):
        try: save = self._save
        except AttributeError: pass
        else:
            if save:
                self.tk.after_cancel(save)
                self._save = None

    def _saveAfter(self, delay):
        self._save = self.tk.after(delay, self._saveFunc)



if __name__ == '__main__':
    import Tkinter

    B = Tkinter.Button(
        text='Click me to flash.\n(Only after last click.)',
        width=20,
        height=8
        )
    B.pack()

    tm = Timed(B, B.flash)
    B['command'] = tm.trigger

    Tkinter.mainloop()
