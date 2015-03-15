**This project has been subsumed into the Pigeon Computer project.**

Please visit:
  * http://thinkpigeon.blogspot.com/
  * https://github.com/PhoenixBureau/PigeonComputer


---


Xerblin is a completely general Human-Computer interface.

It provides a single metaphor for interacting with computers that's simple enough to teach to children yet provides facilities that are useful to advanced programmers.  It can integrate all levels of software from the Desktop to assembly language.

There are three basic user-facing elements to a Xerblin system.

  * Stack - a place to put objects for user manipulation.  This is similar to a Clipboard but it can hold more than one item at a time. Commands operate on the items on the Stack.
  * Dictionary - a place to keep commands. Any command that is inscribed in the Dictionary can be run from the user interface.
  * Interpreter - A very simple command interpreter that takes care of running commands with the Stack.

In addition to the above three UI elements there are discrete commands that provide the basic functionality of the system and that can be composed into more complex commands. They live in the Dictionary and act upon the Stack.  They can be composed into compound commands using four primal relations:

  * Sequence - do one thing after another.
  * Loop - do something over again.
  * Branch - do one thing or another.
  * Parallel - do two or more things that don't conflict.

Using the above four relations compound commands can be composed to perform more involved tasks using the built-in or user-provided "primitives" and other compound commands.

Composition can be done by program, by command line, in the GUI using the mouse and keyboard, or by means of parsing languages.

With a rich set of basic commands and the four kinds of compound commands you have a completely general computer interface that allows for customization and flexibility and can be easily understood and mastered by the average user.

The proof-of-concept demo version of Xerblin is written in Python and is available for download. It currently contains the Xerblin core and a couple of scripts that demonstrate interaction and persistence.