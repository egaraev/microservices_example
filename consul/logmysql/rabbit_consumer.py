import flask, os, socket, subprocess, requests, json, consul, sys
from flask import Flask, request, jsonify
import time
import json
import MySQLdb
import pika
import datetime

time.sleep(40) # seconds


SELF_HOSTNAME = str(socket.gethostname())
SELF_IP = socket.gethostbyname(SELF_HOSTNAME)


# fetch consul's ip, so that we can talk to it.
CONSUL_ALIAS = 'consul'
CONSUL_PORT = '8500'
CONSUL_IP = subprocess.check_output(['getent', 'hosts', CONSUL_ALIAS]).decode().split()[0]



# create consul instance (not agent, just python instance)
c = consul.Consul(host=CONSUL_IP, port=CONSUL_PORT)

# get mongodb IP
keyindex, mysqldb_ip_bytes = c.kv.get('mysqldb')
mysqldb_ip = mysqldb_ip_bytes['Value'].decode()

keyindex, rabbitmq_ip_bytes = c.kv.get('rabbitmq')
rabbitmq_ip = rabbitmq_ip_bytes['Value'].decode()
rabbitmq_ip_only = rabbitmq_ip.split(":", 1)
rabbitmq_ip_only=rabbitmq_ip_only[0]




credentials = pika.PlainCredentials('user1', 'pass1')
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_ip_only,5672,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue='logging')

def callback(ch, method, properties, body):
    now = datetime.datetime.now()
    currenttime = now.strftime("%Y-%m-%d %H:%M")
    print(" [x] Received %r" % body)
    try:
        db = MySQLdb.connect("mysqldb", "cryptouser", "123456", "cryptodb")
        cursor = db.cursor()
        cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, body))
        db.commit()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        db.close()

channel.basic_consume('logging', callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()