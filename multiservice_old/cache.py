import sys
import memcache
from pymemcache.client import base
import pymysql

#memc = memcache.Client(['127.0.0.1:11211'], debug=1);
memc = base.Client(('localhost', 11211))
try:
    conn = pymysql.connect("172.18.0.14","cryptouser","123456","cryptodb" )
except pymysql.Error as e:
    print ("Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit(1)
finally:
    conn.close()
	 
latestslogs = memc.get('toplogs')

if not latestslogs:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM logs order by log_id DESC limit 10')
    rows = cursor.fetchall()
    memc.set('toplogs',rows,60)
    cursor.close()
    print ("Updated memcached with MySQL data")
else:
    print ("Loaded data from memcached")
    for row in latestslogs:
        print ("%s, %s" % (row[0], row[1]))