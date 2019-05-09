'''
This is the part that handles the third form. 
The function part3() corresponds to the get request of the form. It checks if the application is a new one or already modified one.
If it is a new application, we show a new empty form else we retrieve from database and show the previously entered values.
This form can be updated multiple times till application is submitted.
The function insert3() corresponds to the post request of the form. This is responsible for updating the entered details in the database.
The table corresponding to this form is teching_experience.
'''

import os, jinja2, json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint, session
from werkzeug import secure_filename
from flask_oauth import OAuth
from dateutil import relativedelta
from datetime import datetime
from nocache import nocache


from app import app, cursor, db

application_part3 = Blueprint('application_part3', __name__, template_folder='templates', static_folder='static')   


@application_part3.route('part3', methods=['GET'])       #on submission of login details
@nocache

def part3(): 
	sql = "SELECT status FROM teaching_experience WHERE application_no = '%s';" %(session['application_number'])
	cursor.execute(sql)
	rows = cursor.fetchall()
	if rows[0][0] == "new" :												# if the application is new show new empty form
		return render_template('application_part3.html', email_=session['email'], application_number=session['application_number'])
	else:																	# else retrieve already present data
		sql = "SELECT * FROM teaching_experience WHERE application_no = '%s';" %(session['application_number'])
		cursor.execute(sql)
		rows = cursor.fetchall()
		rows = list(rows[0])
		position_info_list = rows[3][1:-1].split(",")
		referee1 = rows[18][1:-1].split(",")
		referee1 = [r.replace("\"","") for r in referee1]
		referee2 = rows[19][1:-1].split(",")
		referee2 = [r.replace("\"","") for r in referee2]
		referee3 = rows[20][1:-1].split(",")
		referee3 = [r.replace("\"","") for r in referee3]

		# fetch the already stored values in the database and display them
		params_ = [rows[2],position_info_list,rows[4],rows[5],rows[6],rows[8],rows[9],rows[10],rows[11],rows[12],
		rows[13],rows[14],rows[15],rows[16],rows[17],referee1,referee2,referee3,rows[21]]

		sql = "SELECT freeze_status FROM main_table WHERE application_no = '%s';" %(session['application_number'])
		cursor.execute(sql)
		freeze_rows = cursor.fetchall()

		if freeze_rows[0][0] == "true":
			return render_template('application_readonly_freezed_part3.html',email_=session['email'],params=params_, application_number=session['application_number'])		
		elif rows[1] == "submitted" :												#if status is submitted the person can no longer chnage the form
			return render_template('application_readonly_part3.html',email_=session['email'],params=params_, application_number=session['application_number'])
		return render_template('application_placeholders_part3.html',params=params_,email_=session['email'], application_number=session['application_number'])
	

@application_part3.route('insert_3', methods=['GET','POST'])       #on submission of login details
@nocache

