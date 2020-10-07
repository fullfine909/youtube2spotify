from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
import youtube_dl



def ytclient():
    api_key = 'AIzaSyBDxBo5zmRC8gNIdgziB1elmDVmlBzVozY'
    return build('youtube','v3',developerKey=api_key)

def getVideoID(url):
    url_data = urlparse(url)
    query = parse_qs(url_data.query)
    return query["v"][0]


def getVideoInfo(arr_id):
    request = yt.videos().list( # pylint: disable=maybe-no-member
        part="snippet,statistics",
        id=arr_id
    )
    response = request.execute()
    v = response['items'][0]

    try:
        likes = v['statistics']['likeCount']
    except:
        likes = 0

    vdict = {
        'id':v['id'],
        'title':v['snippet']['title'],
        'channel':{'id':v['snippet']['channelId'],'name':v['snippet']['channelTitle']},
        'views':v['statistics']['viewCount'],
        'likes':likes}

    return vdict

def addMusicInfo(url):
    with ydl:
        video = ydl.extract_info(url, download=False)

    minfo = {
        'name':video['track'],
        'artist':video['artist']

    }
    
def addVideoComments(vid):
    request = yt.commentThreads().list( # pylint: disable=maybe-no-member
        part="snippet",
        maxResults=50,
        order="relevance",
        videoId=vid
    )
    res =  request.execute()
    comments = res['items']
    ctext = [x['snippet']['topLevelComment']['snippet']['textOriginal'] for x in comments]

    th = 5
    cfinal = list(filter( lambda l: cfilter(l,th),ctext))
    cjoined = '\r\n'.join(cfinal)
    return cjoined

def cfilter(c,th):
    if c.count('\n') > th:
        return True
    else:
        return False

def getVideo(url):
    vid = getVideoID(url)
    vdict = getVideoInfo(vid)
    #vdict["music"] = addMusicInfo(url)
    vdict["comments"] = addVideoComments(vid)
    return vdict


yt = ytclient()
ydl = youtube_dl.YoutubeDL({})
