import os, jinja2, json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint, session
from werkzeug import secure_filename
from flask_oauth import OAuth

from app import app, cursor, db

application_part2 = Blueprint('application_part2', __name__, template_folder='templates', static_folder='static')   


@application_part2.route('part2', methods=['GET'])       #on submission of login details
def part2(): 
	sql = "SELECT status FROM education WHERE application_no = '%s';" %(session['application_number'])
	cursor.execute(sql)
	rows = cursor.fetchall()
	if rows[0][0] == "new" :
		return render_template('application_part2.html', email_=session['email'], application_number=session['application_number'])
	elif rows[0][0] == "modified" :
		sql = "SELECT * FROM education WHERE application_no = '%s';" %(session['application_number'])
		cursor.execute(sql)
		rows = cursor.fetchall()
		rows = list(rows[0])
		btech_list = rows[2][1:-1].split(",")
		mtech_list = rows[3][1:-1].split(",")
		phd_list = rows[4][1:-1].split(",")
		phd_thesis = rows[5][1:-1].split(",")
		gate_list = rows[7][1:-1].split(",")
		# name_list = rows[3][1:-1].split(",")
		params_ = [btech_list,mtech_list,phd_list,phd_thesis,gate_list,rows[8],rows[9],rows[6]]
		
		print "retrieved properly"
		return render_template('application_placeholders_part2_.html',params=params_,email_=session['email'], application_number=session['application_number'])


@application_part2.route('insert_2', methods=['GET','POST'])       #on submission of login details
def insert_2(): 
	if (request.method =='POST'):
		bachelors_date_studied = request.form['bachelors_date_studied']
		bachelors_university = request.form['bachelors_university']
		bachelors_specialization = request.form['bachelors_specialization']
		bachelors_cgpa = request.form['bachelors_cgpa']
		bachelors_info = "("+bachelors_date_studied+","+bachelors_university+","+bachelors_specialization+","+bachelors_cgpa+")"


		masters_date_studied = request.form['masters_date_studied']
		masters_university = request.form['masters_university']
		masters_specialization = request.form['masters_specialization']
		masters_cgpa = request.form['masters_cgpa']
		masters_info = "("+masters_date_studied+","+masters_university+","+masters_specialization+","+masters_cgpa+")"



		phd_date_studied = request.form['phd_date_studied']
		phd_university = request.form['phd_university']
		phd_specialization = request.form['phd_specialization']
		phd_cgpa = request.form['phd_cgpa']
		phd_date_thesis = request.form['phd_date_thesis']
		phd_date_defence = request.form['phd_date_defence']
		phd_edu_info = "("+phd_date_studied+","+phd_university+","+phd_specialization+","+phd_cgpa+")"
		phd_info = "("+phd_date_thesis+","+phd_date_defence+")"



		gate_type = request.form['gate_type']
		gate_score = request.form['gate_score']
		gate_info = "("+gate_type+","+gate_score+")"

		research_specialization = request.form['research_specialization']
		research_interest = request.form.getlist('research_interest[]')
		research_interest = [r.encode("utf8") for r in research_interest]
		temp="{"+ ",".join(research_interest)+"}"
		research_interest_str=temp

		print "research_interest ",research_interest_str


		post_doc = request.form.getlist('post_doc_spec[]')
		post_doc = [p.encode('utf8') for p in post_doc]
		temp="{"+ ",".join(post_doc)+"}"
		post_doc_str=temp

		params = [[bachelors_date_studied,bachelors_university,bachelors_specialization,bachelors_cgpa],
		[masters_date_studied,masters_university,masters_specialization,masters_cgpa],[phd_date_studied,phd_university,phd_specialization,phd_cgpa],[phd_date_thesis,phd_date_defence],[gate_type,gate_score],research_specialization,research_interest,post_doc]

		sql = "UPDATE education SET status='%s', bachelors='%s',masters='%s',phd='%s',phd_thesis='%s',post_doc='%s',gate='%s',research_specialization='%s',research_interest='%s' WHERE application_no='%d';" % ("modified", bachelors_info, masters_info, phd_edu_info, phd_info, post_doc_str, gate_info,research_specialization,research_interest_str, int(session['application_number']))
		print sql

		try:   
		   cursor.execute(sql)
		   db.commit()
		   print "Form education is stored"
		except:
			print "Info error"

		# return "Saved!"
	return render_template('application_placeholders_part2_.html',params=params, email_=session['email'], application_number=session['application_number'])
