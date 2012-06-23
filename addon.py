# Step 1 - load in xbmc core support and setup the environment
import xbmcplugin
import xbmcgui
import sys
from resources.lib.ndc import *

# magic; id of this plugin's instance - cast to integer
thisPlugin = int(sys.argv[1])

# Step 2 - create the support functions (or classes)
def createListing():
    """
    Creates a listing that XBMC can display as a directorylisting
    @return list
    """
    listing = []
    
    listing.append('By Category')
    listing.append('By Day')
    listing.append('By Speaker')
    
    return listing

def sendToXbmc(listing):
    """
    Sends a listing to XBMC for display as a directory listing
    Plugins always result in a listing
    @param list listing
    @return void
    """

    #access global plugin id
    global thisPlugin

    # send each item to xbmc
    for item in listing:
        listItem = xbmcgui.ListItem(item)
        xbmcplugin.addDirectoryItem(thisPlugin,'',listItem)

    # tell xbmc we have finished creating the directory listing
    xbmcplugin.endOfDirectory(thisPlugin)

# Step 3 - run the program
sendToXbmc(createListing())