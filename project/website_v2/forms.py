from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
import ty_recommender
import pandas as pd

job_list = pd.read_csv('./ZipRecruiter.csv')
jobs=job_list.iloc[:,1:6]
columns_titles = ["company","job_title",'location','salary','link']
jobs=jobs.reindex(columns=columns_titles)
jobs= jobs[0:7]

class GetUserInput(FlaskForm):
    welcome_string = 'Please enter your interests, course choices, or desired specialization'
    course_choice = StringField(welcome_string, validators=[DataRequired(), Length(min=2,max=50)])
    choices = []
    for i in range(1,11):
        choices.append((str(i), str(i)))
    num_suggestions = SelectField('Select number of choices to display', choices=choices)
    electives_taken = StringField('Enter electives taken (optional)')
    submit = SubmitField('Get best electives')


class GetUserInputTyler(FlaskForm):
    # Create choices from Ty's recommender file
    choices = []
    for i in range(len(jobs['company'].tolist())):
        choices.append((str(i), jobs['company'].tolist()[i] + ' : ' + jobs['job_title'].tolist()[i]))
    
    course_choice = SelectField('Select an example job', choices=choices, validators = [DataRequired()])
    submit = SubmitField('Get best courses')