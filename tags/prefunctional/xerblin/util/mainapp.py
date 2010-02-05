'''
    Copyright (C) 2004 - 2008 Simon Forman

    This file is part of Xerblin.

    Xerblin is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

This module contains a widget class that serves as the main "controller"
for the Xerblin system.

'''
from Tkinter import Button, X


_pack_options = dict(
    expand=True,
    fill=X,
    padx=14,
    pady=14,
    ipadx=23,
    ipady=23,
    )


class MainApp:
    '''
    This is the main controller for the Xerblin system.  It simply
    contains two buttons.  The first closes the system, and the second
    shows the Guide TextViewer if you have hidden it by closing it's
    window.

    With this button and the close button the base "App" is finished.
    You can get out of the system and you can always bootstrap back into
    it if you close everything (but the main window, which must by
    definition remain open for the whole program to keep running) by
    simply opening the Guide viewer and typing in any command you want to
    run (including the commands that open the rest of the viewers in your
    world.)

    '''

    def __init__(self, frame, i=None, title='Xerblin'):
        self.i = i
        self.frame = frame
        frame.winfo_toplevel().title(title)

        self.close = Button(
            frame,
            text='Close Xerblin',
            width=23,
            command=self.doClose
            )
        self.close.pack(**_pack_options)

        self.open = Button(
            frame,
            text='Open Guide',
            command= self.doOpen
            )
        self.open.pack(**_pack_options)

    def doClose(self):
        self.i.interpret("sys.exit")

    def doOpen(self):
        self.i.interpret("Guide")


if __name__ == '__main__':
    from Tkinter import Tk
    tk = Tk()
    MainApp(tk)
    tk.mainloop()
