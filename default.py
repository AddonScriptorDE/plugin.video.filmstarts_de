#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmcaddon,socket

socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
xbox = xbmc.getCondVisibility("System.Platform.xbox")
addon = xbmcaddon.Addon(id='plugin.video.filmstarts_de')
translation = addon.getLocalizedString

showAllTrailers=addon.getSetting("showAllTrailers")
forceViewMode=addon.getSetting("forceViewMode")
if forceViewMode=="true":
  forceViewMode=True
else:
  forceViewMode=False
viewMode=str(addon.getSetting("viewMode"))

def index():
        addDir('Trailer: '+translation(30008),'',"search",'')
        addDir('Trailer: '+translation(30001),'http://www.filmstarts.de/trailer/aktuell_im_kino.html?version=1',"showSortDirection",'')
        addDir('Trailer: '+translation(30002),'http://www.filmstarts.de/trailer/bald_im_kino.html?version=1',"showSortDirection",'')
        addDir('Filmstarts: Interviews','http://www.filmstarts.de/trailer/interviews/',"listVideosInterview",'')
        addDir('Filmstarts: Fünf Sterne','http://www.filmstarts.de/videos/shows/funf-sterne',"listVideosMagazin",'')
        addDir('Filmstarts: Fehlerteufel','http://www.filmstarts.de/videos/shows/filmstarts-fehlerteufel',"listVideosMagazin",'')
        addDir('Meine Lieblings-Filmszene','http://www.filmstarts.de/videos/shows/meine-lieblings-filmszene',"listVideosMagazin",'')
        addDir('Serien-Trailer','http://www.filmstarts.de/trailer/serien/',"listVideosTV",'')
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def showSortDirection(url):
        addDir(translation(30003),url.replace("?version=1","?sort_order=0&version=1"),"listVideosTrailer",'')
        addDir(translation(30004),url.replace("?version=1","?sort_order=1&version=1"),"listVideosTrailer",'')
        addDir(translation(30005),url.replace("?version=1","?sort_order=3&version=1"),"listVideosTrailer",'')
        addDir(translation(30006),url.replace("?version=1","?sort_order=2&version=1"),"listVideosTrailer",'')
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def listVideos(urlFull):
        content = getUrl(urlFull)
        currentPage=-1
        maxPage=-1
        try:
          match=re.compile('<span class="navcurrpage">(.+?)</span> / (.+?)</li><li class="navnextbtn">', re.DOTALL).findall(content)
          currentPage=int(match[0][0])
          maxPage=int(match[0][1])
        except:
          try:
            match=re.compile('<em class="current">(.+?)</em></li><li class="navcenterdata"><span class="(.+?)">(.+?)</span>', re.DOTALL).findall(content)
            currentPage=int(match[0][0])
            maxPage=int(match[0][2])
          except:
            pass
        if mode=="listVideosTrailer":
          match=re.compile('<img src=\'(.+?)\' alt="(.+?)" title="(.+?)" />\n</span>\n</div>\n<div class="contenzone">\n<div class="titlebar">\n<a class="link" href="(.+?)">\n<span class=\'bold\'>(.+?)</span>', re.DOTALL).findall(content)
          for thumb,temp1,temp2,url,title in match:
                if showAllTrailers=="true":
                  url=url[:url.find("/trailer/")]+"/trailers/"
                  addDir(title,'http://www.filmstarts.de' + url,"listTrailers",get_better_thumb(thumb))
                else:
                  addLink(title,'http://www.filmstarts.de' + url,"playVideo",get_better_thumb(thumb))
        elif mode=="listVideosMagazin":
          if currentPage==1:
            match=re.compile('<a href="(.+?)">\n<img src="(.+?)" alt="" />\n</a>\n</div>\n<div style="(.+?)">\n<h2 class="(.+?)" style="(.+?)"><b>(.+?)</b> (.+?)</h2><br />\n<span style="(.+?)" class="purehtml fs11">\n(.+?)<a class="btn" href="(.+?)"', re.DOTALL).findall(content)
            for temp0,thumb,temp1,temp2,temp3,temp4,title,temp5,temp6,url in match:
                  addLink(title,'http://www.filmstarts.de' + url,"playVideo",get_better_thumb(thumb))
          match=re.compile('<img src=\'(.+?)\' alt="(.+?)" title="(.+?)" />\n</span>\n</div>\n<div class="contenzone">\n<div class="titlebar">\n<a href=\'(.+?)\' class="link">\n<span class=\'bold\'><b>(.+?)</b> (.+?)</span>', re.DOTALL).findall(content)
          for thumb,temp1,temp2,url,temp3,title in match:
                addLink(title,'http://www.filmstarts.de' + url,"playVideo",get_better_thumb(thumb))
        elif mode=="listVideosInterview":
          match=re.compile('<img src=\'(.+?)\'(.+?)</span>\n</div>\n<div class="contenzone">\n<div class="titlebar">\n<a(.+?)href=\'(.+?)\'>\n<span class=\'bold\'>\n(.+?)\n</span>(.+?)\n</a>', re.DOTALL).findall(content)
          for thumb,temp1,temp2,url,title1,title2 in match:
                addLink(title1+title2,'http://www.filmstarts.de' + url,"playVideo",get_better_thumb(thumb))
        elif mode=="listVideosTV":
          spl=content.split('<div class="datablock vpadding10b">')
          for i in range(1,len(spl),1):
            entry=spl[i]
            match=re.compile("<a href='(.+?)'>", re.DOTALL).findall(entry)
            url=match[0]
            match=re.compile("<img src='(.+?)'", re.DOTALL).findall(entry)
            thumb=match[0]
            if entry.find("<span class='bold'>")>=0:
              match=re.compile("<span class='bold'>(.+?)</span>(.+?)<br />", re.DOTALL).findall(entry)
              title=match[0][0]+' '+match[0][1]
            else:
              match=re.compile("<a href='(.+?)'>\n(.+?)<br />", re.DOTALL).findall(entry)
              title=match[0][1]
            addLink(title,'http://www.filmstarts.de' + url,"playVideo",get_better_thumb(thumb))
        if currentPage<maxPage:
          urlNew=""
          if mode=="listVideosTrailer":
            sortNr=urlFull[urlFull.find('sort_order=')+11:]
            sortNr=sortNr[:sortNr.find('&')]
            urlNew=urlFull[:urlFull.find('?')]+"?page="+str(currentPage+1)+"&sort_order="+sortNr+"&version=1"
          elif urlFull.find('?page=')>=0 and (mode=="listVideosMagazin" or mode=="listVideosInterview" or mode=="listVideosTV"):
            match=re.compile('http://www.filmstarts.de/(.+?)?page=(.+?)', re.DOTALL).findall(urlFull)
            urlNew='http://www.filmstarts.de/'+match[0][0]+'page='+str(currentPage+1)
          elif urlFull.find('?page=')==-1 and (mode=="listVideosMagazin" or mode=="listVideosInterview" or mode=="listVideosTV"):
            urlNew=urlFull + "?page="+str(currentPage+1)
          addDir(translation(30007)+" ("+str(currentPage+1)+")",urlNew,mode,'')
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def listTrailers(url):
        content = getUrl(url)
        splMain=content.split('<div class="media_list_02')
        for i in range(1,len(splMain),1):
          entryMain = splMain[i]
          entryMain = entryMain[:entryMain.find('</div>')]
          spl=entryMain.split("<li>")
          for i in range(1,len(spl),1):
            entry=spl[i]
            match=re.compile("src='(.+?)'", re.DOTALL).findall(entry)
            thumb=match[0]
            match=re.compile("title='(.+?)'", re.DOTALL).findall(entry)
            title=match[0].replace(" DF", " - "+str(translation(30009))).replace(" OV", " - "+str(translation(30010)))
            title=cleanTitle(title)
            match=re.compile('href="(.+?)"', re.DOTALL).findall(entry)
            if len(match)>0:
              url="http://www.filmstarts.de"+match[0]
              addLink(title,url,'playVideo',thumb)
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def cleanTitle(title):
        title=title.replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("&#39;","'").replace("&quot;","\"").replace("&szlig;","ß").replace("&ndash;","-")
        title=title.replace("&#38;","&").replace("&#8230;","...").replace("&#8211;","-").replace("&#8220;","-").replace("&#8221;","-").replace("&#8217;","'")
        title=title.replace("&#196;","Ä").replace("&#220;","Ü").replace("&#214;","Ö").replace("&#228;","ä").replace("&#252;","ü").replace("&#246;","ö").replace("&#223;","ß").replace("&#176;","°").replace("&#233;","é").replace("&#224;","à")
        title=title.strip()
        return title

