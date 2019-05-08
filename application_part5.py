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
	print(request.method)
	if (request.method =='POST'):

		sql = "SELECT status, attachment_status FROM main_table WHERE application_no = '%s';" %(session['application_number'])
		print sql
		try:
			cursor.execute(sql)
			rows1 = cursor.fetchall()
			print "rows1 ",rows1
		except:
			print("main table err")

		sql = "SELECT status FROM education WHERE application_no = '%s';" %(session['application_number'])
		try:
			print sql
			cursor.execute(sql)
			rows2 = cursor.fetchall()
			print "rows2 ",rows2
		except:
			print("edu err")

		# print rows1[0][0]=='modified' and rows1[0][1]=='modified' and rows2[0][0]=='modified'
		if rows1[0][0]=='modified' and rows1[0][1]=='modified' and rows2[0][0]=='modified':
			
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

			sql = "SELECT * FROM main_table WHERE application_no = '%s';" %(session['application_number'])
			cursor.execute(sql)
			rows1 = cursor.fetchall()
			rows1 = list(rows1[0])
			name_list = rows1[3][1:-1].split(",")
			name = " ".join(name_list)

			print("main-------")


			sql = "SELECT * FROM education WHERE application_no = '%s';" %(session['application_number'])
			cursor.execute(sql)
			rows2 = cursor.fetchall()
			rows2 = list(rows2[0])
			btech_list = rows2[2][1:-1].split(",")
			mtech_list = rows2[3][1:-1].split(",")
			phd_list = rows2[4][1:-1].split(",")
			phd_thesis = rows2[5][1:-1].split(",")
			gate_list = rows2[6][1:-1].split(",")
			research_interest =",".join(rows2[8])

			print("education-------")


			sql = "SELECT * FROM teaching_experience WHERE application_no = '%s';" %(session['application_number'])
			cursor.execute(sql)
			rows3 = cursor.fetchall()
			rows3 = list(rows3[0])

			print("check rows3-----------------",rows3)


			position_info_list = rows3[3][1:-1].split(",")
			referee1 = rows3[18][1:-1].split(",")
			referee1 = [r.replace("\"","") for r in referee1]
			referee2 = rows3[19][1:-1].split(",")
			referee3 = rows3[20][1:-1].split(",")
			post_doc =",".join(rows3[2])
			pos_info = rows3[3][1:-1].split(",")


			print("teaching_experience-------")


			experience = []
			# for i in range(len(list(rows3[4]))):
			# 	print rows3[4][i]

			# 	temp = [rows3[4][i], rows3[5][i], rows3[6][i],rows3[8][i], rows3[9][i], rows3[10][i]]
			# 	experience.append(temp)
			for i in range(len(list(rows3[4]))):
				temp = []
				temp.append(rows3[4][i])
				if len(list(rows3[5])) < i:
					temp.append(".")
				else:
					temp.append(rows3[5])
				if len(list(rows3[6])) < i:
					temp.append(".")
				else:
					temp.append(rows3[6])
				if len(list(rows3[8])) < i:
					temp.append(".")
				else:
					temp.append(rows3[8])
				if len(list(rows3[9])) < i:
					temp.append(".")
				else:
					temp.append(rows3[9])
				if len(list(rows3[10])) < i:
					temp.append(".")
				else:
					temp.append(rows3[10])
				experience.append(temp)

			projects = []
			for i in range(len(list(rows3[11]))):
				temp = [rows3[11][i], rows3[12][i], rows3[13][i], rows3[14][i]]
				projects.append(temp)

			sql = "SELECT type,filename,max(time_submitted) from attachments where type!='others' and application_no = '%s' group by type,filename;" %(session['application_number'])
			cursor.execute(sql)
			rows4 = cursor.fetchall()
			filenames = []
			print "rows4 ",rows4
			for f in list(rows4):
				filenames.append(f[1])

			sql = " SELECT * from attachments where type='others' and application_no = '%s';" %(session['application_number'])
			cursor.execute(sql)
			rows5 = cursor.fetchall()
			for f in list(rows5):
				filenames.append(f[2])
			
			print("tfg-------")
			
			params = [rows1[0], rows1[2], name, rows1[12], rows1[13], rows1[11], rows1[9], rows1[15], rows1[16], rows1[4], rows1[7], btech_list[1],btech_list[0], btech_list[3], btech_list[4], mtech_list[1],mtech_list[0], mtech_list[3], mtech_list[4],  phd_list[1], phd_list[0], phd_thesis[0], phd_thesis[1], phd_list[3], phd_list[4], gate_list[0], gate_list[1],  rows2[7], research_interest, post_doc, pos_info[0], pos_info[1], pos_info[2], pos_info[3], experience, projects, referee1[1], referee1[0], referee1[2], referee1[3], referee2[1], referee2[0], referee2[2], referee2[3], referee3[1], referee3[0], referee3[2], referee3[3], filenames]


			from create_pdf import createDocx
			createDocx(params)




			return redirect(url_for('show_applications')) 
		else:
			return render_template('application_alert_part5.html', email_=session['email'],msg="Please complete all the previous sections!!")

	# return render_template('.html',params=params, email_=session['email'], application_number=session['application_number'])