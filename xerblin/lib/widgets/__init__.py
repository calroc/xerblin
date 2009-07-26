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

'''
from xerblin import ExecutableWord, SimpleInterpreter
from xerblin.messaging import ListModel
from xerblin.lib.programming import Variable
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.lib.widgets.widgetwrapper import makeViewer
from xerblin.lib.widgets.listviewer import SequenceController
from xerblin.lib.widgets.textviewer import TextViewer


class listviewer(
    StackLen(1),
    StackType(0, ListModel),
    ExecutableWord
    ):
    '''
    Given a ListModel on the stack open a ListViewer on it.
    '''
    def execute(self, stack):
        model = stack[0]
        name = "ListViewer %s" % (id(model),)
        stack[0] = makeViewer(name, model, SequenceController)


class textviewer(
    StackLen(2),
    StackType(0, (Variable, basestring)),
    StackType(1, SimpleInterpreter),
    ExecutableWord
    ):
    '''textviewer

    Given some text and an Object on the stack open a textviewer on the text.

In the Xerblin textviewer the left mouse button functions very much like most people are used to: when pressed once it sets the insertion cursor and when pressed once and dragged it traces out a selection.

In addition, you can place selections onto the stack by pressing either the middle or right buttons before releasing the left one.

If you click the right button the selection will be copied onto the stack, if you click the middle button the selection will be cut from the current window onto the stack.

The middle button by itself pastes the current selection into the current window at the mouse position. But if you click the left button before releasing the middle button you'll paste the item on the top of the stack into the current window instead of the selection. And if you click the right button you'll paste the item on the top of the stack into the current window and also remove that item from the stack (i.e. "pop").

The middle button also allows you to "grab" and scroll window contents.  If you click the middle button on a textviewer and move the mouse you'll scroll the text instead of pasting.

The right button by itself will invoke the command word under the mouse.  However, if you click the left button before releasing the right button the system will instead open a viewer on the command word under the mouse. And if instead you click the middle button before releasing the right button the system will attempt to evoke the command word under the mouse, that is, it will find the word in the Dictionary and place it onto the stack. 


Summary

Right Button First = Invoke
    or then the Left Button = Open
    or then the Middle Button = Evoke (put it on the Stack)

Left Button First = Point (set the cursor location)
    and drag = trace out a selection (text) or copy item (list)
        then the Right Button = Copy selected text to Stack
        or then the Middle Button = Cut selected text to Stack

Middle Button = Paste current selection to pointer.
    or then the Left Button = Copy item on Stack to pointer.
    or then the Right Button = "Pop" item on Stack to pointer.



Summary of Summary
(TOS means "Top Of Stack", i.e. the item on the top of the Stack.)

Invoke = Right
Open = Right, Left
Evoke = Right, Middle

Select/Point = Left
Copy = Left, Right
Cut = Left, Middle

Paste Selection = Middle
Paste TOS = Middle, Left
Pop/Paste TOS = Middle, Right

    '''
    def execute(self, stack):
        model, interpreter = stack[:2]
        if not isinstance(model, Variable):
            v = Variable('noname')
            v.value = str(model)
            model = v
        name = "TextViewer %s" % (id(model),)
        viewer = makeViewer(
            name,
            model,
            TextViewer,
            viewer_options={'interpreter':interpreter},
            )
        stack[:2] = [viewer]


__all__ = [
    'listviewer',
    'textviewer',
    ]
