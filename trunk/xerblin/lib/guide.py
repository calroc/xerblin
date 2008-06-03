from xerblin import ExecutableWord


class Guide(ExecutableWord):
    '''Xerblin User's Guide

Xerblin is a simple system designed to allow normal people to
get the most out of their computer with the least muss and fuss.

Once you know how to use Xerblin, you'll be able to use your computer
much easier and get more use out of the incredible information appliance
in front of you.


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

    '''
    def execute(self, stack):
        stack.insert(0, self.__doc__)


class TextViewerGuide(ExecutableWord):
    '''TextViewer Guide

In the Xerblin TextViewer the left mouse button functions very much like most people are used to: when pressed once it sets the insertion cursor and when pressed once and dragged it traces out a selection.

In addition, you can place selections onto the stack by pressing either the middle or right buttons before releasing the left one. If you click the right button the selection will be copied onto the stack, if you click the middle button the selection will be cut from the current window onto the stack.

The middle button by itself pastes the current X selection into the current window at the mouse position, just like a normal X app. But if you click the left button before releasing the middle button you'll paste the item on the top of the stack into the current (Xerblin) window instead of the X selection. And if you click the right button you'll paste the item on the top of the stack into the current window and also remove that item from the stack (i.e. "pop").

The right button by itself will execute the command word under the mouse. However, if you click the left button before releasing the right button the system will instead execute the "opendoc" command word on the text under the mouse. And if instead you click the middle button before releasing the right button the system will attempt to "lookup" the command word under the mouse and, if found, place that ExecutableWord? onto the stack. 
    '''
    def execute(self, stack):
        stack.insert(0, self.__doc__)


class GuideWords(ExecutableWord):
##
##self TextViewerGuide textviewer "TextViewerGuideTextViewer" setname self Inscribe drop
##"hide" TextViewerGuideTextViewer exec
##

    '''

        show = "show"
        * Guide = show GuideViewer
        * TextViewerGuide = show TextViewerGuideTextViewer
        

    '''
    def execute(self, stack):
        stack.insert(0, self.__doc__)


