import os, jinja2, json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint, session
from werkzeug import secure_filename
from flask_oauth import OAuth
from time import gmtime, strftime


from app import app, cursor, db

application_part4 = Blueprint('application_part4', __name__, template_folder='templates', static_folder='static')   



# UPLOAD_FOLDER = os.path.basename('static/uploads')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
print("upload folder globally ",app.config['UPLOAD_FOLDER'])
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','doc','docx'])
ALLOWED_EXTENSIONS_photo = set(['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file_photo(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_photo


@application_part4.route('part4', methods=['GET'])       #on submission of login details
def part4(): 
	sql = "SELECT * FROM attachments WHERE application_no = '%s';" %(session['application_number'])
	cursor.execute(sql)
	rows = cursor.fetchall()

	sql = "SELECT attachment_status FROM main_table WHERE application_no = '%s';" %(session['application_number'])
	cursor.execute(sql)
	rows1 = cursor.fetchall()
	if rows1[0][0] == 'submitted':
		return render_template('application_readonly_part4.html', params=rows, email_=session['email'])
	
	return render_template('application_part4.html', params=rows, email_=session['email'])

@application_part4.route('insert_4', methods=['GET','POST'])       #on submission of login details
def insert_4(): 
	params = []
	if request.method == 'POST':

		photo_f = request.files['photo']
		if photo_f and allowed_file_photo(photo_f.filename):
			filename = secure_filename(photo_f.filename)
			file_name = str(session['application_number']) + "_photo_" + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) +"."+filename.split(".")[-1]
			print filename
			print "config folder ",app.config['UPLOAD_FOLDER']
			photo_f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
			sql = "INSERT INTO attachments(application_no,type,filename) VALUES ('%s','%s','%s');"%(session['application_number'],'photo',
				file_name)
			try:   
			   cursor.execute(sql)
			   db.commit()
			   print "Inserted photo"
			except:
				print "Info error"

		signature_f = request.files['signature']
		if signature_f and allowed_file_photo(signature_f.filename):
			filename = secure_filename(signature_f.filename)
			file_name = str(session['application_number']) + "_signature_" + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) +"."+filename.split(".")[-1]
			signature_f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
			sql = "INSERT INTO attachments(application_no,type,filename) VALUES ('%s','%s','%s');"%(session['application_number'],'signature',
				file_name)
			try:   
			   cursor.execute(sql)
			   db.commit()
			   print "Inserted signature"
			except:
				print "Info error"

		cv_f = request.files['cv']
		if cv_f and allowed_file(cv_f.filename):
			filename = secure_filename(cv_f.filename)
			file_name = str(session['application_number']) + "_cv_" + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) +"."+filename.split(".")[-1]
			cv_f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
			sql = "INSERT INTO attachments(application_no,type,filename) VALUES ('%s','%s','%s');"%(session['application_number'],'cv',
				file_name)
			try:   
			   cursor.execute(sql)
			   db.commit()
			   print "Inserted cv"
			except:
				print "Info error"

		teaching_f = request.files['teaching']
		if teaching_f and allowed_file(teaching_f.filename):
			filename = secure_filename(teaching_f.filename)
			file_name = str(session['application_number']) + "_teaching_" + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) +"."+filename.split(".")[-1]
			teaching_f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
			sql = "INSERT INTO attachments(application_no,type,filename) VALUES ('%s','%s','%s');"%(session['application_number'],'teaching',
				file_name)
			try:   
			   cursor.execute(sql)
			   db.commit()
			   print "Inserted teaching"
			except:
				print "Info error"

		research_f = request.files['research']
		if research_f and allowed_file(research_f.filename):
			filename = secure_filename(research_f.filename)
			file_name = str(session['application_number']) + "_research_" + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) +"."+filename.split(".")[-1]
			research_f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
			sql = "INSERT INTO attachments(application_no,type,filename) VALUES ('%s','%s','%s');"%(session['application_number'],'research',
				file_name)
			try:   
			   cursor.execute(sql)
			   db.commit()
			   print "Inserted research"
			except:
				print "Info error"

		LOP = request.files['LOP']
		if LOP and allowed_file(LOP.filename):
			filename = secure_filename(LOP.filename)
			file_name = str(session['application_number']) + "_LOP_" + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) +"."+filename.split(".")[-1]
			LOP.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
			sql = "INSERT INTO attachments(application_no,type,filename) VALUES ('%s','%s','%s');"%(session['application_number'],'LOP',
				file_name)
			try:   
			   cursor.execute(sql)
			   db.commit()
			   print "Inserted LOP"
			except:
				print "Info error"

		others = request.files.getlist('others[]')
		for f in others:
			if f and allowed_file(f.filename):
				filename = secure_filename(f.filename)
				file_name = str(session['application_number']) + "_others_" + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) +"."+filename.split(".")[-1]
				f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
				sql = "INSERT INTO attachments(application_no,type,filename) VALUES ('%s','%s','%s');"%(session['application_number'],'others',
				file_name)
				try:   
				   cursor.execute(sql)
				   db.commit()
				   print "Inserted others"
				except:
					print "Info error"

		
		sql = "UPDATE main_table SET attachment_status='%s'" %("modified")
		try:   
			cursor.execute(sql)
			db.commit()
			print "attachment_status is updated\n"
			sql = "SELECT * FROM attachments WHERE application_no = '%s';" %(session['application_number'])
			cursor.execute(sql)
			rows = cursor.fetchall()

			sql = "SELECT attachment_status FROM main_table WHERE application_no = '%s';" %(session['application_number'])
			cursor.execute(sql)
			rows1 = cursor.fetchall()
			if rows1[0][0] == 'submitted':
				return render_template('application_readonly_part4.html', params=rows, email_=session['email'])
	
			return  render_template('application_part4.html', params = rows,email_=session['email'])
		except:
			print "Info error"

	return "error!! try again"
