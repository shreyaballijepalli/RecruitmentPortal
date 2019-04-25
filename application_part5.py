import os, jinja2, json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint, session
from werkzeug import secure_filename
from flask_oauth import OAuth

from app import app, cursor, db

application_part5 = Blueprint('application_part5', __name__, template_folder='templates', static_folder='static')   


@application_part5.route('part5', methods=['GET'])       #on submission of login details
def part5(): 
	return render_template('application_part5.html', email_=session['email'], application_number=session['application_number'])



@application_part5.route('insert_5', methods=['GET','POST'])       #on submission of login details
def insert_5(): 
	if (request.method =='POST'):
		sql = "UPDATE main_table SET status = \'submitted\' WHERE application_no = '%d';"%(int(session['application_number']))
		print sql
		try:   
		   cursor.execute(sql)
		   db.commit()
		   print "Submitted main table"
		except:
			print "Info error"

		sql = "UPDATE education SET status = \'submitted\' WHERE application_no = '%d';"%(int(session['application_number']))
		try:   
		   cursor.execute(sql)
		   db.commit()
		   print "Submitted education"
		except:
			print "Info error"

		sql = "UPDATE teaching_experience SET status = \'submitted\' WHERE application_no = '%d';"%(int(session['application_number']))
		try:   
		   cursor.execute(sql)
		   db.commit()
		   print "Submitted teaching_experience"
		except:
			print "Info error"
		# return "Saved!"
	return redirect(url_for('show_applications')) 
	# return render_template('.html',params=params, email_=session['email'], application_number=session['application_number'])