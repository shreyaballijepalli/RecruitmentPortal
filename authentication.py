import os, jinja2, json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint, session
from werkzeug import secure_filename
from flask_oauth import OAuth
from flask_login import logout_user, confirm_login, LoginManager

GOOGLE_CLIENT_ID = '968468250852-0hgdrduaga14on3nqo72mhhi0aovspel.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'AowoVK79d8yLqWt7M-5cy3mJ'
REDIRECT_URI = '/oauth2callback'  # one of the Redirect URIs from Google APIs console
 
SECRET_KEY = 'development key'
DEBUG = True

from app import app, cursor, db
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from application import application, set_params
app.register_blueprint(application, url_prefix='/application')
 
google = oauth.remote_app('google',
base_url='https://www.google.com/accounts/',
authorize_url='https://accounts.google.com/o/oauth2/auth',
request_token_url=None,
request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
'response_type': 'code'},
access_token_url='https://accounts.google.com/o/oauth2/token',
access_token_method='POST',
access_token_params={'grant_type': 'authorization_code'},
consumer_key=GOOGLE_CLIENT_ID,
consumer_secret=GOOGLE_CLIENT_SECRET)

results = []
name_ = ""

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/verify/')
def verify():
	access_token = session.get('access_token')
	if access_token is None:
		return redirect(url_for('login'))
 
	access_token = access_token[0]
	from urllib2 import Request, urlopen, URLError
	 
	headers = {'Authorization': 'OAuth '+access_token}
	req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
	None, headers)
	try:
		res = urlopen(req)
	except URLError, e:
		if e.code == 401:
			# Unauthorized - bad token
			session.pop('access_token', None)
			return redirect(url_for('login'))
		return res.read()
	 
	result = res.read()
	print 'res read ',result
	d = json.loads(result)
	global name_ 
	name_ = d['email']
	print d['email']
	
	sql = "SELECT * FROM main_table WHERE email = '%s'" % (d['email'])       #checking if user is already there in database
	cursor.execute(sql)
	global results
	results = cursor.fetchall()
	if results == []:
		query = "INSERT INTO main_table(email) VALUES ('"+d['email']+"')"
		cursor.execute(query)
		db.commit()

	confirm_login()
	set_params(results)
	return redirect(url_for('show_applications')) 
	# else:
	# 	print "existing"
	# 	return redirect(url_for('menu.show_menu'))

@app.route('/menu/', methods=['GET'])       #on submission of login details
def show_applications(): 

	return render_template('show_application.html', rows=results, name_=name_)

@app.route('/login')
def login():
	callback=url_for('authorized', _external=True)
	return google.authorize(callback=callback)
 
@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
	access_token = resp['access_token']
	session['access_token'] = access_token, ''
	return redirect(url_for('verify'))
 
@google.tokengetter
def get_access_token():
	return session.get('access_token')

 
if __name__ == '__main__':
	app.run(debug = True)