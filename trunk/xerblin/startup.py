# This is the default start up "script" for Xerblin.  The xerblin script
# imports the startup_script string below and calls the interpret()
# method of the new Xerblin Object with it as the argument.

# If you're looking for the place where the StackViewer and the Close
# Button are created, that's in the bin/xerblin script.

startup_script = (

    # Create a default list to put texts.
    ''' meta "texts" constant self Inscribe drop '''

    # Create a list as a scratchpad.
    ''' meta "scratchpad" constant self Inscribe drop '''

    # Set the StackViewer in the corner.
    ''' 480 364 0 0 meta''' # some coordinates. Now call setGeometry.
    ''' self "StackViewer" lookup "setGeometry" lookup InvokeWord'''
    

    # Hide the TextViewerGuide.
    ''' "hide" TextViewerGuide '''

    # Create the words in the built-in word "GuideWords".
    '''self GuideWords makewords drop '''

'''
'''
)
##
##self GuideWords makewords drop
##'''
##)
