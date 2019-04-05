import psycopg2

conn = psycopg2.connect(database="recruitment_portal", user = "postgres", password = "password", host = "127.0.0.1", port = "5432")

print("Opened database successfully")

cur = conn.cursor()


#### CREATING TYPES

cur.execute('''CREATE TYPE name_info AS (first_name text, middle_name text, last_name text); ''')

cur.execute('''CREATE TYPE address_info AS (house_no text, locality text, city text,
	district text,state text,pin_code integer,country text ); ''')

cur.execute('''CREATE TYPE education_info AS (date_studied date, university text,
	specialization text);''')

cur.execute('''CREATE TYPE phd_info AS (start education_info, date_thesis education_info,
	date_defence education_info  );''')

cur.execute('''CREATE TYPE gate_info AS (type text,gate_score integer); ''')

cur.execute('''CREATE TYPE research_info AS (specialization text, interest text);''')

cur.execute('''CREATE TYPE position_info AS (position text, pay_band integer, grade_pay integer,
	consolidated_salary integer);''')

cur.execute('''CREATE TYPE experience_info AS (organization text,start_date date,end_date date,
	total_period integer,full_time boolean, desgn text, type_of_work text);''')

cur.execute('''CREATE TYPE project_info AS (project_number integer,amount integer );''')

cur.execute('''CREATE TYPE referee_info AS (email text,name name_info,desgn text,
	address address_info);''')

####CREATING TABLES


cur.execute('''CREATE TABLE main_table (name name_info,address address_info,email text,
	alt_email text, nationality text, age integer, date_of_birth date, caste text,
	disability boolean, other_info text );''')

cur.execute('''CREATE TABLE education (phd phd_info,masters education_info,
	bachelors education_info, gate gate_info, research research_info, post_doc text[]);''')

cur.execute('''CREATE TABLE teaching_experience (postion position_info, experience experience_info,
google_scholar text, dblp text, linkedin text, sponsored_project project_info,
consultancy_project project_info,referee referee_info[]  );''')




# cur.execute('''CREATE TYPE inventory_item_new2 AS (
#     name            text,
#     supplier_id     integer,
#     price           numeric
# );''')

# cur.execute('''CREATE TABLE on_hand_new2 (
#     item      inventory_item_new,
#     count     integer
# );''')

# cur.execute('''INSERT INTO on_hand_new2 VALUES (ROW('fuzzy dice', 42, 1.99), 1000);''')

# cur.execute('''SELECT * FROM on_hand_new2''')
# rows = cur.fetchall()

# for row in rows:
#    print "ITEM = ", row[0]
#    print "NAME = ", row[1]

conn.commit()
conn.close()