from Tkinter import Toplevel
from xerblin import Object, ExecutableWord
from xerblin.messaging import ListModel
from xerblin.lib.constant import Constant
##from xerblin.lib.variable import variable
from xerblin.lib.widgets.geometrybinder import GeometryBinder
from xerblin.lib.widgets.TextViewer import TextViewer
from xerblin.util.stackcheckers import StackLen


class XerblinWindow(Toplevel):

    def __init__(self, *a, **b):
        Toplevel.__init__(self, *a, **b)
        self._geometry = ''
        self._iconified = False
        self.protocol("WM_DELETE_WINDOW", self._byebye)

    def iconifyToggle(self):
        if self._iconified:
            self._hello()
        else:
            self._byebye()

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


class iconifyToggle(ExecutableWord):
    '''
    Call iconifyToggle() method of self.window.
    '''
    def __init__(self, window):
        ExecutableWord.__init__(self, None)
        self.window = window

    def execute(self, stack):
        self.window.iconifyToggle()


class hide(iconifyToggle):
    '''
    Hide window.
    '''
    def execute(self, stack):
        self.window._byebye()


class show(iconifyToggle):
    '''
    Show window.
    '''
    def execute(self, stack):
        self.window._hello()


class setGeometry(StackLen(1), ExecutableWord):
    '''
    Set the geometry of self.window.
    '''
    def __init__(self, window):
        ExecutableWord.__init__(self, None)
        self.window = window

    def execute(self, stack):
        x, y, w, h = stack[0]
        geom = '%ix%i+%i+%i' % (w, h, x, y)
        self.window.geometry(geom)
        del stack[0]
        self.window.update_idletasks()


def MakeViewer(
    title,
    model,
    ViewerClass=TextViewer,
    geom=None,
    viewer_options={},
    window_options={},
    ):

    # Prepare a XerblinWindow Toplevel object.
    T = XerblinWindow(**window_options)
    T.title(title)
    if geom:
        T.geometry(geom)

    # Create the viewer inside our window.
    viewer = ViewerClass(model, T, **viewer_options)

    # "Hook" the geometry of the window to some xerblin vars.
    gb = GeometryBinder(T)

    # Build an initial dictionary for our new Object.
    D = dict(
        model=Constant('model', model),
        viewer=Constant('viewer', viewer),
        iconifyToggle=iconifyToggle(T),
        show=show(T),
        hide=hide(T),
        setGeometry=setGeometry(T),
        )

    # Add in Vars for width, height, x, and y.
    D.update(gb.dict_of_vars)

    # Create the Object.
    o = Object(dictionary=D)
    o._gb = gb # Don't let's garbage collect the GeometryBinder, eh what?

    return o


if __name__ == "__main__":
    o = MakeViewer('Demo XerblinWindow with TextViewer', ListModel())

##t = XerblinWindow()
##t.title("Banana")

# t.iconify(); t.deiconify()
# t.withdraw(); t.wm_deiconify()
