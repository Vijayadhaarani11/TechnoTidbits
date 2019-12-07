from application import app
from flask import render_template, session, redirect, request, flash, escape
from application import Model

@app.route('/dashboard/',methods=['GET'])
def dashboard():
    return render_template("student_dashboard.html")


@app.route('/courses_page/',methods=['GET'])
def courses_page():
    record = Model.get_course()
    course_title = []
    id =[]
    count = 0
    for row in record:
        course_title.append(row[1])
        id.append(row[0])
        count = count + 1
    return render_template("courses_page.html",count= count, course_title= course_title,id=id)


@app.route('/course_content/<course_id>/')
def course_content(course_id):
    record = Model.get_course_info(course_id)
    title = []
    syllabus = []
    descrip = []
    for row in record:
        syllabus.append(row[4])
        title.append(row[1])
        descrip.append(row[2])
    return render_template("course_content.html",title = title,syllabus =syllabus[0].split("("),description = descrip, id = course_id)


@app.route('/course_video/<course_id>')
def course_video(course_id):
    record = Model.get_course_video(course_id)
    url = []
    for row in record:
        url.append(row[2])
    return render_template("video.html", video_list=url, id=course_id)

@app.route('/course_quiz/<course_id>')
def course_quiz(course_id):
    record = Model.get_quiz(course_id)
    questions = []
    for question in record:
        holderDict = {}
        holderDict['id'] = question[0]
        holderDict['text'] = question[2]
        holderDict['answers'] = question[3].split(',')
        questions.append(holderDict)
    return render_template('/quiz_page.html', questions=questions, id=course_id)


@app.route('/dashboard_admin/', methods=['GET'])
def dashboard_admin():
    return render_template("dash_dashboard.html")