def insert_3(): 
	if (request.method =='POST'):

		post_doc = request.form.getlist('post_doc_spec[]')
		post_doc = [p.encode('utf8') for p in post_doc]
		temp="{"+ ",".join(post_doc)+"}"
		post_doc_str=temp

		current_position = request.form['current_position']
		pay_band = request.form['pay_band']
		grade_pay = request.form['grade_pay']
		consolidated_salary = request.form['consolidated_salary']
		position_info = "("+current_position+","+pay_band+","+grade_pay+","+consolidated_salary+")"


		experience_org = request.form.getlist('experience_org[]')
		experience_org = [r.encode("utf8") for r in experience_org]
		temp="{"+ ",".join(experience_org)+"}"
		experience_org_str=temp

		start_date = request.form.getlist('start_date[]')
		print("check start date --------",start_date)
		start_date = [r.encode("utf8") for r in start_date]
		temp="{"+ ",".join(start_date)+"}"
		start_date_str=temp


		end_date = request.form.getlist('end_date[]')
		end_date = [r.encode("utf8") for r in end_date]
		temp="{"+ ",".join(end_date)+"}"
		end_date_str=temp



		total_period = []
		# temp = "{"

		if (len(start_date)!=0 and start_date[0]!="") and (len(end_date)!=0 and end_date[0]!=""):
			for i in range(len(start_date)):		
				d1 =  start_date[i].replace('/','-')
				d1 =  datetime.strptime(d1, '%Y-%m-%d')
				d2 =  end_date[i].replace('/','-')
				d2 = datetime.strptime(d2, '%Y-%m-%d')
				difference = relativedelta.relativedelta(d1, d2)
				diff = str(difference.years)+"years "+ str(difference.months)+"months"
				total_period.append(str(diff))

		temp="{"+ ",".join(total_period)+"}"
		total_period_str=temp





		# total_period = request.form.getlist('total_period[]')
		# temp="{"+ ",".join(total_period)+"}"
		# total_period_str=temp



		# total_period = [r for r in total_period]

		full_time = request.form.getlist('full_time[]')
		full_time = [r.encode("utf8") for r in full_time]
		temp="{"+ ",".join(full_time)+"}"
		full_time_str=temp

		desgn = request.form.getlist('desgn[]')
		desgn = [r.encode("utf8") for r in desgn]
		temp="{"+ ",".join(desgn)+"}"
		desgn_str=temp

		type_of_work = request.form.getlist('type_of_work[]')
		type_of_work = [r.encode("utf8") for r in type_of_work]
		temp="{"+ ",".join(type_of_work)+"}"
		type_of_work_str=temp

		# experience_str = "{";
		# for i in range(len(experience_org)):
		# 	temp = "("+experience_org[i]+","+start_date[i]+","+end_date[i]+","+total_period[i]+","+full_time[i]+","+desgn[i]+","+type_of_work[i]+")"
		# 	if i==len(experience_org)-1:
		# 		experience_str+=temp+"}"
		# 	else:
		# 		experience_str+=temp+","


		google_scholar = request.form['google_scholar']
		dblp = request.form['dblp']
		linkedin = request.form['linkedin']

		sponsored_project_title = request.form.getlist('sponsored_project_title[]')
		consultancy_project_title = request.form.getlist('consultancy_project_title[]')

		if len(sponsored_project_title)!=0 and sponsored_project_title[0]!="":
			temp="{"+ ",".join(sponsored_project_title) + ","
		else:
			temp="{"
		temp+=",".join(consultancy_project_title)+"}"

		project_title_str=temp
		merged_project_title = sponsored_project_title+consultancy_project_title


		sponsored_project_amount = request.form.getlist('sponsored_project_amount[]')
		consultancy_project_amount = request.form.getlist('consultancy_project_amount[]')
		if len(sponsored_project_amount)!=0 and sponsored_project_amount[0]!="":
			temp = "{"+ ",".join(sponsored_project_amount) + ","
		else:
			temp = "{"
		temp += ",".join(consultancy_project_amount)+"}"
		project_amount_str = temp
		merged_project_amount=sponsored_project_amount+consultancy_project_amount 

		sponsored_project_details = request.form.getlist('sponsored_project_details[]')
		consultancy_project_details = request.form.getlist('consultancy_project_details[]')
		if len(sponsored_project_details)!=0 and sponsored_project_details[0]!="":
			temp = "{"+ ",".join(sponsored_project_details) + ","
		else:
			temp = "{"
		temp += ",".join(consultancy_project_details)+"}"
		project_details_str = temp
		merged_project_details=sponsored_project_details+consultancy_project_details 


		project_type = []

		if len(sponsored_project_title)!=0 and sponsored_project_title[0]!="" and len(consultancy_project_title) and consultancy_project_title[0]!="":
			project_type_str="{"
			for i in range(len(sponsored_project_title)):
				project_type.append("sponsored")
				project_type_str+="sponsored"+","

			for i in range(len(consultancy_project_title)):
				project_type.append("consultancy")
				if i == len(consultancy_project_amount)-1:
					project_type_str+="consultancy}"
				else:
					project_type_str+="consultancy"+","
		else:
			project_type_str="{}"



		referee1_email = request.form['referee1_email']
		referee1_name = request.form['referee1_name']
		referee1_desg = request.form['referee1_desg']
		referee1_address = request.form['referee1_address']
		referee1_info = "("+referee1_email+","+referee1_name+","+referee1_desg+",\""+referee1_address+"\")";

		referee2_email = request.form['referee2_email']
		referee2_name = request.form['referee2_name']
		referee2_desg = request.form['referee2_desg']
		referee2_address = request.form['referee2_address']
		referee2_info = "("+referee2_email+","+referee2_name+","+referee2_desg+",\""+referee2_address+"\")";


		referee3_email = request.form['referee3_email']
		referee3_name = request.form['referee3_name']
		referee3_desg = request.form['referee3_desg']
		referee3_address = request.form['referee3_address']
		referee3_info = "("+referee3_email+","+referee3_name+","+referee3_desg+",\""+referee3_address+"\")";


		remarks = request.form['remarks']



		sql = "UPDATE teaching_experience SET status='%s',post_doc='%s',position='%s',\
		experience_organization='%s',experience_start_date='%s',experience_end_date='%s',\
		experience_total_period = '%s',experience_full_time='%s',experience_desgn='%s',\
		experience_type_of_work = '%s',project_type='%s',project_title='%s',project_amount= '%s',\
		project_details='%s',google_scholar='%s',dblp='%s',linkedin='%s',referee1='%s',referee2='%s',referee3='%s',remarks='%s'\
		WHERE application_no='%d';" %("modified",post_doc_str,position_info,experience_org_str,start_date_str,end_date_str,
			total_period_str,full_time_str,desgn_str,type_of_work_str,project_type_str,project_title_str,
			project_amount_str,project_details_str,google_scholar,dblp,linkedin,referee1_info,referee2_info,referee3_info,remarks,int(session['application_number']))
		print sql
		try:   
		   cursor.execute(sql)
		   db.commit()
		   print "Form teaching_experience is stored"
		except:
			print "Info error"


		params = [post_doc,[current_position,pay_band,grade_pay,consolidated_salary],experience_org,start_date,end_date,
		full_time,desgn,type_of_work,project_type,merged_project_title,merged_project_amount,merged_project_details,
		google_scholar,dblp,linkedin,[referee1_email,referee1_name,referee1_desg,referee1_address],[referee2_email,referee2_name,
		referee2_desg,referee2_address],[referee3_email,referee3_name,referee3_desg,referee3_address],remarks]

		# return "Saved!"
	return render_template('application_placeholders_part3.html',params=params, email_=session['email'], application_number=session['application_number'])
