import requests
import json

url = "https://www.youtube.com/watch?v=k5nOPltHgZI&ab_channel=UnitedWeStreamMadrid"
page = requests.get(url).text

start = 'metadataRowRenderer'
sidx = page.find(start)-2

finish = 'collapsedItemCount'
fidx = page.find(finish)-3

text = '['+page[sidx:fidx]+']'
text_json = json.loads(text)

s = {}
songs = []
for x in text_json:
    keys = list(x['metadataRowRenderer']['contents'][0].keys())[0]
    title = x['metadataRowRenderer']['title']['simpleText']

    if title == 'Canción':
        songs.append(s)
        s = {}

    if keys == 'runs':
        value = x['metadataRowRenderer']['contents'][0]['runs'][0]['text']
    elif keys == 'simpleText':
        value = x['metadataRowRenderer']['contents'][0]['simpleText']

    s[title]=value

songs.append(s)
songs.pop(0)


print('ye')