import flask, os, socket, subprocess, requests, json, consul, sys
from flask import Flask, request, jsonify
import time
import json
import MySQLdb
import pika
import datetime


SELF_HOSTNAME = str(socket.gethostname())
SELF_IP = socket.gethostbyname(SELF_HOSTNAME)



time.sleep(15) # seconds

# fetch consul's ip, so that we can talk to it.
CONSUL_ALIAS = 'consul'
CONSUL_PORT = '8500'
CONSUL_IP = subprocess.check_output(['getent', 'hosts', CONSUL_ALIAS]).decode().split()[0]



# create consul instance (not agent, just python instance)
c = consul.Consul(host=CONSUL_IP, port=CONSUL_PORT)




# add this webservice to catalog

consul_registry = {
    "id":SELF_HOSTNAME,
    "service": "logmysql",
    "address":SELF_IP,
    "port": 5000
}


url = "http://{}:8500/v1/agent/service/register".format(CONSUL_IP)
headers = {}
res = requests.put(url, data=open('register.json', 'rb'), headers=headers)

# OR we can add to kv
# add to kv
LOGMYSQL_IP = SELF_IP
LOGMYSQL_PORT = '5000'
REGISTRY = ':'.join([LOGMYSQL_IP, LOGMYSQL_PORT])
c.kv.put('logmysql', REGISTRY)


app = Flask(__name__)



@app.route('/')
def hello_world():
    text = """Welcome to webservice. <br>
              Host IP: %s <br>
           """ % (SELF_IP)
    return text, 200

	
@app.route('/health')
def health():
    data = {
        'status': 'healthy'
    }
    return json.dumps(data)	
	

	
	
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
