from flask import Flask
from flask import request, render_template, redirect, flash, session, url_for
from application import Model
from application import login
from application import app

# View issue is called to view the issue raised by the loged in user
@app.route('/view_issue/', methods=['GET'])
def view_issue():
    print("User_name:",login.user_name)
    record = Model.get_issue_byid(login.user_id)
    message = []
    status = []
    count = 0
    for row in record:
        print("Subject = ", row[3])
        print("Message =", row[4])
        message.append(row[4])
        status.append(row[5])
        count = count + 1

    return render_template('view_issue.html', my_string="Issues raised by " + login.user_name, messages=message,
                           status=status, count=count)


# raise_issue is called after the user hits the send button to record the issue
@app.route('/view_issue/', methods=['POST'])
def raise_issue():
    # get from information
    messageData = request.form

    if messageData['subject'] == '':
        flash("The subject field is required.")
        return redirect(url_for("raise_issue"))
    if messageData['message'] == '':
        flash("The username field is required.")
        return redirect(url_for("raise_issue"))
    print(messageData['subject'])
    print("  message is ", messageData['message'])
    subject = messageData['subject']
    message = messageData['message']

    if (Model.update_issuedb(login.user_id, login.user_name, subject, message)):
        print("Issue Updated Successfully")
        flash('Your Issue has been recorded')
        return view_issue()
    else:
        flash('Failed to record ur issue, Kindly retry')
        return render_template('raise_issue.html', my_string="How can we help you " + login.user_name)


# get_issue is called to record the issue by the user
@app.route('/raise_issue/', methods=['GET'])
def get_issue():
    return render_template('raise_issue.html', my_string="How can we help you " + login.user_name)


# resolve_issue  is called by the admin to update the status of the raised issue
@app.route('/resolve_issue/', methods=['GET'])
def resolve_issue():
    return render_template('resolve_issue.html')


# status_update is called to update the status of the ticket
@app.route('/view_issue_admin/', methods=['POST'])
def status_update():
    # get from information
    messageData = request.form

    if messageData['issue_id'] == '':
        flash("The issue id is required.")
        return redirect(url_for('resolve_issue'))
    if messageData.get('status') == '':
        flash("The status is required.")
        return redirect(url_for('resolve_issue'))
    print(messageData['issue_id'])
    issue_id = messageData['issue_id']

    if (Model.check_issue(issue_id)):
        status = messageData.get('status')
        issue_id = messageData['issue_id']

        if (Model.status_updatedb(status, issue_id)):
            flash('Status successfully updated in the database')
            return view_issue_admin()
        else:
            flash('Status update failed. Try again')
            return redirect(url_for('resolve_issue'))
    else:
        flash("Enter a valid Issue Id")
        return redirect(url_for('resolve_issue'))


# view_issue_admin is called by the administrator to view the
@app.route('/view_issue_admin/', methods=['GET'])
def view_issue_admin():
    record = Model.get_issue()
    message = []
    status = []
    id = []
    name = []
    subject = []
    count = 0
    for row in record:
        print("Subject = ", row[3])
        print("Message =", row[4])
        message.append(row[4])
        status.append(row[5])
        id.append(row[0])
        name.append(row[2])
        subject.append(row[3])
        count = count + 1

    return render_template('view_issue_admin.html', messages=message, status=status, count=count, id=id, name=name,
                           subject=subject)
