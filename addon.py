import sys
import xbmc, xbmcgui, xbmcplugin
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup as bs

def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict.'''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split("=")
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

def addDirectoryItem(name, isFolder=True, parameters={}, playable=False):
    ''' Add a list item to the XBMC UI.'''
    li = xbmcgui.ListItem(name)

    if playable == True:
        li.setProperty("IsPlayable", "True")

    url = sys.argv[0] + "?" + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=isFolder)

def show_root_menu():
    ''' Show the plugin's root menu.'''
    addDirectoryItem(name="Wednesday", parameters={ "name": "WED", "level": "1" }, isFolder=True)
    addDirectoryItem(name="Thursday", parameters={ "name": "THURS", "level": "1" }, isFolder=True)
    addDirectoryItem(name="Friday", parameters={ "name": "FRI", "level": "1" }, isFolder=True)
    xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)

def show_video_list(url):
    ''' Scrape the agenda page and display all the videos.'''
    page = urllib2.urlopen(url)
    soup = bs(page)

    for session in soup.findAll("td","session"):
        if session.find("p","bottomAligned") is not None:
            fullTitle = "%s - %s" % (session.find("div","title").a.string.encode("utf-8"), session.find("div","speaker").a.string.encode("utf-8"))
            addDirectoryItem(name=fullTitle,isFolder=False,parameters={"videoUrl": "http://ndcoslo.oktaset.com" + session.find("p","bottomAligned").a["href"], "level": "2"},playable=True)

    xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)

def play_video(url):
    ''' Scrape the session page and grab the vimeo video ID.'''
    page = urllib2.urlopen(urllib.unquote(url))
    soup = bs(page)
    vimeoID = soup.find("div","links").a["href"].split("/")[-1]

    vimeoPlayer = "plugin://plugin.video.vimeo/?action=play_video&videoid=" +  vimeoID

    listItem = xbmcgui.ListItem(path=vimeoPlayer)

    return xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)

def main():
    params = parameters_string_to_dict(sys.argv[2])
    name = params.get("name")
    level = params.get("level")

    if level is None:
        show_root_menu()
    elif level == "1":
        if name == "WED":
            show_video_list(url="http://ndcoslo.oktaset.com/Agenda/wednesday")
        elif name == "THURS":
            show_video_list(url="http://ndcoslo.oktaset.com/Agenda/thursday")
        elif name == "FRI":
            show_video_list(url="http://ndcoslo.oktaset.com/Agenda/friday")
    elif level == "2":
        play_video(params.get("videoUrl"))

if __name__ == "__main__":
    main()