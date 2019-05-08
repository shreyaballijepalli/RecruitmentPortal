import os, jinja2, json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint, session
from werkzeug import secure_filename
from flask_oauth import OAuth

from app import app, cursor, db

admin_section = Blueprint('admin', __name__, template_folder='templates', static_folder='static') 


@admin_section.route('view_applications', methods=['GET'])
def admin_view_part1():
	sql = "SELECT application_no, name, position_applied FROM main_table WHERE status = '%s';" %"submitted"
	cursor.execute(sql)
	rows1 = list(cursor.fetchall())

	rows = []
	for i in range(len(rows1)):
		temp = [rows1[i][0], rows1[i][1], rows1[i][2], str(rows1[i][0])+".pdf"]
		rows.append(temp)

	print rows

	return render_template('admin_view_part1.html', email_=session['email'], rows=rows)

@admin_section.route('add_admin', methods=['GET', 'POST'])
def add_admin():
	if (request.method =='POST'):

		add_email = request.form['addthisemail']

		sql = "insert into admins (email) values('%s')" % (str(add_email))
		try: 
			cursor.execute(sql)
			db.commit()
		except:
			print "error"
	return render_template('add_admin.html', email_=session['email'])

@admin_section.route('freeze_admin', methods=['GET', 'POST'])


def freeze_admin():
	if (request.method == 'POST'):
		print "freeze applications"
		sql = "UPDATE main_table SET freeze_status = \'true\' WHERE status = \'submitted\'"
		try:
			cursor.execute(sql)
			db.commit()
			print sql
		except:
			print "Db error"

	sql = "SELECT application_no, name, position_applied FROM main_table WHERE status = '%s';" %"submitted"
	cursor.execute(sql)
	rows1 = list(cursor.fetchall())

	rows = []
	for i in range(len(rows1)):
		temp = [rows1[i][0], rows1[i][1], rows1[i][2], str(rows1[i][0])+".pdf"]
		rows.append(temp)

	print rows
	return render_template('admin_view_part1.html', email_=session['email'], rows=rows)
