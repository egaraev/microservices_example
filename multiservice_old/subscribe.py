import pika
import time
credentials = pika.PlainCredentials('user1', 'pass1')
connection = pika.BlockingConnection(pika.ConnectionParameters('172.18.0.10',5672,'/',credentials))
channel = connection.channel()

channel.queue_declare(queue='logging')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume('logging', callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
	
