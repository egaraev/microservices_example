from flask import Flask, flash, render_template, redirect, url_for, request, session, escape
from module.database import Database
import MySQLdb
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import flask, os, socket, subprocess, requests, json, consul
import urllib2
from bson.json_util import dumps
from flask import Flask, request, jsonify
import pymysql
import memcache
import time

time.sleep(10)

app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"
db = Database()

jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "blablabla"
secret="blabla"

db1 = MySQLdb.connect(host="mysqldb", user="cryptouser", passwd="123456", db="cryptodb")
cur = db1.cursor()

# fetch consul's ip, so that we can talk to it.
CONSUL_ALIAS = 'consul'
CONSUL_PORT = '8500'
CONSUL_IP = subprocess.check_output(['getent', 'hosts', CONSUL_ALIAS]).decode().split()[0]
# create consul instance (not agent, just python instance)
con = consul.Consul(host=CONSUL_IP, port=CONSUL_PORT)
# get logmongo IP
keyindex, redisapp_ip_bytes = con.kv.get('redisapp')
redisapp_ip = redisapp_ip_bytes['Value'].decode()

API_ENDPOINT = "http://"+redisapp_ip+"/api/save"
req = urllib2.Request(API_ENDPOINT)
req.add_header('Content-Type', 'application/json')






class ServerError(Exception):pass

@app.route('/')
def index():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name=username_session)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_form  = request.form['username']
        password_form  = request.form['password']
        cur.execute("SELECT COUNT(1) FROM users WHERE username = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM users WHERE username = %s;", [username_form]) # FETCH THE HASHED PASSWORD
            for row in cur.fetchall():
                if password_form == row[0]:
                    session['username'] = request.form['username']
                    access_token = create_access_token(identity=username_form)
                    data = {"field": username_form, "value": access_token}
                    response = urllib2.urlopen(req, json.dumps(data))
                    return redirect(url_for('index'))
                else:
                    error = "Invalid Credential"
        else:
            error = "Invalid Credential"
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/add/')
def add():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('add.html', session_user_name=username_session)
    return redirect(url_for('login'))


@app.route('/adduser', methods = ['POST', 'GET'])
def adduser():
        if request.method == 'POST' and request.form['save']:
            if db.insert(request.form):
                flash("A new user has been added")
            else:
                flash("A new user can not be added")

            return redirect(url_for('users'))
        else:
            return redirect(url_for('users'))


@app.route('/delete/<int:id>/')
def delete(id):
    data = db.read(id)
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        if len(data) == 0:
            return redirect(url_for('users'))
        else:
            session['delete'] = id
        return render_template('delete.html', data = data, session_user_name=username_session)

    return redirect(url_for('login'))




@app.route('/deleteuser', methods = ['POST'])
def deleteuser():
    if request.method == 'POST' and request.form['delete']:

        if db.delete(session['delete']):
            flash('A user has been deleted')

        else:
            flash('A user can not be deleted')

        session.pop('delete', None)

        return redirect(url_for('users'))
    else:
        return redirect(url_for('users'))


####
@app.route('/users')
def users():
    data = db.read(None)
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('/index_u.html', session_user_name=username_session, data = data)
    return redirect(url_for('login'))


@app.route('/update/<int:id>/')
def update(id):
    data = db.read(id)
    if 'username' in session:
        username_session = escape(session['username']).capitalize()

        if len(data) == 0:
            return redirect(url_for('users'))
        else:
            session['update'] = id
        return render_template('update.html', data = data, session_user_name=username_session)

    return redirect(url_for('login'))


@app.route('/updateuser', methods=['POST'])
def updateuser():
    if request.method == 'POST' and request.form['update']:

        if db.update(session['update'], request.form):
            flash('A user has been updated')

        else:
            flash('A user can not be updated')

        session.pop('update', None)

        return redirect(url_for('users'))
    else:
        return redirect(url_for('users'))

####
@app.route('/settings')
def settings():
    data = db.read_settings(None)

    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('/index_s.html', session_user_name=username_session, data = data)
    return redirect(url_for('login'))


