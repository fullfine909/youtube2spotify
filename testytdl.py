import youtube_dl

url = 'https://www.youtube.com/watch?v=G9SEKxkcvK0&ab_channel=PrimaveraSound'
ydl = youtube_dl.YoutubeDL({})
with ydl:
    video = ydl.extract_info(url, download=False)


print('ey')