def search():
        keyboard = xbmc.Keyboard('', str(translation(30008)))
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
          search_string = keyboard.getText().replace(" ","+")
          content = getUrl("http://www.filmstarts.de/suche/1/?q="+search_string)
          spl=content.split('<tr><td style=" vertical-align:middle;">')
          for i in range(1,len(spl),1):
            entry=spl[i]
            match=re.compile("src='(.+?)'", re.DOTALL).findall(entry)
            thumb=match[0]
            match=re.compile("'>\n(.+?)</a>", re.DOTALL).findall(entry)
            title=match[0].replace("<b>","").replace("</b>","")
            title=cleanTitle(title)
            match=re.compile("href='(.+?)'", re.DOTALL).findall(entry)
            url="http://www.filmstarts.de"+match[0].replace(".html","/trailers/")
            addDir(title,url,'listTrailers',thumb)
          xbmcplugin.endOfDirectory(pluginhandle)
          if forceViewMode==True:
            xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def playVideo(url):
        content = getUrl(url)
        match1=re.compile('"cmedia" : (.+?),', re.DOTALL).findall(content)
        match2=re.compile("cmedia: '(.+?)'", re.DOTALL).findall(content)
        if len(match1)>0:
          media=match1[0]
        elif len(match2)>0:
          media=match2[0]
        match1=re.compile('"ref" : (.+?),', re.DOTALL).findall(content)
        match2=re.compile("ref: '(.+?)'", re.DOTALL).findall(content)
        if len(match1)>0:
          ref=match1[0]
        elif len(match2)>0:
          ref=match2[0]
        match1=re.compile('"typeRef" : "(.+?)"', re.DOTALL).findall(content)
        match2=re.compile("typeRef: '(.+?)'", re.DOTALL).findall(content)
        if len(match1)>0:
          typeRef=match1[0]
        elif len(match2)>0:
          typeRef=match2[0]
        content = getUrl('http://www.filmstarts.de/ws/AcVisiondataV4.ashx?media='+media+'&ref='+ref+'&typeref='+typeRef)
        finalUrl=""
        match1=re.compile('/nmedia/youtube:(.+?)"', re.DOTALL).findall(content)
        match2=re.compile('hd_path="(.+?)"', re.DOTALL).findall(content)
        if len(match1)>0:
          finalUrl=getYoutubeUrl(match1[0])
        elif len(match2)>0:
          finalUrl=match2[0]
        if finalUrl!="":
          listitem = xbmcgui.ListItem(path=finalUrl)
          return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def getYoutubeUrl(id):
          if xbox==True:
            url = "plugin://video/YouTube/?path=/root/video&action=play_video&videoid=" + id
          else:
            url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=" + id
          return url

