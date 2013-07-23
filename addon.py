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
    addDirectoryItem(name="2012", parameters={ "year": "2012", "level": "1" }, isFolder=True)
    addDirectoryItem(name="2013", parameters={ "year": "2013", "level": "1" }, isFolder=True)
    xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)

def show_day_list(year):
    ''' Show the day list.'''
    addDirectoryItem(name="Wednesday", parameters={ "day": "WED", "year": year, "level": "2" }, isFolder=True)
    addDirectoryItem(name="Thursday", parameters={ "day": "THURS", "year": year, "level": "2" }, isFolder=True)
    addDirectoryItem(name="Friday", parameters={ "day": "FRI", "year": year, "level": "2" }, isFolder=True)
    xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)

def show_video_list(year, day):
    ''' Scrape the agenda page and display all the videos.'''
    baseUrl = get_base_video_url(year, day)
    agendaComponent = get_agenda_url_component(year, day)
    pageUrl = baseUrl + agendaComponent
    page = urllib2.urlopen(pageUrl)
    soup = bs(page)

    for session in soup.findAll("td","session"):
        if session.find("p","bottomAligned") is not None:
            fullTitle = "%s - %s" % (session.find("div","title").a.string.encode("utf-8"), session.find("div","speaker").a.string.encode("utf-8"))
            addDirectoryItem(name=fullTitle,isFolder=False,parameters={"videoUrl": baseUrl + session.find("p","bottomAligned").a["href"], "level": "3"},playable=True)

    xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)

def get_base_video_url(year, day):
    if year == "2012":
        return "http://ndc2012.oktaset.com"
    else:
        return "http://ndcoslo.oktaset.com"

def get_agenda_url_component(year, day):
    if day == "WED":
        return "/Agenda/wednesday"
    elif day == "THURS":
        return "/Agenda/thursday"
    elif day == "FRI":
        return "/Agenda/friday"

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
    day = params.get("day")
    level = params.get("level")
    year = params.get("year")

    if level is None:
        show_root_menu()
    elif level == "1":
        show_day_list(year)
    elif level == "2":
        show_video_list(year, day)
    elif level == "3":
        play_video(params.get("videoUrl"))

if __name__ == "__main__":
    main()