import os, jinja2

from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint
from werkzeug import secure_filename



global app
app = Flask(__name__, template_folder='templates/')
app.secret_key = 'secret'

# def nocache(view):
#     @wraps(view)
#     def no_cache(*args, **kwargs):
#         response = make_response(view(*args, **kwargs))
#         response.headers['Last-Modified'] = datetime.now()
#         response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
#         response.headers['Pragma'] = 'no-cache'
#         response.headers['Expires'] = '-1'
#         return response
        
#     return update_wrapper(no_cache, view)


#################### connect to database ###############
#!/usr/bin/python
import psycopg2
db = psycopg2.connect(database="recruitment_portal", user = "postgres", password = "root", host = "127.0.0.1", port = "5432")
#username for database, password, databasename
cursor = db.cursor()