@app.route('/updates/<int:id>/')
def updates(id):
    data = db.read_settings(id)

    if len(data) == 0:
        return redirect(url_for('settings'))
    else:
        session['update'] = id
        return render_template('update_s.html', data=data)


@app.route('/updatesettings', methods=['POST'])
def updatesettings():
    if request.method == 'POST' and request.form['update']:

        if db.update_settings(session['update'], request.form):
            flash('A settings has been updated')

        else:
            flash('A settings can not be updated')

        session.pop('update', None)

        return redirect(url_for('settings'))
    else:
        return redirect(url_for('settings'))



@app.route('/orders')
def orders():
    data = db.read_orders(None)

    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('/index_o.html', session_user_name=username_session, data = data)
    return redirect(url_for('login'))


@app.route('/closedorders')
def closedorders():
    data = db.read_corders(None)

    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('/index_co.html', session_user_name=username_session, data = data)
    return redirect(url_for('login'))


@app.route('/logs')
def logs():


	
    memc  = memcache.Client(['memcached:11211'], debug=1);
    result = memc.get('toplogs')
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
            memc .set('toplogs', result, 60)

    else:
        print("got the data directly from memcache")
        for row in result:      
            print ("%s, %s" % (str(row[0]), str(row[1])))
		

#    data = db.read_logs(None)
    data=result

    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('/logs.html', session_user_name=username_session, data = data)
    return redirect(url_for('login'))

####


@app.route('/markets')
def markets():
    data = db.read_markets(None)

    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('/index_market.html', session_user_name=username_session, data = data)
    return redirect(url_for('login'))


@app.route('/updatem/<int:id>/')
def updatem(id):
    data = db.read_markets(id)
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        if len(data) == 0:
            return redirect(url_for('markets'))
        else:
            session['update'] = id
        return render_template('update_market.html', data = data, session_user_name=username_session)

    return redirect(url_for('login'))

@app.route('/updatemarket', methods=['POST'])
def updatemarket():
    if request.method == 'POST' and request.form['update']:

        if db.update_market(session['update'], request.form):
            flash('A market has been updated')

        else:
            flash('A market can not be updated')

        session.pop('update', None)

        return redirect(url_for('markets'))
    else:
        return redirect(url_for('markets'))

@app.route('/deletem/<int:id>/')
def deletem(id):
        data = db.read_markets(id)
        if 'username' in session:
            username_session = escape(session['username']).capitalize()
            if len(data) == 0:
                return redirect(url_for('markets'))
            else:
                session['delete'] = id
            return render_template('delete_market.html', data=data, session_user_name=username_session)

        return redirect(url_for('login'))

@app.route('/deletemarket', methods=['POST'])
def deletemarket():
        if request.method == 'POST' and request.form['delete']:

            if db.delete_markets(session['delete']):
                flash('A market has been deleted')

            else:
                flash('A market can not be deleted')

            session.pop('delete', None)

            return redirect(url_for('markets'))
        else:
            return redirect(url_for('umarkets'))

@app.route('/addm/')
def addm():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('add_market.html', session_user_name=username_session)
    return redirect(url_for('login'))



@app.route('/addmarket', methods=['POST', 'GET'])
def addmarket():
            if request.method == 'POST' and request.form['save']:
                if db.insert_market(request.form):
                    flash("A new market has been added")
                else:
                    flash("A new market can not be added")

                return redirect(url_for('markets'))
            else:
                return redirect(url_for('markets'))





#####
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

	
def query_db(result):
    db_connection = pymysql.connect("mysqldb","cryptouser","123456","cryptodb" )
    c = db_connection.cursor()
    try:
        c.execute('SELECT date, log_entry FROM logs order by log_id DESC limit 1000')
        data = c.fetchall()
        db_connection.close()
    except:
        data = 'invalid'
    return data	
	

if __name__ == '__main__':
    app.run(debug = True, port=5000, host="0.0.0.0")
