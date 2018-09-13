# Deezer Python API

import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from requests import get

def youtube(q):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q)
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response.read())
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        return 'https://www.youtube.com' + vid['href']

def deezer(q, what=None, limit=None, index="0", output="json"):
    params = dict(q=q,index=index,limit=limit,output=output)
    response = get(url="https://api.deezer.com/search/{}".format(what + "/" if what else ""), params=params)
    result = response.json()
    
    return result