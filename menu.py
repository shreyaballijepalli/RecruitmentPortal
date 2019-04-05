import os, jinja2, json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint, session
from werkzeug import secure_filename
from flask_oauth import OAuth

from app import app, cursor, db

menu = Blueprint('menu', __name__, template_folder='templates', static_folder='static')   


@menu.route('/', methods=['GET'])       #on submission of login details
def show_menu(): 
	
   return render_template('show_menu.html')



@menu.route('/insert', methods=['GET'])       #on submission of login details
def insert(): 
   return render_template('show_menu.html')