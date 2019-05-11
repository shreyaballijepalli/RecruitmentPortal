# RecruitmentPortal

### PreRequisites
	- Python 2.7
	- PostgreSQL

This is a Faculty Recruitment Web Portal.

To run the project, execute the file: 

	python create_schema.py
	python authentication.py 

### About the Web Portal
The web portal has 5 forms.

#### Applicant View:

- Personal Information : This contains fields corresponding to the Position Applied, Name, Email, Date of Birth, Category, Gender and other Personal information about the candidate. All fields are compulsory in this form.
- Education : This contains fields corresponding to Education information of the candidate. It is possible to have upto 2 entries for Btech, Mtech fields. Fields corresponding to GATE, Research Specialiation, Research Interests are optional.
- Experience : This contains fields corresponding to post doc, industrial/organization experience, projects, google scholar, dblp profiles, referee information. All fields in this form are optional except the information corresponding to the 3 referees.
- Attachments : This contains option to upload photo, signature, cv, teahcing statement, research statement, list of publications , any other documents.
  Photo, signature are accepted in png,jpg,jpeg format whereas all other files are accepted only in pdf format. This page also displays previously uploaded files.
- Submit Application :  This is where the candidate can mention his Name, Place and submit the application. It is possible to modify the attachments Section even after submitting the application, but the other sections can't be modified. Once the admin freezes the application, it is not possible to edit any section of the application.   

#### Admin View:
- The Admin can view all the applications submitted so far in pdf format. All the applications are available in static/applications folder.
- The first admin has to manually added to the admins table in the database.
- There is an option to create new admin where an admin can be added by entering his/her email address.
- There is a freeze applications button. On clicking this button, all the applications submitted so far will be freezed i.e the applicant can no longer modify the application.

The files included in the project are as follows:

 - create_schema.py : This file corresponds to creating the schema i.e the tables,user-defined types required for the project.
   We have used postgres database.Before creating the schema using this file, a database named recruitment_portal has be created.
   - main_table: This is the table that stores personal information of the applicant. It has fields status, freeze_status which determine the status of the application whether it is 'submitted' or 'freezed'.  
   - education : This is the table that stores the education details of the applicant. Fields like bachelors, masters, phd are user defined fields.
   - teaching_experience: This is the table that stores experience details of the applicant. It also stores information corresponding to the three referees.
   - attachments : This is the table that stores the attachments uploaded by the applicant along with timestamp. All the attachments are stored in static/uploads folder.
   - admins: This is the table that stores the emails corresponding to admins. The first admin email has to be inserted manually.
     It can be done using the query *INSERT INTO admins (email) values(email_id);*  



 -  app.py : This is the main application file that connects to the database and maintains app variables.

 -  authentication.py : This file has code corresponding to registering blueprints and google api authentication.
 
 -  application.py : This file handles the Personal Information form in the application. It handles updating/entering data in the database,rendering the corresponding html templates.

 -  application_part2.py : This file handles the Education form in the application. It handles updating/entering data in the database,rendering the corresponding html templates.

 -  application_part3.py : This file handles the Experience form in the application. It handles updating/entering data in the database,rendering the corresponding html templates.

 -  application_part4.py : This file handles the Attachments form in the application. All the previous versions of files are displyed in the page.

 -  application_part5.py : This file handles the submit part of the application. It updates the status of the application, generates a pdf of the application which is stored in static/applications and sends emails to referees. The content that is sent to the referees can be changed in the insert_5() function in the file.

 -  admin_Section.py : This file handles the admin part of the application. It implements the add admin and freeze application functionalities.

 -  docxtopdf.py : This file converts the application from docx to pdf format.

 -  templates : This folder contains all html templates used in this application.

 -  static/applications : This folder contains all submitted applications.

 -   static/uploads :  This folder contains all files uploaded by the applicant/