def get_better_thumb(thumb_url):
          # This image provider does dynamic image modificiation
          # c -> resize, b -> border, o -> overlay
          # by removing this parameters we get the original/native thumb
          thumb_url = '/'.join([
              p for p in thumb_url.split('/')
              if not p[0:2] in ('c_', 'b_', 'o_')
          ])
          return thumb_url

def getUrl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:18.0) Gecko/20100101 Firefox/18.0')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

def parameters_string_to_dict(parameters):
        ''' Convert parameters encoded in a URL to a dict. '''
        paramDict = {}
        if parameters:
            paramPairs = parameters[1:].split("&")
            for paramsPair in paramPairs:
                paramSplits = paramsPair.split('=')
                if (len(paramSplits)) == 2:
                    paramDict[paramSplits[0]] = paramSplits[1]
        return paramDict

def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
         
params=parameters_string_to_dict(sys.argv[2])
mode=params.get('mode')
url=params.get('url')
if type(url)==type(str()):
  url=urllib.unquote_plus(url)

if mode=="playVideo":
    playVideo(url)
elif mode=="showSortDirection":
    showSortDirection(url)
elif mode=="listTrailers":
    listTrailers(url)
elif mode=="listVideosMagazin" or mode=="listVideosInterview" or mode=="listVideosTV" or mode=="listVideosTrailer":
    listVideos(url)
elif mode=="search":
    search()
else:
    index()