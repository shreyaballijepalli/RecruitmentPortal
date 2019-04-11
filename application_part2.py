import os, jinja2, json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint, session
from werkzeug import secure_filename
from flask_oauth import OAuth

from app import app, cursor, db

application_part2 = Blueprint('application_part2', __name__, template_folder='templates', static_folder='static')   


@application_part2.route('part2', methods=['GET'])       #on submission of login details
def part2(): 
   return render_template('application_part2.html')

@application_part2.route('insert_2', methods=['GET','POST'])       #on submission of login details
def insert_2(): 
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
	phd_info = "("+phd_edu_info+","+phd_date_thesis+","+phd_date_defence+")"



	gate_type = request.form['gate_type']
	gate_score = request.form['gate_score']
	gate_info = "("+gate_type+","+gate_score+")"

	research_specialization = request.form['research_specialization']
	research_interest = request.form['research_interest']
	research_info = "("+research_specialization+","+str(research_interest)+")"

	print "check research ",research_interest

	post_doc = request.form['post_doc_spec']

	print "check  ",post_doc

	# post_doc1 = request.form['post_doc1']
	# post_doc2 = request.form['post_doc2']
	# post_doc3 = request.form['post_doc3']

	# post_doc = "{"+post_doc1+","+post_doc2+","+post_doc3+"}"

	sql = "UPDATE education SET bachelors='%s',masters='%s',phd='%s',phd_thesis='%s',post_doc='%s',gate='%s',research='%s' WHERE application_no='%d';" % (bachelors_info, masters_info, phd_edu_info, phd_info, post_doc, gate_info,research_info, int(session['application_number']))
	try:   
	   cursor.execute(sql)
	   db.commit()
	   print "Form education is stored"
	except:
		print "Info error"

	return "Saved!"
   	# return render_template('application_placeholders_part1.html',params=params)