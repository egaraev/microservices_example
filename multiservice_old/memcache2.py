from pymemcache.client import base
import pymysql
import memcache

memc  = memcache.Client(['127.0.0.1:11211'], debug=1);

result = memc.get('toplogs')
#print (result)

def query_db(result):
    db_connection = pymysql.connect("172.18.0.14","cryptouser","123456","cryptodb" )
    c = db_connection.cursor()
    try:
        c.execute('SELECT date, log_entry FROM logs order by log_id DESC limit 10')
        data = c.fetchall()
        db_connection.close()
    except:
        data = 'invalid'
    return data

if result is None:
    print("got a miss, need to get the data from db")
    result = query_db(result)
    if result == 'invalid':
        print("requested data does not exist in db")
    else:
        print("returning data to client from db")
        for row in result:
            print ("%s, %s" % (row[0], row[1]))
        print("setting the data to memcache")
        memc.set('toplogs', result, 60)

else:
    print("got the data directly from memcache")
    for row in result:      
            print ("%s, %s" % (str(row[0]), str(row[1])))


