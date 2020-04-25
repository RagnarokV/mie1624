from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class GetUserInput(FlaskForm):
    course_choice = StringField('Please enter your interests, course choices or desired specialization', validators=[DataRequired(), Length(min=2,max=50)])
    choices = []
    for i in range(1,11):
        choices.append((str(i), str(i)))
    num_suggestions = SelectField('Select number of choices to display', choices=choices)
    electives_taken = StringField('Enter electives taken (optional)')
    submit = SubmitField('Get best electives')