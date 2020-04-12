import flask, os, socket, subprocess, requests, json, consul
from flask import Flask
import time
import json

SELF_HOSTNAME = str(socket.gethostname())
SELF_IP = socket.gethostbyname(SELF_HOSTNAME)


time.sleep(5) # seconds

# fetch consul's ip, so that we can talk to it.
CONSUL_ALIAS = 'consul'
CONSUL_PORT = '8500'
CONSUL_IP = subprocess.check_output(['getent', 'hosts', CONSUL_ALIAS]).decode().split()[0]



# create consul instance (not agent, just python instance)
c = consul.Consul(host=CONSUL_IP, port=CONSUL_PORT)

# get mongodb IP
keyindex, mongodb_ip_bytes = c.kv.get('mongodb')
mongodb_ip = mongodb_ip_bytes['Value'].decode()

keyindex, rabbitmq_ip_bytes = c.kv.get('rabbitmq')
rabbitmq_ip = rabbitmq_ip_bytes['Value'].decode()

keyindex, redis_ip_bytes = c.kv.get('redis')
redis_ip = redis_ip_bytes['Value'].decode()


# add this webservice to catalog

consul_registry = {
    "id":SELF_HOSTNAME,
    "service": "flaskapp",
    "address":SELF_IP,
    "port": 5000
}
#c.catalog.register('flaskapp-node', SELF_IP, service=consul_registry, dc='dc1')


# Register healthcheck
#payload = { 
#    "id": SELF_HOSTNAME,
#    "service": "flaskapp",	
#    "name": "flaskapp", 
#   "port": 5000, 
#    "check": { "name": "Check FlaskApp health", "http": "http://flaskapp:5000/health", "method": "GET", "interval": "10s", "timeout": "1s" } 
#}

url = "http://{}:8500/v1/agent/service/register".format(CONSUL_IP)
headers = {}
res = requests.put(url, data=open('register.json', 'rb'), headers=headers)

# OR we can add to kv
# add to kv
FLASKAPP_IP = SELF_IP
FLASKAPP_PORT = '5000'
REGISTRY = ':'.join([FLASKAPP_IP, FLASKAPP_PORT])
c.kv.put('flaskapp', REGISTRY)




app = Flask(__name__)




@app.route('/')
def hello_world():
    text = """Welcome to webservice. <br>
              Host IP: %s <br>
              MongoDB IP: %s <br>
			  RabitMQ IP: %s <br>
			  Redis IP: %s <br>
           """ % (SELF_IP, mongodb_ip, rabbitmq_ip, redis_ip)
    return text, 200

	
@app.route('/health')
def health():
    data = {
        'status': 'healthy'
    }
    return json.dumps(data)	
	
	
	
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
