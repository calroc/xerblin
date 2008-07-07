from xerblin import ExecutableWord
from xerblin.util.stackcheckers import StackLen
from math import *

class calc(StackLen(1), ExecutableWord):
    '''
    Calculate the expression on TOS.

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
    '''

    def execute(self, stack):
        expression = stack[0]
        result = eval(expression)
        stack[0] = result
