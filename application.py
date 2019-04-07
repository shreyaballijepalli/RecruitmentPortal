import os, jinja2, json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint, session
from werkzeug import secure_filename
from flask_oauth import OAuth

from app import app, cursor, db

application = Blueprint('application', __name__, template_folder='templates', static_folder='static')   

res = []

def set_params(params):
	global res
	res = params


@application.route('/insert', methods=['GET'])       #on submission of login details
def insert(): 
   return render_template('show_application.html')