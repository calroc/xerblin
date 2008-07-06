'''
Helper module for startup.  The basic Documentation words are defined here.
'''
from xerblin import ExecutableWord
from xerblin.util.models import Text


# This dict contains named documentation strings.  These strings will be made
# into TextViewers in the main interpreter.
Documentation = dict(

    Guide = '''Welcome
    
    This is the Guide.  You can close this TextViewer and then open it again later by right-clicking on the word Guide in any TextViewer.  You can also reopen this Guide by using the "Open Guide" button on the Xerblin controller widget.

    Right-clicking on a word that is also the name of a Xerblin Word will "Invoke" that word, causing it to perform its action.  You can tell if a word is a command because it will light up orange if you try right-clicking on it.

    You can also Invoke numbers by right-clicking on them.  Invoking a number puts it onto the stack.  Try it with these numbers:

        23      17

    Once you have some numbers on the stack, you can Invoke math commands to use the interface like a calculator. Try it now, put some numbers on the Stack (you can edit this text to include new numbers) then right-click on one of these words:  add  sub mul div

Invoke MathGuide for more.


Here is a summary of TextViewer Mouse commands (Invoke TextViewerGuide for more details.)

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


For a list of all the commands in the system Invoke WordList .


[more guides here]

Viewers..

Viewers allow you to interact with the system.

Stack..

Combining Words..

Finding Codesmiths to Create and Modify Your Words..

    ''',

    TextViewerGuide = '''TextViewerGuide

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

''',

    MathGuide = '''Math in Xerblin

First you must put some text on the stack that describes an equation.  For example, let's say you wanted to know what three times twenty-seven was.  Select the following text, but before you let go of the mouse button press the right button once too.  (Then let go of all the buttons.)

    3 * 27

You should see the text of that equation on the stack.  Now Invoke calc  just right-click on the word calc right here in the text.

You'll see that the text equation on the Stack has been replaced by the integer result 81.

    You can also use several mathematical functions and constants, such as sin() and pi.  Try:

 2 * pi * pow(23, 2)

 ...to find the area of a circle of radius 23.


Here are the available math functions you can use in your equations:

* / + -

exp(x)
    Return e**x. 

log(x[, base])
    Return the logarithm of x to the given base. If the base is not specified, return the natural logarithm of x (that is, the logarithm to base e).

log10(x)
    Return the base-10 logarithm of x. 

pow(x, y)
    Return x**y. 

sqrt(x)
    Return the square root of x. 

Trigonometric functions:

acos(x)
    Return the arc cosine of x, in radians. 

asin(x)
    Return the arc sine of x, in radians. 

atan(x)
    Return the arc tangent of x, in radians. 

atan2(y, x)
    Return atan(y / x), in radians. The result is between -pi and pi. The vector in the plane from the origin to point (x, y) makes this angle with the positive X axis. The point of atan2() is that the signs of both inputs are known to it, so it can compute the correct quadrant for the angle. For example, atan(1) and atan2(1, 1) are both pi/4, but atan2(-1, -1) is -3*pi/4. 

cos(x)
    Return the cosine of x radians. 

hypot(x, y)
    Return the Euclidean norm, sqrt(x*x + y*y). This is the length of the vector from the origin to point (x, y). 

sin(x)
    Return the sine of x radians. 

tan(x)
    Return the tangent of x radians. 

Angular conversion:

degrees(x)
    Converts angle x from radians to degrees. 

radians(x)
    Converts angle x from degrees to radians. 

Hyperbolic functions:

cosh(x)
    Return the hyperbolic cosine of x. 

sinh(x)
    Return the hyperbolic sine of x. 

tanh(x)
    Return the hyperbolic tangent of x. 

Also two mathematical constants:

pi
    The mathematical constant pi. 

e
    The mathematical constant e. 
''',

    WordList = '''WordList

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

    )


def InscribeDocumentationWords(interpreter, coords):
    '''
    This helper function takes the above Documentation dict and converts
    it into TextViewer objects in the interpreter's dictionary.
    It's only used in the main xerblin script.
    coords are a 4-tuple, the default (x, y, w, h) coords for the windows.
    (See setGeometry in lib/widgets/widgetwrapper.py.)
    '''
    TV = interpreter.dictionary.get('textviewer')

    for name, text in Documentation.iteritems():

        # Convert the string into a Text var word.
        t = Text(name, text)

        # Build a fake stack for TV.
        stack = [t, interpreter]

        # Make the TextViewer Object.
        TV.execute(stack)
        T = stack[0]

        # Set the name.
        T.name = name

        # Set the size and location of the Toplevel window.
        T.dictionary['setGeometry'].execute([coords])
        T.dictionary['hide'].execute([])

        # "Inscribe" the word.
        interpreter.dictionary[name] = T


class GuideWords(ExecutableWord):
    '''
    A helper word to let the startup script create these words at runtime.
    Basically this is a hard-coded string constant.
    '''

    word_source = '''

        * Stack = "show" StackViewer
        * new-list = meta meta pop swap push unmeta
        * new-text = texts self "" textviewer push drop
        * save = meta scratchpad swap push drop

          t = pop swap drop unmeta
          i & t Nop
        * restore = scratchpad dup i

        * drop-all = meta drop
        * open = self swap open

    ''' + ''.join(
    # For each of the Documentation TextViewers, replace it with a SeqWord
    # that shows the TextViewer.  This essentially makes the name of the
    # viewer open it.  To get the viewer you must Evoke the SeqWord and pick
    # out its trailing component (the TextViewer object.)
    ' * %s = "show" %s ' % (n, n)
    for n in Documentation
    )

    def execute(self, stack):
        stack.insert(0, self.word_source)


