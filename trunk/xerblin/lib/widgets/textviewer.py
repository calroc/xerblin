from Tkinter import Text as TkText
from Tkinter import (
    Toplevel,
    Label,
    END,
    GROOVE,
    FLAT,
    INSERT,
    DISABLED,
    NORMAL,
    )
from Tkdnd import DndHandler

from xerblin import ExecutableWord
from xerblin.messaging import ModelMixin, Viewer, ListModel
from xerblin.util.models import Text
from xerblin.lib.widgets.stackwidgets import ViewerMakerMixin
from xerblin.lib.widgets.controllerlistbox import SourceWrapper
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.util.editor import editParagraphModel


class dnd(DndHandler):
    def on_motion(self, event):
        try:
            DndHandler.on_motion(self, event)
        finally:
            return "break"


class TextViewerWidget(TkText):
    '''
    A Tk Text subclass to display the contents of a SequentialExecutableWord.
    '''

    def __init__(self, viewer, master=None,  **kw):

        # You can't actually edit this sucker in-place.
        kw.setdefault('state', DISABLED)
        kw.setdefault('wrap', 'word')

        TkText.__init__(self, master, **kw)
        self.viewer = viewer
        self.bind('<Button-1>', self.startDrag)
        self.bind('<Button-3>', self.onClick)

    def startDrag(self, event):
        index = self.index("@%i,%i" % (event.x, event.y))
        thing = self.thingAt(index)
        if thing:
            source = thing.model
            source = SourceWrapper(source, self, index)
            event.num = 1 # Don't ask. (See Tkdnd.py)
            dnd(source, event)
        return "break"

    def onClick(self, event):
        # Find the pv, ew, or nothing..
        index = self.index("@%i,%i" % (event.x, event.y))
        if self._getParagraphTagAt(index):
            return

        model = Text('noname', '')

        if index == '1.0':
            self.viewer.model.insert(0, model)
        else:
            self.viewer.model.append(model)

        editParagraphModel(model)

    def dnd_accept(self, source, event):
        self.focus_force()
##        print 'dnd_accept', self, source, event
        return self

    def dnd_enter(self, source, event):
##        print 'dnd_enter', self, source, event
        pass

    def dnd_motion(self, source, event):
        x = event.x_root - self.winfo_rootx()
        y = event.y_root - self.winfo_rooty()
        index = self.index("@%i,%i" % (x, y))
        thing = self.thingAt(index)
##        print 'dnd_motion', self, source, event
        pass

    def dnd_leave(self, source, event):
##        print 'dnd_leave', self, source, event
        pass

    def dnd_commit(self, source, event):
##        print 'dnd_commit', self, source, event
        x = event.x_root - self.winfo_rootx()
        y = event.y_root - self.winfo_rooty()
        index = self.index("@%i,%i" % (x, y))

        thing = self.thingAt(index)
        if thing:
            index = thing.model_index
        else:
            index = len(self.viewer.model)

        self.viewer.model.insert(index, source.source)

    def thingAt(self, index):
        '''
        Return the ParagraphViewer or WordViewer at index or None.
        '''
        return self.paragraphAt(index) or self.widgetAt(index)

    def paragraphAt(self, index):
        '''
        Return the ParagraphViewer at index or None.
        '''
        tag = self._getParagraphTagAt(index)
        if tag:
            return self._getParagraphViewer(tag)

    def widgetAt(self, index):
        '''
        Return the WordViewer at index or None.
        '''
        contents = self.dump(index)
        if not contents:
            return
        contents = dict((t, n) for t, n, _ in contents)
        try:
            widget = contents['window']
        except KeyError:
            return
        widget = self.nametowidget(widget)
        return widget.word_viewer

    def _getParagraphTagAt(self, index=INSERT):
        '''
        Return the paragraph tag at index or None.
        '''
        tags = self.tag_names(index)
        if not tags:
            return

        # pick out the paragraph_* tag
        tags = [t for t in tags if t.startswith('paragraph_')]
        if not tags:
            return

        assert len(tags) == 1, repr(tags)
        return tags[0]

    def _getParagraphViewer(self, tag):
        '''
        Return the ParagraphViewer that has the given tag.
        '''
        pvs = list(self.viewer.kidsWho(self._tagEquals(tag)))
        assert len(pvs) == 1, repr(pvs)
        return pvs[0]

    @staticmethod
    def _tagEquals(tag):
        return lambda n: hasattr(n, 'tag') and n.tag == tag


