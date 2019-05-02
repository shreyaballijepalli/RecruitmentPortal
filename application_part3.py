import os, jinja2, json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint, session
from werkzeug import secure_filename
from flask_oauth import OAuth

from app import app, cursor, db

application_part3 = Blueprint('application_part3', __name__, template_folder='templates', static_folder='static')   


@application_part3.route('part3', methods=['GET'])       #on submission of login details
def part3(): 
	sql = "SELECT status FROM teaching_experience WHERE application_no = '%s';" %(session['application_number'])
	cursor.execute(sql)
	rows = cursor.fetchall()
	if rows[0][0] == "new" :
		return render_template('application_part3.html', email_=session['email'], application_number=session['application_number'])
	else:
		sql = "SELECT * FROM teaching_experience WHERE application_no = '%s';" %(session['application_number'])
		cursor.execute(sql)
		rows = cursor.fetchall()
		rows = list(rows[0])
		position_info_list = rows[2][1:-1].split(",")
		referee1 = rows[16][1:-1].split(",")
		referee2 = rows[17][1:-1].split(",")
		referee3 = rows[18][1:-1].split(",")

		params_ = [position_info_list,rows[3],rows[4],rows[5],rows[6],rows[7],rows[8],rows[9],rows[10],rows[11],rows[12],
		rows[13],rows[14],rows[15],referee1,referee2,referee3]
		
		# print "retrieved properly"

		if rows[1] == "submitted" :
			return render_template('application_readonly_part3.html',params=params_, application_number=session['application_number'])
		return render_template('application_placeholders_part3.html',params=params_,email_=session['email'], application_number=session['application_number'])
	

@application_part3.route('insert_3', methods=['GET','POST'])       #on submission of login details
def insert_3(): 
	if (request.method =='POST'):

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
		start_date = [r.encode("utf8") for r in start_date]
		temp="{"+ ",".join(start_date)+"}"
		start_date_str=temp


		end_date = request.form.getlist('end_date[]')
		end_date = [r.encode("utf8") for r in end_date]
		temp="{"+ ",".join(end_date)+"}"
		end_date_str=temp


		total_period = request.form.getlist('total_period[]')
		temp="{"+ ",".join(total_period)+"}"
		total_period_str=temp

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

		sponsored_project_number = request.form.getlist('sponsored_project_number[]')
		consultancy_project_number = request.form.getlist('consultancy_project_number[]')
		temp="{"+ ",".join(sponsored_project_number) + ","
		temp+=",".join(consultancy_project_number)+"}"
		project_number_str=temp
		merged_project_number = sponsored_project_number+consultancy_project_number


		sponsored_project_amount = request.form.getlist('sponsored_project_amount[]')
		consultancy_project_amount = request.form.getlist('consultancy_project_amount[]')
		temp = "{"+ ",".join(sponsored_project_amount) + ","
		temp += ",".join(consultancy_project_amount)+"}"
		project_amount_str = temp
		merged_project_amount=sponsored_project_amount+consultancy_project_amount 


		project_type = []

		project_type_str="{"

		for i in range(len(sponsored_project_number)):
			project_type.append("sponsored")
			project_type_str+="sponsored"+","

		for i in range(len(consultancy_project_amount)):
			project_type.append("consultancy")

			if i == len(consultancy_project_amount)-1:
				project_type_str+="consultancy}"
			else:
				project_type_str+="consultancy"+","




		# project_str = "{";
		# for i in range(len(sponsored_project_number)):
		# 	temp = "(sponsored,"+sponsored_project_number[i]+","+sponsored_project_amount[i]+")"
		# 	project_str+=temp+","

		# for i in range(len(consultancy_project_number)):
		# 	temp = "(consultancy,"+consultancy_project_number[i]+","+consultancy_project_number[i]+")"
		# 	if i==len(consultancy_project_number)-1:
		# 		project_str+=temp+"}"
		# 	else:
		# 		project_str+=temp+","


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



		sql = "UPDATE teaching_experience SET status='%s',position='%s',\
		experience_organization='%s',experience_start_date='%s',experience_end_date='%s',\
		experience_total_period = '%s',experience_full_time='%s',experience_desgn='%s',\
		experience_type_of_work = '%s',project_type='%s',project_number='%s',project_amount= '%s',\
		google_scholar='%s',dblp='%s',linkedin='%s',referee1='%s',referee2='%s',referee3='%s'\
		WHERE application_no='%d';" %("modified",position_info,experience_org_str,start_date_str,end_date_str,
			total_period_str,full_time_str,desgn_str,type_of_work_str,project_type_str,project_number_str,
			project_amount_str,google_scholar,dblp,linkedin,referee1_info,referee2_info,referee3_info,int(session['application_number']))
		print sql
		try:   
		   cursor.execute(sql)
		   db.commit()
		   print "Form teaching_experience is stored"
		except:
			print "Info error"


		params = [[current_position,pay_band,grade_pay,consolidated_salary],experience_org,start_date,end_date,
		total_period,full_time,desgn,type_of_work,project_type,merged_project_number,merged_project_amount,google_scholar,dblp,linkedin,[referee1_email,referee1_name,referee1_desg,referee1_address],[referee2_email,referee2_name,
		referee2_desg,referee2_address],[referee3_email,referee3_name,referee3_desg,referee3_address]]


		# for i in range(len(sponsored_project_number)):

		# 	sql2 = "INSERT INTO project_info SET type='%s',project_number='%d',amount='%d' WHERE application_no='%d';" %("sponsored",sponsored_project_number[i],sponsored_project_amount[i],int(session['application_number']))
		# 	print sql2
		# 	try:   
		# 	   cursor.execute(sql2)
		# 	   db.commit()
		# 	   print "Form sponsored project is stored"
		# 	except:
		# 		print "Info error"

		# for i in range(len(consultancy_project_number)):
		# 	sql3 = "UPDATE project_info SET type='%s',project_number='%d',amount='%d' WHERE application_no='%d';" %("consultancy",consultancy_project_number[i],consultancy_project_amount[i],int(session['application_number']))
		# 	print sql3
		# 	try:   
		# 	   cursor.execute(sql3)
		# 	   db.commit()
		# 	   print "Form consultancy project is stored"
		# 	except:
		# 		print "Info error"

		# for i in range(len(experience_org)):
		# 	sql4 = "UPDATE experience_info SET organization='%s',start_date='%s',end_date='%s',total_period='%d',full_time='%s',desgn='%s',type_of_work='%s' WHERE application_no='%d';" %(experience_org[i],start_date[i],end_date[i],
		# 		total_period[i],full_time[i],desgn[i],type_of_work[i],int(session['application_number']))
		# 	print sql4
		# 	try:   
		# 	   cursor.execute(sql4)
		# 	   db.commit()
		# 	   print "Form experience is stored"
		# 	except:
		# 		print "Info error"



		# return "Saved!"
	return render_template('application_placeholders_part3.html',params=params, email_=session['email'], application_number=session['application_number'])
