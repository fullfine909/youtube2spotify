from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs


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

    vdict = {
        'id':v['id'],
        'title':v['snippet']['title'],
        'channel':{'id':v['snippet']['channelId'],'name':v['snippet']['channelTitle']},
        'views':v['statistics']['viewCount'],
        'likes':v['statistics']['likeCount']}

    return vdict


def addVideoComments(vdict):
    vid = vdict["id"]
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
    vdict["comments"] = cjoined
    return vdict

def cfilter(c,th):
    if c.count(' - ') > th:
        return True
    else:
        return False

def getVideo(url):
    vid = getVideoID(url)
    vdict = getVideoInfo(vid)
    return addVideoComments(vdict)


yt = ytclient()

