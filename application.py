import os, jinja2, json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint, session
from werkzeug import secure_filename
from flask_oauth import OAuth

from app import app, cursor, db

application = Blueprint('application', __name__, template_folder='templates', static_folder='static')   


@application.route('/part1', methods=['GET','POST'])       #on submission of login details
def part1(): 
	#insert
	if (request.method =='POST'):
		val = request.form['application_no']
		print val
		return render_template('application_part1.html')
	else:
		return "new application"
	# return render_template('application_placeholders_part1.html',params=params)


@application.route('/part2', methods=['GET'])       #on submission of login details
def part2(): 
   return render_template('application_part2.html')




@application.route('/insert_1', methods=['GET','POST'])       #on submission of login details
def insert_1(): 
	if (request.method =='POST'):
		position = request.form['position']
		firstname = request.form['first_name']
		middlename = request.form['middle_name']
		lastname = request.form['last_name']
		name = "("+firstname+","+middlename+","+lastname+")"
		address1 = request.form['address_1']
		address2 = request.form['address_2']
		address3 = request.form['address_3']
		address = address1+address2+address3
		email = request.form['email']
		altemail = request.form['alt_email']
		nationality = request.form['nationality']
		age = request.form['age']
		date_of_birth = request.form['date_of_birth']
		caste = request.form['caste']
		disability = request.form['disability']
		other_info = request.form['other_info']
		# photo = request.form['photo']
		# signature = request.form['signature']

		params = [position,firstname,middlename,lastname,nationality,age,date_of_birth,
		caste,email,altemail,disability,address1,address2,address3,other_info]

#update
		sql = "INSERT INTO main_table (position_applied, name, address, email, alt_email,\
		 nationality,age,date_of_birth, caste, disability,other_info) \
		VALUES('%s','%s','%s','%s','%s','%s','%d','%s','%s','%s','%s') " \
		% (position,name,address,email,altemail,nationality,
		  int(age),date_of_birth,caste,disability,other_info)

		try:   
		   cursor.execute(sql)
		   db.commit()
		   print "Form personal info is stored"
		except:
			print "Info error"

	#return "Saved!"
   	return redirect(url_for("/part1"))



@application.route('/insert_2', methods=['GET','POST'])       #on submission of login details
def insert_2(): 
	phd_date_studied = request.form['phd_university_date']
	phd_university = request.form['phd_university']
	phd_specialization = request.form['phd_specialization']
	phd_date_thesis = request.form['phd_date_thesis']
	phd_date_defence = request.form['phd_date_defence']
	phd_edu_info = "("+phd_date_studied+","+phd_university+","+phd_specialization+")"
	phd_info = "("+phd_edu_info+","+phd_date_thesis+","+phd_date_defence+")"


	masters_date_studied = request.form['masters_university_date']
	masters_university = request.form['masters_university']
	masters_specialization = request.form['masters_specialization']
	masters_info = "("+masters_date_studied+","+masters_university+","+masters_specialization+")"

	bachelors_date_studied = request.form['bachelors_university_date']
	bachelors_university = request.form['bachelors_university']
	bachelors_specialization = request.form['bachelors_specialization']
	bachelors_info = "("+bachelors_date_studied+","+bachelors_university+","+bachelors_specialization+")"

	gate_type = request.form['gate_type']
	gate_score = request.form['gate_score']
	gate_info = "("+gate_type+","+gate_score+")"

	research_specialization = request.form['research_specialization']
	research_interest = request.form['research_interest']
	research_info = "("+research_specialization+","+research_interest+")"

	print "check research ",research_interest

	post_doc = request.form['post_doc_spec']

	print "check  ",post_doc

	# post_doc1 = request.form['post_doc1']
	# post_doc2 = request.form['post_doc2']
	# post_doc3 = request.form['post_doc3']

	# post_doc = "{"+post_doc1+","+post_doc2+","+post_doc3+"}"

	params = []


	sql = "INSERT INTO education (phd,phd_thesis, masters, bachelors, gate,research,\
	 post_doc) \
	VALUES('%s','%s',%s','%s','%s','%s','%s') " \
	% (phd_edu_info,phd_info,masters_info,bachelors_info,gate_info,research_info,post_doc)

	try:   
	   cursor.execute(sql)
	   db.commit()
	   print "Form education is stored"
	except:
		print "Info error"

	return "Saved!"
   	# return render_template('application_placeholders_part1.html',params=params)