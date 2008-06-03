import Tkinter
from pygoo import toXML, _merge_subelements_to_options, _grid
from xerblin import Object, ExecutableWord
from xerblin.lib.constant import Constant
from xerblin.lib.widgets.widgetwrapper import (
    XerblinWindow,
    iconifyToggle,
    setGeometry,
    )
from xerblin.lib.widgets.geometrybinder import GeometryBinder
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.messaging import ListModel
from xerblin.util.models import Text
from xerblin.lib.pygoo.wrappers import (
    GraphWrapper,
    CommandWrapper,
    ButtonWrapper,
    )


WIDGET_TYPES = dict(
    Button = ButtonWrapper,
    Canvas = Tkinter.Canvas,
    Checkbutton = Tkinter.Checkbutton,
    Entry = Tkinter.Entry,
    Graph = GraphWrapper,
    Label = Tkinter.Label,
    Listbox = Tkinter.Listbox,
    Scale = Tkinter.Scale,
    Radiobutton = Tkinter.Radiobutton,
    Text = Tkinter.Text,
    )


def realize(master, obj, element, namespace):
    '''
    Grok XML description into actual widgets.

    master - Tkinter container widget to use as this widget's parent.
    element - ElementTree Element describing the desired widget.
    namespace - An Object to bind child widgets to, if their 'name'
        attribute is specified in the element XML.
    '''

    options = dict(element.attrib)
    name = options.pop('name', None)
    command = options.pop('command', None)
    grid = None

    widget_type = element.tag.capitalize()

    if widget_type == "Frame":

        widget = Tkinter.Frame(master, **options)

        for subelement in element:

            if subelement.tag.lower() == "grid":
                grid = subelement
                continue

            realize(widget, obj, subelement, namespace)

    else:
        if element:

            D = dict((n.tag.lower(), n) for n in element)

            grid = D.pop('grid', None)

            _merge_subelements_to_options(D.values(), options)

        widget_factory = WIDGET_TYPES[element.tag.capitalize()]

        widget = widget_factory(master, **options)

    if name: namespace[name] = widget

    if widget_type == 'Button' and command:
        widget['command'] = CommandWrapper(obj, command)

    _grid(widget, grid)

    return widget


class WidgetHolder(ExecutableWord):
    '''
    A sort of constant Word that provides read-only (i.e you can't set
    its value attribute) access to a Tkinter widget at runtime.  It does
    this by defering the actual widget retrieval to its WidgetsObject
    "parent".  This also allows it to be pickled as a (name, w-obj) tuple
    which then reduce pickling of "widgets" to the pickling of the
    WidgetsObject that originally created their corresponding
    WidgetHolder objects.

    In practice you can access and set the Tk(-inter) attributes of a
    widget by the following idiom (where WO is the WidgetsObject):

        WO "widget-name" lookup
    
            (Gets the WidgetHolder, which is safe to pickle anywhere in
            the system.  Once you have it, follow with... )

        get "attribute-name" getitem

            (to get an attribute's value, and)

        get "attribute-name" value setitem

            (to set a value.)

    I'm sorry to report that these attributes won't be saved along with
    the WidgetHolders, although I plan to remedy that in the future.  For
    now, if you change attributes at runtime from what you specify in the
    widget source and then try to restore a backup made after that, those
    changes will be lost.  So, specify what you want in the source, and
    only use attribute changes for transient signals and whatnot.
    '''

    def __init__(self, name, widgetsobject):
        ExecutableWord.__init__(self, name)
        self.widgetsobject = widgetsobject

    def execute(self, stack):
        stack.insert(0, self.value)

    def getValue(self):
        return self.widgetsobject.getNamedWidget(self.name)

    value = property(getValue)

    def __getstate__(self):
        return self.name, self.widgetsobject

    def __setstate__(self, state):
        name, widgetsobject = state
        self.name = name
        self.widgetsobject = widgetsobject


class EntryHolder(WidgetHolder):
    '''
    I.e.,

        EH "value" "Iloveyou" setattr

    '''

    def execute(self, stack):
        stack.insert(0, self._get_widget())

    def _get_widget(self):
        return self.widgetsobject.getNamedWidget(self.name)

    def getValue(self):
        return self._get_widget().get()

    def setValue(self, value):
        widget = self._get_widget()
        widget.delete(0, Tkinter.END)
        widget.select_clear()
        widget.insert(0, value)

    value = property(getValue, setValue)

    def __getstate__(self):
        return self.name, self.widgetsobject, self.value

    def __setstate__(self, state):
        name, widgetsobject, value = state
        self.name = name
        self.widgetsobject = widgetsobject
        self._set_me = value


class WidgetsObject(Object):

    def __getstate__(self):
        return (
            self.name,
            self.stack,
            self.dictionary,
            self.context,
            )

    def __setstate__(self, state):
        name, stack, D, context = state
        source = D['source'].value
        top = D['window'].value

        self.namespace = {}

        for widget in toXML(source):
            realize(top, context, widget, self.namespace)

        Object.__init__(self, name, stack=stack, dictionary=D)
        self.context = context

        for eh in D.itervalues():
            if isinstance(eh, EntryHolder):
                eh.value = eh._set_me

    def getNamedWidget(self, name):
        return self.namespace[name]

    def __init__(self, context, source, name=None):
        self.context = context

        top = XerblinWindow()
        top.title(name or 'Xerblin Widgets')

        # Build an initial dictionary for our new Object.
        D = dict(
            window=Constant('window', top),
            source=Constant('source', source),
            iconifyToggle=iconifyToggle(top),
            setGeometry=setGeometry(top),
            )

        self.namespace = {}

        for widget in toXML(source):
            realize(top, context, widget, self.namespace)

        for name, widget in self.namespace.iteritems():
            if isinstance(widget, Tkinter.Entry):
                D[name] = EntryHolder(name, self)
            else:
                D[name] = WidgetHolder(name, self)

        gb = GeometryBinder(top)

        # Add in Vars for width, height, x, and y.
        D.update(gb.dict_of_vars)

        Object.__init__(self, name, dictionary=D)


class makewidgets(
    StackLen(2),
    StackType(0, (str, Text, ListModel)),
    StackType(1, Object),
    ExecutableWord
    ):
    '''
    Convert a source text into widgets in a window.
    '''
    def execute(self, stack):
        source, obj = stack[:2]
        source = self._source(source)
        window = WidgetsObject(obj, source)
        stack[:2] = [window]

    def _source(self, source):
        if isinstance(source, str):
            return source
        if isinstance(source, Text):
            return source.value
        if isinstance(source, ListModel):
            G = (self._source(thing) for thing in source)
            return ''.join(G)
        return ''
