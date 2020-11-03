
import mysql.connector
import pandas as pd
import random
import string


db = mysql.connector.connect(
    host="mydb1.cke3tvcjf0an.eu-west-1.rds.amazonaws.com",
    user="admin",
    passwd="mydb1mydb1",
    database="firstdb"
)

c = db.cursor()
   
# mysql -h mydb1.cke3tvcjf0an.eu-west-1.rds.amazonaws.com -P 3306 -u admin -p



def showTables(c):
    q = "SHOW TABLES;"
    c.execute(q)
    r = c.fetchall()
    for t in r:
        print(t)

def resetdb():
    try:
        q = "DROP DATABASE firstdb"
        c.execute(q)
        q = "CREATE DATABASE firstdb"
        c.execute(q)
        connectdb()
        initdb()
        print('database reseted')
    except:
        connectdb()
        initdb()
        print('database already dropped')

def connectdb():
    q = "use firstdb"
    c.execute(q)
    print('connected')
    
def initdb():
    # read excel
    df = pd.read_excel('FlaskWebProject1/tables.ods',0, header=None,  engine="odf")

    # main tables 
    idx = _ods2pd(29,df)
    for i in idx:
        row = list(df.iloc[i])
        cleanrow = _nanremover(row)
        mainTable(cleanrow)

    # relational tables
    idx = _ods2pd(30,df)
    for i in idx:
        row = list(df.iloc[i])
        cleanrow = _nanremover(row)
        relationTable(cleanrow)

    # load user
    q = 'INSERT INTO product (id,name) VALUES (%s,%s)'
    c.execute(q, ('dtd9srb32n2qbzn2c35j4iutg','hate'))
    q = 'INSERT INTO user (id,name) VALUES (%s,%s)'
    c.execute(q, ('dtd9srb32n2qbzn2c35j4iutg','hate'))
    db.commit()

def createTable(q):
    try:
        c.execute(q)
        t = q.split(' ')[2]
        print("Table {} created successfully".format(t))
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

def mainTable(row):
    tname = row.pop(0)
    values = ', '.join(row)
    q = "CREATE TABLE {} ({})".format(tname,values)
    createTable(q)

def relationTable(row):
    table = row[0]
    col1 = row[1]
    col2 = row[2]
    col3 = row[3]
    t1 = col1[:-3]
    t2 = col2[:-3]
    q = "CREATE TABLE {} ({} VARCHAR(22), {} VARCHAR(22), {} FOREIGN KEY({}) REFERENCES {}(id), FOREIGN KEY({}) REFERENCES {}(id), PRIMARY KEY({},{}))".format(table,col1,col2,col3,col1,t1,col2,t2,col1,col2)
    createTable(q)

def insertMany(table,values):
    insertRecord(table,values,1)

def insertOne(table,values):
    insertRecord(table,values,0)

def insertRecord(table,values,m):
    if values:
        try:
            c.execute('describe '+table)
            res = c.fetchall()
            names = [x[0] for x in res]
            margin = len(values) if m == 0 else len(values[0])
            names = names[0:margin]
            qnames = ', '.join(names)
            qvalues = ','.join(['%s' for i in range(len(names))])

            q = "INSERT IGNORE INTO {} ({}) VALUES ({})".format(table,qnames,qvalues)

            # insert one vs many
            if m == 0:
                c.execute(q, values)
            else:
                c.executemany(q, list(set(values)) )
            db.commit()
            print(c.rowcount, "was inserted in {}.".format(table))
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        except:
            print('Take care!')
    else:
        print('Nothing to insert')

def checkProduct(table,pname):

    N = len(pname)
    pcheck = '"'+'","'.join(pname)+'"'
    pid = _randArray(N)

    q = "SELECT * FROM {} WHERE NAME IN ({})".format(table,pcheck)
    c.execute(q)
    rproduct = c.fetchall()

    new_p = []
    all_p = []


    for i in range(N):
        check = list(filter(lambda x : pname[i] in x,  rproduct))
        if check:
            # label found
            l = (check[0][0],pname[i])
            all_p.append(l)
        else:
            l = (pid[i],pname[i])
            all_p.append(l)
            new_p.append(l)

    return [all_p,new_p]

def checkVideo(vid):
    q = "SELECT id,name,hspt FROM video WHERE id = '{}'".format(vid)
    c.execute(q)
    rvideo = c.fetchall()
    if rvideo:

        q = "SELECT t.id, t.name, t.artist_display, a.name, t.href, t.hmp3, a.himg, t.popularity, t.bpm, t.duration, l.name "\
            "FROM track t "\
            "INNER JOIN album a on t.album_id = a.id "\
            "INNER JOIN label l on a.label_id = l.id "\
            "INNER JOIN track2video tv on t.id = tv.track_id "\
            "INNER JOIN video v on tv.video_id = v.id "\
            "WHERE v.id = '{}' "\
            "ORDER BY tv.pos".format(rvideo[0][0])

        c.execute(q)
        rsongs = c.fetchall()

        songs = []
        for x in rsongs:
            songs.append({
                'id':x[0],
                'name':x[1],
                'artist':x[2],
                'album':x[3],
                'href':x[4],
                'hmp3':x[5],
                'himg':x[6],
                'pop':x[7],
                'bpm':x[8],
                'dur':x[9],
                'label':x[10]})


        v = {
            'id':rvideo[0][0],
            'name':rvideo[0][1],
            'hspt':rvideo[0][2]}
        return [1,songs,v]
    else:
        return [0,0,0]


def addParameters(c,table,param):
    q = "ALTER TABLE {} ADD {} ;"

def _nanremover(arr):
    return [x for x in arr if str(x) != 'nan']

def _ods2pd(idx,df):
    ind = list(df.iloc[idx-1])[0].split(' ')   # cell in excel with order to create tables
    arr = [int(i) for i in ind] 
    return [x-1 for x in arr]

def _randArray(n):
    ra = []
    for i in range(n):
        ra.append(_randStr())
    return ra

def _randStr():
    chars = string.ascii_letters + string.digits 
    return ''.join(random.choice(chars) for _ in range(22))

# resetdb()
# connectdb()
# initdb()
# showTables(c)
# addParameters(c,'track','danceability FLOAT, energy FLOAT, loudness FLOAT, tempo FLOAT')

