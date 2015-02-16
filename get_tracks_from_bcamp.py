
import urllib2
import urllib
import json
import re
import requests
from bs4 import BeautifulSoup



api_key = '1398647563774172|9Olb3-J0Afb6dfwHWoR3Y2FccCk'

def get_tracks_from_bcamp(bcamp_url):
    web = urllib.urlopen(bcamp_url)
    soup = BeautifulSoup(web.read(), 'lxml')
    data  = soup.find_all("script")
    data = [str(s) for s in data]
    
    script = [s for s in data if s.find('mp3-128') > 0]
    
    mp3_regex = '\B"http:\/\/popplers5\.bandcamp\.com\/download\/track\?[-a-z-A-Z0-9+&@#/%?=~_|$!:,.;]*'
    mp3_regex_compiler = re.compile(mp3_regex, re.U)
    mp3s = mp3_regex_compiler.findall(script[0])
    mp3s = [s[1:] for s in mp3s]
    
    track_titles_regex = 'title\":\"[A-Za-z0-9- \/\'\\&-;]+'
    title_regex_compiler = re.compile(track_titles_regex, re.U)
    titles = title_regex_compiler.findall(script[0])
    titles = [s[8:] for s in titles]
    titles = titles[1:]
    
    tracks = dict(zip(titles,mp3s))
    
    artist_regex = 'artist: "[A-Za-z0-9\/ ]+'
    artist_regex_compiler = re.compile(artist_regex,re.U)
    artist = artist_regex_compiler.findall(script[0])
    artist = artist[0][9:]
    
    return artist, tracks


def get_event_text_fb_from_id(id):
    baseurl = "https://graph.facebook.com/v2.2"
    payload = {'id': id,
               'access_token': api_key,
               'fields': 'name,cover,description,start_time,venue'}
    r = requests.get(baseurl, params=payload)
    r = r.json()
    return r


def find_bcamp_url(text):
    bcamp_regex = 'https?:\/\/[A-za-z0-9-]+\.bandcamp\.com\/?[-a-z-A-Z]*'
    bcamp_compiler = re.compile(bcamp_regex, re.U)
    bcamp = bcamp_compiler.findall(text)
    return bcamp



def get_fb_event_text_from_link(url):
    m = re.compile('https?://www.facebook.com/events/[0-9]+([\/\?]|[\/\?])?.*')
    if m.match(url):
        regex_compiler = re.compile('[0-9]+')
        fbid = regex_compiler.search(url).group()
        
        baseurl = "https://graph.facebook.com/v2.2"
        payload = {'id': fbid,
                   'access_token': api_key,
                   'fields': 'name,cover,description,start_time,venue'}
        r = requests.get(baseurl, params=payload)
        r = r.json()
        return r['description']
    else:
        print "not a facebook event url"


def __get_tracks_from_fb_event__(fb_url):
    #print url
    text = get_fb_event_text_from_link(fb_url)
    #print text
    bcamp_urls = find_bcamp_url(text)
    #print bcamp_urls
    tracks = [get_tracks_from_bcamp(i) for i in bcamp_urls]
    return tracks

# fb_url = 'https://www.facebook.com/events/805228439542222/'

tracks = __get_tracks_from_fb_event__('https://www.facebook.com/events/760584384034988/')

print tracks






