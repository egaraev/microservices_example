import flask, os, socket, subprocess, requests, json, consul
import time
import json
from redis import Redis
import random
from flask import Flask, render_template,request,redirect,url_for, jsonify # For flask implementation
from urllib.parse import parse_qs
from bson.json_util import dumps

 
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

keyindex, redis_ip_bytes = c.kv.get('redis')
redis_ip = redis_ip_bytes['Value'].decode()
redis_ip_only = redis_ip.split(":", 1)
redis_ip_only=redis_ip_only[0]

# add this webservice to catalog

consul_registry = {
    "id":SELF_HOSTNAME,
    "service": "redisapp",
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
REDISAPP_IP = SELF_IP
REDISAPP_PORT = '5000'
REGISTRY = ':'.join([REDISAPP_IP, REDISAPP_PORT])
c.kv.put('redisapp', REGISTRY)




app = Flask(__name__)


r = Redis(host=redis_ip_only, db=0)



@app.route("/")
def hello():
    return render_template('red.html')

	
@app.route("/api/save", methods=['POST'])
def create_item():
    content = request.json
    field = content['field']
    value = content['value'] 	
    ret= r.set(field, value)
    app.logger.debug(ret)
    return jsonify(message="Token added sucessfully"), 201

	
@app.route("/save", methods=['POST'])
def save():
    field = request.form['field']
    value = request.form['value']
    ret = r.set(field, value)
    app.logger.debug(ret)
    new_value = r.get(field)
    return render_template('red.html', saved=1, value=new_value)

@app.route("/get", methods=['POST'])
def get():
    field = request.form['field']
    value = r.get(field)
    str_value = value.decode('utf-8')
    return render_template('red.html', field=field, value=str_value)


	
	
@app.route('/health')
def health():
    data = {
        'status': 'healthy'
    }
    return json.dumps(data)	
	
	
	
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
