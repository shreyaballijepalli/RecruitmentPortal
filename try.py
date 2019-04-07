import psycopg2
db = psycopg2.connect(database="recruitment_portal", user = "postgres", password = "password", host = "127.0.0.1", port = "5432")
#username for database, password, databasename
cursor = db.cursor()


application_number = "1"
position = "f"
firstname = "d"
middlename = ""
lastname = "k"
name = "(\""+firstname+"\",\""+middlename+"\",\""+lastname+"\")"
address1 = "d"
address2 = ""
address3 = ""
# address = address1+address2+address3
#email = request.form['email']
altemail = "d"
nationality = "d"
age = "2"
date_of_birth = "2018-05-05"
caste = "d"
disability = "n"
other_info = ""
# photo = request.form['photo']
# signature = request.form['signature']

params = [position,[firstname,middlename,lastname],nationality,age,date_of_birth,
caste,altemail,disability,address1,address2,address3,other_info]



sql = "UPDATE main_table SET position_applied = '%s', name='%s',address1='%s', address2='%s', address3='%s',\
		alt_email='%s',nationality='%s',age='%d',date_of_birth='%s',caste='%s',\
disability='%s',other_info='%s' WHERE application_no = '%d';" % (position,name,address1,address2,address3, altemail,nationality,int(age),\
   		date_of_birth,caste,disability,other_info,int(application_number))

print application_number, sql

try:   
   cursor.execute(sql)
   db.commit()
   print "Form personal info is stored"
except:
	print "Info error"
