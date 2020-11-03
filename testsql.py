from FlaskWebProject1.apiutil import link2data
from FlaskWebProject1.songutils import openRes, addSongs
from FlaskWebProject1.sqlutils import resetdb

url = 'https://www.youtube.com/watch?v=4utKO75DtBE&t=2099s&ab_channel=BE-AT.TV'

#resetdb()


#[x,v] = openRes()
[x,v] = link2data(url)


print('yey')

