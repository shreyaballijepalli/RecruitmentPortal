import os, jinja2, json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint, session
from werkzeug import secure_filename
from flask_oauth import OAuth
import smtplib

from app import app, cursor, db

application_part5 = Blueprint('application_part5', __name__, template_folder='templates', static_folder='static')   


@application_part5.route('part5', methods=['GET'])       #on submission of login details
def part5(): 
	return render_template('application_part5.html', email_=session['email'], application_number=session['application_number'])



@application_part5.route('insert_5', methods=['GET','POST'])       #on submission of login details
def insert_5(): 
	if (request.method =='POST'):

		sql = "SELECT status, attachment_status FROM main_table WHERE application_no = '%s';" %(session['application_number'])
		cursor.execute(sql)
		rows1 = cursor.fetchall()

		sql = "SELECT status FROM education WHERE application_no = '%s';" %(session['application_number'])
		cursor.execute(sql)
		rows2 = cursor.fetchall()

		sql = "SELECT status FROM teaching_experience WHERE application_no = '%s';" %(session['application_number'])
		cursor.execute(sql)
		rows3 = cursor.fetchall()

		if rows1[0][0]=='modified' and rows1[0][1]=='modified' and rows2[0][0]=='modified' and rows3[0][0]=='modified':
			
			s = smtplib.SMTP("smtp.gmail.com", 587)
			s.ehlo()
			s.starttls()
			s.login("swegroup10@gmail.com","Swe@2019")
			msg = "You are the referee for "+str(session['application_number']) # The /n separates the message from the headers
			sql = "SELECT referee1,referee2,referee3 FROM teaching_experience WHERE application_no = '%s';" %(session['application_number'])
			try:
				cursor.execute(sql)
				rows = cursor.fetchall()
				rows = list(rows[0])
				print "rows ",rows
				email1 = rows[0].split(",")[0][1:]
				email2 = rows[1].split(",")[0][1:]
				email3 = rows[2].split(",")[0][1:]
				print email1,email2,email3
				s.sendmail("swegroup10@gmail.com", email1, msg)
				s.sendmail("swegroup10@gmail.com", email2, msg)
				s.sendmail("swegroup10@gmail.com", email3, msg)
			except:
				print "Info error email",sql
				return render_template('application_alert_part5.html', email_=session['email'], msg="Please enter reachable email ids")			

			sql = "UPDATE main_table SET status = \'submitted\', date_submitted=NOW(), attachment_status = \'submitted\' WHERE application_no = '%d';"%(int(session['application_number']))
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
			return redirect(url_for('show_applications')) 
		else:
			return render_template('application_alert_part5.html', email_=session['email'],msg="Please complete all the previous sections!!")

	# return render_template('.html',params=params, email_=session['email'], application_number=session['application_number'])