import psycopg2

global conn
global cursor


def connect_db():
    global conn, cursor
    conn = psycopg2.connect(user="postgres", password="Dhaarani11*", host="127.0.0.1", port="5432", database="postgres")
    cursor = conn.cursor()


# login Mdoel function
def get_password_byid(emailid):
    select_query = '''SELECT * from "user" where email = %s'''
    cursor.execute(select_query, (emailid,))
    record = cursor.fetchall()
    return record


def check_user(emailid):
    count_query = """select Count(*) from "user" where email = %s"""
    cursor.execute(count_query, (emailid,))
    count = cursor.fetchone()
    present = count[0]
    return present


def create_user(fname, lname, name, email, password, role):
    postgres_insert_query = """ INSERT INTO "user" ( first_name, last_name, user_name, email, password_hash, role) VALUES (%s,%s,%s,%s,%s,%s)"""
    record_to_insert = (fname, lname, name, email, password, role)
    cursor.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into mobile table")
    return count


# issue Management Data Model functions
def get_issue_byid(userid):
    select_query = '''SELECT * from "issue" where user_id = %s'''
    cursor.execute(select_query, (userid,))
    record = cursor.fetchall()
    return record


def update_issuedb(id, name, subject, message):
    postgres_insert_query = """ INSERT INTO "issue" (user_id, user_name, subject, message,status) VALUES (%s,%s,%s,%s,%s)"""
    record_to_insert = (id, name, subject, message, "Created")
    cursor.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into mobile table")
    if (count == 1):
        return 1
    return 0


def status_updatedb(status, issue_id):
    postgres_update_query = """ UPDATE "issue" set status = %s where issue_id = %s"""
    cursor.execute(postgres_update_query, (status, issue_id))
    conn.commit()
    count = cursor.rowcount
    if (count > 0):
        print(count, "Record inserted successfully into issue table")
        return 1
    return 0


def get_issue():
    select_query = '''SELECT * from "issue"'''
    cursor.execute(select_query)
    record = cursor.fetchall()
    return record


def check_issue(issue_id):
    connect_db()
    select_query = '''SELECT Count(*) from "issue" where issue_id = %s'''
    cursor.execute(select_query, (issue_id,))
    count = cursor.fetchone()
    present = count[0]
    if (present):
        return 1
    return 0


# course Management function
def get_course():
    connect_db()
    select_query = '''SELECT * from "course"'''
    cursor.execute(select_query)
    record = cursor.fetchall()
    return record


def get_course_info(id):
    select_query = '''SELECT * from "course" where id = %s'''
    cursor.execute(select_query, (id,))
    record = cursor.fetchall()
    return record

def get_course_video(id):
    select_query = '''SELECT * from "course_video" where course_id = %s'''
    cursor.execute(select_query, (id,))
    record = cursor.fetchall()
    return record

def get_quiz(course_id):
    select_query = '''SELECT * from "quiz" where course_id = %s'''
    cursor.execute(select_query, (course_id,))
    record = cursor.fetchall()
    return record