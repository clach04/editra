#!/usr/bin/env python
###############################################################################
# Name: Editra.pyw                                                            #
# Purpose: Editra's main launch script                                        #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################


"""
Main launch script for the Editor. It first tries to look for Editra on the
local path and if it is not there it tries to import the Main method
from where Editra would be installed if it was installed using distutils

@summary: Editra's main launch script for Windows

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id: Editra.pyw 63538 2010-02-23 03:39:03Z CJP $"
__revision__ = "$Revision: 63538 $"

#--------------------------------------------------------------------------#
# Dependencies
import ctypes
import sys
import os

try:
    import src as esrc
    IS_LOCAL = True
except ImportError:
    try:
        import Editra as esrc
        IS_LOCAL = False
    except ImportError, msg:
        print "There was an error while tring to import Editra"
        print ("Make sure that Editra is on your PYTHONPATH and that "
               "you have wxPython installed.")
        print "ERROR MSG: "
        print str(msg)
        os._exit(1)

#--------------------------------------------------------------------------#
# There are currently some necessary hacks for launching editra from this
# script that will hopefully be removed in the not so distance future once
# the plugin managers meta registry is redesigned.

def main():
    # Set icon in taskbar under Microsoft Windows to match app icon
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('dummy.string.content.does.not.matter')  # see https://stackoverflow.com/a/1552105/674475

    # The initial import above is necessary to get the path of where
    # Editra is installed so that the src package can be put on the path.
    # If the src module is not on the path the plugins are unable to import
    # things from inside editras namespace properly. It also causes problems
    # with recongnizing plugins in Extension registry of the Plugins metaclass.
    SRC_DIR = os.path.dirname(esrc.__file__)
    if not IS_LOCAL:
        SRC_DIR = os.path.join(SRC_DIR, 'src')

    # Cleanup any of Editras modules that are already present before
    # importing Editra again so that the modules are imported with the
    # correct signature (i.e ed_theme vs src.ed_theme). As the plugin
    # manager currently registers the class objects metadata by using
    # the classes module signature for identification.
    if not IS_LOCAL:
        torem = [ key for key in sys.modules.keys()
                  if key.startswith('Editra') ]
        for key in torem:
            del sys.modules[key]
    else:
        if 'src' in sys.modules:
            del sys.modules['src']

    sys.path.insert(0, SRC_DIR)
    import Editra
    Editra.Main()


if __name__ == '__main__':
    main()
