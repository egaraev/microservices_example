import pika
#Create a new instance of the Connection object
credentials = pika.PlainCredentials('user1', 'pass1')
connection = pika.BlockingConnection(pika.ConnectionParameters('172.18.0.10',5672,'/',credentials))
#Create a new channel with the next available channel number or pass in a channel number to use
channel = connection.channel()
#Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can specify various properties that control the durability of the queue and its contents, and the level of sharing for the queue.
channel.queue_declare(queue='logging')
message='2 - We already have 0.5746 BTC-DCR on our balance'
channel.basic_publish(exchange='', routing_key='logging', body=message)    
print("[x] Sent %r" % message)
connection.close()

