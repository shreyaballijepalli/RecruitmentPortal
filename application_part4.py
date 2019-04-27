import os, jinja2, json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint, session
from werkzeug import secure_filename
from flask_oauth import OAuth
from time import gmtime, strftime


from app import app, cursor, db

application_part4 = Blueprint('application_part4', __name__, template_folder='templates', static_folder='static')   



UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
	return render_template('application_part4.html')

@application_part4.route('insert_4', methods=['GET','POST'])       #on submission of login details
def insert_4(): 

	if request.method == 'POST':

		photo_f = request.files['photo']
		if photo_f and allowed_file_photo(photo_f.filename):
			filename = secure_filename(photo_f.filename)
			file_name = str(session['application_number']) + "_photo_" + strftime("%Y-%m-%d_%H:%M:%S", gmtime()) +filename.split(".")[-1]
			print filename
			photo_f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

			

		signature_f = request.files['signature']
		if signature_f and allowed_file_photo(signature_f.filename):
			filename = secure_filename(signature_f.filename)
			file_name = session['application_number'] + "_signature_" + strftime("%Y-%m-%d_%H:%M:%S", gmtime()) +filename.split(".")[-1]
			signature_f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))


		cv_f = request.files['cv']
		if cv_f and allowed_file(cv_f.filename):
			filename = secure_filename(cv_f.filename)
			file_name = session['application_number'] + "_cv_" + strftime("%Y-%m-%d_%H:%M:%S", gmtime()) +filename.split(".")[-1]
			cv_f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))


		teaching_f = request.files['teaching']
		if teaching_f and allowed_file(teaching_f.filename):
			filename = secure_filename(teaching_f.filename)
			file_name = session['application_number'] + "_teaching_" + strftime("%Y-%m-%d_%H:%M:%S", gmtime()) +filename.split(".")[-1]
			teaching_f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

		research_f = request.files['research']
		if research_f and allowed_file(research_f.filename):
			filename = secure_filename(research_f.filename)
			file_name = session['application_number'] + "_research_" + strftime("%Y-%m-%d_%H:%M:%S", gmtime()) +filename.split(".")[-1]
			research_f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

		LOP = request.files['LOP']
		if LOP and allowed_file(LOP.filename):
			filename = secure_filename(LOP.filename)
			file_name = session['application_number'] + "_LOP_" + strftime("%Y-%m-%d_%H:%M:%S", gmtime()) +filename.split(".")[-1]
			LOP.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

		others = request.files.getlist('others[]')
		for f in others:
			if f and allowed_file(f.filename):
				filename = secure_filename(f.filename)
				file_name = session['application_number'] + "_others_" + strftime("%Y-%m-%d_%H:%M:%S", gmtime()) +filename.split(".")[-1]
				f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
		return  render_template('application_part4.html')
	return "error!! try again"
