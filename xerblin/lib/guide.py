from xerblin import ExecutableWord
from xerblin.util.models import Text
from xerblin.lib.widgets.words import textviewer

TV = textviewer()


def InscribeDocumentationWords(interpreter):
    for name, text in {

    "Guide":

        '''Welcome
    
    This is the Guide.  You can close this TextViewer and then open it again later by right-clicking on the word Guide in any TextViewer.  You can also reopen this Guide by using the "Open Guide" button on the Xerblin controller widget.

    Right-clicking on a word that is also the name of a Xerblin Word will "Invoke" that word, causing it to perform its action.  You can tell if a word is a command because it will light up orange if you try right-clicking on it.  Further down in this document, you'll find a list of most of the basic words in the system.

    You can also Invoke numbers by right-clicking on them.  Invoking a number puts it onto the stack.  Try it with these numbers:

        23      17

    Once you have some numbers on the stack, you can Invoke math commands to use the interface like a calculator:  add  sub  (See below for more.)

    You can also just Invoke the word calc but first you must put some text on the stack that describes an equation.  For example, let's say you wanted to know what three times twenty-seven was.  Select the folowing text, but before you let go of the mouse button press the right button once too.  (Then let go of all the buttons.)

    3 * 27

    You should see the text of that equation on the stack.  Now Invoke calc

    Right-click on the word calc right here in the TextViewer.  You'll see that the string representation of this equation on the Stack has turned into the integer result, 81

    You can also use several mathematical functions and constants, such as sin() and pi.  Try 2 * pi * pow(23, 2) to find the area of a circle of radius 23.


Summary of TextViewer commands (for more details right-click on TextViewerGuide here.)


Invoke = Right
Open = Right, Left
Evoke = Right, Middle

Select/Point = Left
Copy = Left, Right
Cut = Left, Middle

Paste Selection = Middle
Paste TOS = Middle, Left
Pop/Paste TOS = Middle, Right

(TOS means "Top Of Stack", i.e. the item on the top of the Stack.)


[more guides here]

Viewers..

Viewers allow you to interact with the system.

Stack..

Words..

Combining Words..

Finding Codesmiths to Create and Modify Your Words..



Basic Words
==================================
==================================

Stack Words
----------------------------------
drop
dup
over
pick
rot
swap
tuck


Math Words
----------------------------------
add
div
mod
mul
sub


Logic Words
----------------------------------
and
boolean
false
not
or
true


Advanced Words
==================================
==================================

Programming Words
----------------------------------
constant
get
makewords
NewBranchWord
NewLoopWord
NewSeqWord
Nop
set
variable


Object Words
----------------------------------
createObject
execute
getstack
Inscribe
lookup
self
warranty
words


Special Words
----------------------------------
getattr
getitem
setattr
setitem
setname


List Words
----------------------------------
meta
pop
push
unmeta


Additional Words
==================================
==================================

Animation Words
----------------------------------
attach
cosinedelta
cubicdelta
quadraticdelta
run
sinedelta
timeframe


GUI Words
----------------------------------
listviewer
makewidgets
textviewer


Misc
----------------------------------
demotext
emit
s2t
sys.exit


OS Words
----------------------------------
find
ls
pwd


Time Words
----------------------------------
time
timedate

    ''',


    "TextViewerGuide":
    '''TextViewerGuide

In the Xerblin TextViewer the left mouse button functions very much like most people are used to: when pressed once it sets the insertion cursor and when pressed once and dragged it traces out a selection.

In addition, you can place selections onto the stack by pressing either the middle or right buttons before releasing the left one.

If you click the right button the selection will be copied onto the stack, if you click the middle button the selection will be cut from the current window onto the stack.

The middle button by itself pastes the current selection into the current window at the mouse position. But if you click the left button before releasing the middle button you'll paste the item on the top of the stack into the current window instead of the selection. And if you click the right button you'll paste the item on the top of the stack into the current window and also remove that item from the stack (i.e. "pop").

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

        }.iteritems():
        t = Text(name, text)
        stack = [t, interpreter]
        TV.execute(stack)
        T = stack[0]
        T.name = name
        setGeometry = T.dictionary['setGeometry']
        setGeometry.execute([[390, 123, 650, 720]])
        interpreter.dictionary[name] = T


class GuideWords(ExecutableWord):
##
##self TextViewerGuide textviewer "TextViewerGuideTextViewer" setname self Inscribe drop
##"hide" TextViewerGuideTextViewer exec
##

    '''
        * Guide = "show" Guide
        * TextViewerGuide = "show" TextViewerGuide
    '''
##    '''
##        * TextViewerGuide = "show" TextViewerGuide
##    '''
    def execute(self, stack):
        stack.insert(0, self.__doc__)


