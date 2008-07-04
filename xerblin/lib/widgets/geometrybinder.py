# -*- coding: utf-8 -*-
from xerblin.util.models import Variable, NumberVariable
from re import compile as RE
from re import VERBOSE


class GeometryVariable(NumberVariable):
    '''
    Contains an integer value.  Used with GeometryBinder.
    '''

    def __init__(self, name, initial_value, geometrybinder):
        super(GeometryVariable, self).__init__(name, initial_value)
        self.gb = geometrybinder

    def setValue(self, value):
        super(GeometryVariable, self).setValue(value)
        self.gb.handleSet()

    def __getstate__(self):
        return self.value, self.gb

    def __setstate__(self, state):
        V, GB = state
        self.inner_value = V
        self.gb = GB

    value = property(Variable.getValue, setValue)


class GeometryBinder:
    '''
    Connects a Tkinter Toplevel widget to a group of GeometryVariables
    and arranges for those Vars to be updated when the user resizes or
    moves the Toplevel, and for the Toplevel to change size or position
    as appropriate when one of the Vars is changed programmatically.
    '''

    _RE = RE('(\d+) x (\d+) ([+-] \d+) ([+-] \d+)', VERBOSE)

    def __init__(self, widget):
        self.T = widget.winfo_toplevel()
        self._configuring = False

        w, h, x, y = self.getGeometry()

        self.vars = [
            GeometryVariable('width', w, self),
            GeometryVariable('height', h, self),
            GeometryVariable('x', x, self),
            GeometryVariable('y', y, self),
            ]

        self.dict_of_vars = dict((v.name, v) for v in self.vars)

        self.T.bind('<Configure>', self.configureCallback)

    def handleSet(self):
        '''
        Called by Vars in self.vars when one changes, sets client widget's
        geometry.
        '''
        if self._configuring:
            return

        w, h, x, y = (v.value for v in self.vars)
        if x >= 0: x = '+' + str(x)
        if y >= 0: y = '+' + str(y)
        geom = "%ix%i%s%s" % (w, h, x, y)
        self.T.geometry(geom)

    def configureCallback(self, event=None):
        '''
        Deal with user changing the size or location of window.
        '''
        self._configuring = True
        try:
            for var, value in zip(self.vars, self.getGeometry()):
                if var.value != value:
                    var.value = value
        finally:
            self._configuring = False

    def getGeometry(self):
        '''
        Return the geometry of Toplevel as four integers.
        '''
        geom = self.T.geometry()
        m = self._RE.match(geom)
        assert m is not None, 'wtf? bad geometry string? %r)' % (geom,)
        w, h, x, y = map(int, m.groups())
        return w, h, x, y

    def __getstate__(self):
        return (
            self.T,
            self.vars,
            self.dict_of_vars,
            )

    def __setstate__(self, state):
        T, V, D = state
        self.T = T
        self._configuring = False
        self.vars = V
        self.dict_of_vars = D
        self.handleSet()
        self.T.bind('<Configure>', self.configureCallback)


if __name__ == '__main__':
    from Tkinter import Tk

    root = Tk()
    root.update_idletasks()
    gb = GeometryBinder(root)
    root.mainloop()

##  Notes:
##
##  4.10. Geometry strings
##
##      A geometry string is a standard way of describing the size and
##      location of a top-level window on a desktop.
##
##      A geometry string has this general form:
##            "wxh±x±y"
##      where:
##
##      • The w and h parts give the window width and height in pixels.
##      They are separated by the character "x".
##
##      • If the next part has the form +x, it specifies that the left side
##      of the window should be x pixels from the left side of the desktop.
##      If it has the form -x, the right side of the window is x pixels
##      from the right side of the desktop.
##
##      • If the next part has the form +y, it specifies that the top of
##      the window should be y pixels below the top of the desktop. If it
##      has the form -y, the bottom of the window will be y pixels above
##      the bottom edge of the desktop.
##
##      For example, a window created with geometry="120x50-0+20" would be
##      120 pixels wide by 50 pixels high, and its top right corner will be
##      along the right edge of the desktop and 20 pixels below the top
##      edge.
##



#  We want four Variables that each represent one of x, y, width, height,
#  of a given Toplevel widget; and, when you set one of those Vars it
#  will cause the Toplevel widget to resize.  Also, if you resize the
#  window it should cause the Vars to update their values (triggering
#  notify messages.)
#
#  Perhaps what we really want is one four-valued data object that you
#  can access just like a list.  Nah.  K.I.S.S.

