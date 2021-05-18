

from flask.helpers import url_for
from surveys import * #imports surveys and questions
from flask import Flask, request, render_template, redirect, flash #imports flask object, request, and jinga
from flask_debugtoolbar import DebugToolbarExtension #helps with debugging with html templates

#creates new app and you must provide key right after
app = Flask(__name__)
app.config['SECRET_KEY'] = "CBsecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#initialize user's survey responses
responses = []
number_of_questions = len(satisfaction_survey.questions)
count = 0

#Root route that will display title of survey, instructions, and start button
#start button will direct users to /questions/0
@app.route('/')
def home_page():
    survey_title = satisfaction_survey.title
    survey_instructions = satisfaction_survey.instructions
    return render_template("index.html", title = survey_title, instructions = survey_instructions)


#Handles questions
@app.route('/questions/<int:question_number>')
def show_question(question_number):
    global count
    if question_number != count:
        flash("You are trying to access an invalid question.")
        return redirect(f"/questions/{count}")
    else: 
        question_to_display = satisfaction_survey.questions[question_number].question
        question_choices = satisfaction_survey.questions[question_number].choices
        return render_template("questions.html", question = question_to_display, choices = question_choices)
    

@app.route('/answer', methods=["POST"])
def get_answer():
    answer = request.form["chosen"]
    responses.append(answer)
    
    global count
    count = 1 + count;
    if count < len(satisfaction_survey.questions):
        return redirect(f"/questions/{count}")
    else:
        count = 0
        return render_template("thankyou.html")