class ParagraphViewer(Viewer):

    def __init__(self, text_viewer, model, model_index):
        Viewer.__init__(self, model)
        self.text_viewer = text_viewer
        self.model_index = model_index
        self.tag = 'paragraph_%i' % id(self)
        text_viewer.text.tag_config(self.tag, borderwidth=2)
        text_viewer.insert(END, model.value, self.tag)

        tbind = text_viewer.text.tag_bind
        tbind(self.tag, '<Enter>', self.mouseEnterCallback)
        tbind(self.tag, '<Leave>', self.mouseLeaveCallback)
        tbind(self.tag, '<Button-3>', self.clickCallback)

    def mouseEnterCallback(self, event=None):
        tconfig = self.text_viewer.text.tag_config
        tconfig(self.tag, relief=GROOVE)
        tconfig(self.tag, background='white')

    def mouseLeaveCallback(self, event=None):
        T = self.text_viewer.text
        T.tag_config(self.tag, relief=FLAT)
        T.tag_config(self.tag, background=T['background'])

    def clickCallback(self, event=None):
        editParagraphModel(self.model)

    def nearestEnd(self, index):
        T = self.text_viewer.text
        tags = first, last = self.tag + '.first', self.tag + '.last'

        total = len(T.get(first, last))
        head = len(T.get(first, index))
        assert head <= total

        tail = total - head
        return T.index(tags[tail > head])


class WordViewer(Viewer):
    '''
    Contains an ExecutableWord.
    '''

    class WordWidget(Label):
        def __init__(self, T, word_viewer, **kw):
            self.word_viewer = word_viewer
            Label.__init__(self, T, {}, **kw)
            self.bind('<Destroy>', self._onDestroy)

        def registerIndex(self, index):
            self.index = index

        def _onDestroy(self, event=None):
            # Be nice to memory.  These widgets hang about in the TkText's
            # 'children' dict. :(
            del self.word_viewer
            self.destroy()

    def __init__(self, text_viewer, model, model_index):
        Viewer.__init__(self, model)
        self.text_viewer = text_viewer
        self.model_index = model_index
        self._createWidget(END)

    def _createWidget(self, index):
        T = self.text_viewer.text
        W = self._word_widget = self.WordWidget(
            T,
            self,
            text=self.model.name,
            padx='0',
            pady='0',
            relief=GROOVE,
            font=T['font'],
            fg=T['fg'],
            bg=T['bg'],
            )
        T.window_create(index, window=W)
        W.registerIndex(T.index(index))
        W.bind('<Enter>', self._mouseEnterCallback)
        W.bind('<Leave>', self._mouseLeaveCallback)
##        W.bind('', )

    def _mouseEnterCallback(self, event=None):
        self._word_widget['bg'] = 'lightgreen'

    def _mouseLeaveCallback(self, event=None):
        self._word_widget['bg'] = self.text_viewer.text['bg']


class TextViewer(Viewer):

    def __init__(self, model, master=None, **kw):
        Viewer.__init__(self, model)
        self.text = TextViewerWidget(self, master, **kw)
        self.text.pack(expand=True, fill='both')
        self.update()
        ModelMixin.root.addChild(self)

    def insert(self, *args):
        t = self.text
        t['state'] = NORMAL
        try:
            return t.insert(*args)
        finally:
            t['state'] = DISABLED

    def handle(self, message):
        if not self._checkMessage(message):
            return False

        if message.model is self.model or self._dispatch(message):
            self.update()
            return True

        return False

    def update(self):
        self.text['state'] = NORMAL
        try:
            self.text.delete('0.0', END)
            new_kids = []
            for i, item in enumerate(self.model):

                if isinstance(item, Text):
                    new_kids.append(ParagraphViewer(self, item, i))

                elif isinstance(item, ExecutableWord):
                    new_kids.append(WordViewer(self, item, i))

            self.replaceChildren(new_kids)
            self._clearOldTags(new_kids)
        finally:
            self.text['state'] = DISABLED

    def _clearOldTags(self, new_kids):
        new_tags = set(
            kid.tag
            for kid in new_kids
            if hasattr(kid, 'tag')
            )

        have_tags = set(
            tag
            for tag in self.text.tag_names()
            if tag.startswith('paragraph_')
            )

        gone_tags = have_tags - new_tags

        for tag in gone_tags:
            self.text.tag_delete(tag)





class textviewer(
    ViewerMakerMixin,
    StackLen(1),
    StackType(0, ListModel),
    ExecutableWord
    ):
    '''
    Given a ListModel on the stack open a ListViewer on it.
    '''
    def execute(self, stack):
        model = stack[-1]
        name = "%s TextViewer" % (id(model),)
        stack[-1] = self._makeViewer(model, name, TextViewer)


class s2t(StackLen(1), StackType(0, str), ExecutableWord):
    '''
    Convert a string to a Text.
    '''
    def execute(self, stack):
        s = stack[-1]
        p = Text('noname', s)
        stack[-1] = p


