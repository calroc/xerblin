# This is the default start up "script" for Xerblin.  The xerblin script
# imports the startup_script string below and calls the interpret()
# method of the new Xerblin Object with it as the argument.

# If you're looking for the place where the StackViewer and the Close
# Button are created, that's in the bin/xerblin script.

startup_script = (
    # First, create a TextViewer on the built-in word "Guide".
    # (It's in xerblin/lib/guide.py.)
    '''self Guide textviewer '''

    # Name it "GuideViewer" and inscribe it into the Dictionary.
    '''"GuideViewer" setname
        self Inscribe drop '''
    
    # Create a TextViewer for the TextViewerGuide.
    '''
    self TVGuide textviewer
    "TextViewerGuide" setname
    self Inscribe drop
    "hide" TextViewerGuide
    '''

    # Create the words in the built-in word "GuideWords".
    '''self GuideWords makewords drop '''

'''
'''
)
##
##self GuideWords makewords drop
##'''
##)
