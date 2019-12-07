from flask import Flask, url_for, request, render_template
app = Flask(__name__)
import application.index
import application.students
import application.login
import application.Model
import application.issue_controller