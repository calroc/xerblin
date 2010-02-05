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


This is the default start up "script" for Xerblin.  The xerblin script
imports the startup_script string below and calls the interpret()
method of the new Xerblin Object with it as the argument.

If you're looking for the place where the StackViewer and the Close
Button are created, that's in the xerblin.util.fresh module.
'''
from xerblin.documentation import docs


startup_script = (

    # Create a default list to put texts.
    ''' meta "texts" constant self Inscribe drop '''

    # Create a list as a scratchpad.
    ''' meta "scratchpad" constant self Inscribe drop '''

    # Set the StackViewer in the corner.
    ''' 384 237 0 0 meta''' # some coordinates. Now call setGeometry.
    ''' self "StackViewer" lookup "setGeometry" lookup InvokeWord'''
    

    # Show the first Guide and set it's x coordinate.
    ''' "show" Guide '''
    ''' 880 800 0 273 meta '''
    ''' self "Guide" lookup "setGeometry" lookup InvokeWord '''
)


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
    * Words = self dup words textviewer drop

    ''' + ''.join(

    # For each of the Documentation TextViewers, replace it with a
    # SeqWord that shows the textviewer.  This essentially makes the name
    # of the viewer open it.  To get the viewer you must Evoke the
    # SeqWord and pick out its trailing component (the textviewer
    # object.)

    ' * %s = "show" %s ' % (n, n)
    for n in docs
)
