##IMPORTS

from application import app
from flask import request, render_template, redirect, flash, session, url_for
import hashlib  # library for hashing
from application import Model
global user_name, user_id
app.secret_key = '$JLmL!eCQXyajbdu2LCJ&Vwqs2JGagg3B&FRfexCmKB'


def check_password(hashed_password, user_password):
    return hashed_password == hashlib.sha256(user_password.encode()).hexdigest()
###LOGIN THE USER
@app.route('/login/', methods=['POST'])
def login():
    formData = request.form
    # validation
    if formData['email'] == "":
        flash("The username field is required.")
        return redirect("/")
    if formData['password'] == "":
        flash("The password field is required.")
        return redirect("/")
    Model.connect_db()
    row = Model.get_password_byid(formData['email'])
    hashed_password = 0
    for idx in row:
        print("Entering for loop")
        global user_name, user_id
        user_name = idx[3]
        print("in for loop", idx[3])
        user_id = idx[0]
        hashed_password = idx[5]
    print("user password", formData['password'])
    print("User name", user_name)
    print("Displaying password", hashed_password)

    # check the password
    if check_password(hashed_password, formData['password']):
        if formData['email'] == 'admin':
            return render_template("dash_dashboard.html")
        return render_template("student_dashboard.html")
    flash("Your password was incorrect.")
    return redirect("/")


###REGISTER THE USER
@app.route('/register/', methods=['GET', 'POST'])
def Sign_up():
    # form data is GET, so render template
    if request.method == 'GET':
        return render_template('register.html')

    # request method is POST, so do everything

    formData = request.form

    # form validation
    if formData['email'] == "" or formData['password'] == "" or formData['password2'] == "":
        flash("All text fields are required")
        return redirect(url_for("register"))
    if formData['password'] != formData['password2']:
        flash("Password Mismatch")
        return redirect("/register/")
    if not 'isTeacher' in formData:  # if is teacher wasn't selected
        role = 'Student'  # they aren't a teacher
    else:
        role = 'Teacher'  # they are a teacher!
    Model.connect_db()

    password = formData['password']
    # hashing password
    # salt = uuid.uuid4().hex
    password = hashlib.sha256(password.encode()).hexdigest()
    present = Model.check_user(formData['email'])

    if (present):
        flash("Email Id already exist")
        return redirect("/register/")
    else:

        result = Model.create_user(formData['fname'], formData['lname'], formData['name'], formData['email'], password,
                                   role)
        if (result):
            flash("The entry was created")
            return redirect("/")
        else:
            flash("The entry creation unsuccessful")
            return redirect("/register/")


@app.route('/dash_dashboard/', methods=['GET'])
def view_dashboard():
    return render_template("dash_dashboard.html")
