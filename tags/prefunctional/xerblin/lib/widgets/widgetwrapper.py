'''
    Copyright (C) 2004 - 2009 Simon Forman

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

This module defines a class,

    XerblinWindow - A Tkinter Toplevel that is adapted to serve as a
        "hull" for Xerblin Viewer objects.

and a factory function,

    makeViewer() - Takes a title string, model object, Viewer class,
        optional geometry string (see Tkinter docs or setGeometry word in
        this module), and options (optional) for the Viewer instance
        created and for the Toplevel widget itself, and create a Toplevel
        widget with a Viewer instance for that model.

        Returns a new Xerblin Object with the Toplevel "hull", the Viewer
        instance, and the model in its dictionary, as well as a few
        pre-defined words for manipulating them (see below.)

This module also contains classes for three ExecutableWords that the
makeViewer() factory function creates for each Viewer widget/Object.

    hide - Hides the widget. It won't show up in the system taskbar.
    show - Shows the (previously hidden) widget.
    setGeometry - Change the dimensions or location of the widget.


'''
from Tkinter import Toplevel
from xerblin import Object, ExecutableWord
from xerblin.lib.programming import Constant
from xerblin.lib.widgets.textviewer import TextViewer
from xerblin.util.stackcheckers import StackLen


class XerblinWindow(Toplevel):
    '''
    Window class with support for pickling and helper methods for showing
    and hiding the window.  Also, the WM_DELETE_WINDOW protocol, i.e. the
    callback for the little "x" close-this-window button on the title bar
    is hooked to the hide method.  This means that you don't actually
    destroy the window when you "close" it.  It remains and can be
    reopened by calling the show method.

    This window class is used by the Viewer classes as a frame (see the
    makeViewer() function) and ExecutableWords are created to call those
    show and hide methods, and to change the geometry of the window. 
    '''

    def __init__(self, *a, **b):
        Toplevel.__init__(self, *a, **b)
        self._geometry = ''
        self._iconified = False
        self.protocol("WM_DELETE_WINDOW", self._byebye)

    def _byebye(self, event=None):
        if not self._iconified:
            self._geometry = self.geometry()
            self.withdraw()
            self._iconified = True

    def _hello(self):
        if self._iconified:
            self.wm_deiconify()
            self.geometry(self._geometry)
            self._iconified = False

    def __getstate__(self):
        return (
            self._geometry or self.geometry(),
            self.title(),
            self._iconified,
            )

    def __setstate__(self, state):
        geom, title, iconified = state
        self.__init__()
        self.title(title)
        self._geometry = geom
        if geom:
            self.geometry(geom)
        self._iconified = iconified
        if iconified:
            self.withdraw()


class hide(ExecutableWord):
    '''
    Hide window.
    '''
    def __init__(self, window):
        ExecutableWord.__init__(self, None)
        self.window = window

    def execute(self, stack):
        self.window._byebye()


class show(hide):
    '''
    Show window.
    '''
    def execute(self, stack):
        self.window._hello()


class setGeometry(StackLen(1), ExecutableWord):
    '''
    Set the geometry of self.window.  Expects a list of four numbers:
    x, y, width, height.
    '''
    def __init__(self, window):
        ExecutableWord.__init__(self, None)
        self.window = window

    def execute(self, stack):
        x, y, w, h = stack[0]
        pattern = ''.join((
            '%ix%i', # width and height
            '+-'[x < 0], # correct operator for x
            '%i',
            '+-'[y < 0], # correct operator for y
            '%i'
            ))
        geom = pattern % (w, h, x, y)
        self.window.geometry(geom)
        del stack[0]
        self.window.update_idletasks()


def makeViewer(
    title,
    model,
    ViewerClass=TextViewer,
    geom=None,
    viewer_options={},
    window_options={},
    ):
    '''
    Given a title string, a model object (some object subclassing the
    ModelMixin class), and a Viewer class, as well as optional geometry
    string and option dicts for the Viewer and XerblinWindow classes,
    create and return an Object encapsulating the model, viewer, and
    three ExecutableWord commands "show", "hide" and "setGeometry" which
    act on the Toplevel XerblinWindow.
    '''

    # Prepare a XerblinWindow Toplevel object.
    T = XerblinWindow(**window_options)
    T.title(title)
    if geom:
        T.geometry(geom)

    # Create the viewer inside our window.
    viewer = ViewerClass(model, T, **viewer_options)

    # Build an initial dictionary for our new Object.
    D = dict(
        model=Constant('model', model),
        viewer=Constant('viewer', viewer),
        show=show(T),
        hide=hide(T),
        setGeometry=setGeometry(T),
        )

    # Create the Object.
    o = Object(dictionary=D)

    return o


if __name__ == "__main__":
    from Tkinter import mainloop
    from xerblin.lib.programming import Variable
    o = makeViewer(
        'Demo XerblinWindow with TextViewer',
        Variable('hi', 'there'),
        viewer_options=dict(interpreter=None),
        )
    mainloop()
