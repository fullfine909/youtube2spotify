
import MySQLdb
import pandas as pd
import openpyxl
import random
import string

db = MySQLdb.connect(
    host="mydb1.cke3tvcjf0an.eu-west-1.rds.amazonaws.com",
    user="admin",
    passwd="mydb1mydb1",
    database="firstdb"
)

c = db.cursor()
   


def showTables(c):
    q = "SHOW TABLES;"
    c.execute(q)
    r = c.fetchall()
    for t in r:
        print(t)

def resetdb(c):
    try:
        q = "DROP DATABASE firstdb"
        c.execute(q)
        q = "CREATE DATABASE firstdb"
        c.execute(q)
        print('database reseted')
    except:
        print('database already dropped')
    finally:
        connectdb(c)

def connectdb(c):
    q = "use firstdb"
    c.execute(q)
    print('connected')
    
def initdb(c):
    # read excel
    df = pd.read_excel('tables.ods',0, header=None)

    # main tables 
    ind = list(df.iloc[28])[0].split(' ')   # cell in excel with order to create tables
    tindex = _cindex(ind)


    for i in tindex:
        row = list(df.iloc[i])
        cleanrow = _nanremover(row)
        mainTable(c,cleanrow)

    # relational tables
    ind = list(df.iloc[29])[0].split(' ')
    tindex = _cindex(ind)

    for i in tindex:
        row = list(df.iloc[i])
        cleanrow = _nanremover(row)
        relationTable(c,cleanrow)

def createTable(c,q):
    try:
        c.execute(q)
        t = q.split(' ')[2]
        print("Table {} created successfully".format(t))
    except MySQLdb.Error as err:
        print("Something went wrong: {}".format(err))

def mainTable(c,row):
    tname = row.pop(0)
    values = ', '.join(row)
    q = "CREATE TABLE {} ({})".format(tname,values)
    createTable(c,q)

def relationTable(c,row):
    table = row[0]
    col1 = row[1]
    col2 = row[2]
    t1 = row[3]
    t2 = row[4]
    q = "CREATE TABLE {} ({} VARCHAR(22), {} VARCHAR(22), FOREIGN KEY({}) REFERENCES {}(id), FOREIGN KEY({}) REFERENCES {}(id), PRIMARY KEY({},{}))".format(table,col1,col2,col1,t1,col2,t2,col1,col2)
    createTable(c,q)

def insertMany(table,names,values):
    insertRecord(table,names,values,1)

def insertOne(table,names,values):
    insertRecord(table,names,values,0)

def insertRecord(table,names,values,m):
    q = "INSERT IGNORE INTO {} ({}) VALUES (%s, %s)".format(table,names)
    try:
        # insert one vs many
        if m == 0:
            c.execute(q, values)
        else:
            c.executemany(q, list(set(values)) )
        db.commit()
        print(c.rowcount, "was inserted in {}.".format(table))
    except MySQLdb.Error as err:
        print("Something went wrong: {}".format(err))

def addParameters(c,table,param):
    q = "ALTER TABLE {} ADD {} ;"


def _nanremover(arr):
    return [x for x in arr if str(x) != 'nan']

def _cindex(arr):
    arr = [int(i) for i in arr] 
    return [x-1 for x in arr]

def _randStr():
    chars = string.ascii_letters + string.digits 
    return ''.join(random.choice(chars) for _ in range(22))

# resetdb(c)
# initdb(c)
# connectdb(c)
# showTables(c)
# addParameters(c,'track','danceability FLOAT, energy FLOAT, loudness FLOAT, tempo FLOAT')