from flask import Flask, render_template, url_for, flash, redirect
from forms import GetUserInput, GetUserInputTyler
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import recommender #Neil's
import ty_recommender # Ty's
import os
import pandas as pd

# Inputs
recommended_courses = pd.read_csv('./recommended_courses.csv')

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd41f5843ea7c2f1f9de25b9b3d22fefe'

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/students', methods=['GET', 'POST'])
def home():
    form = GetUserInput()
    if form.validate_on_submit():
        course_choice = [form.course_choice.data]
        num_suggestions = int(form.num_suggestions.data)
        electives_taken = form.electives_taken.data
        electives_taken = electives_taken.split(',') if electives_taken else []
        electives_taken = [elective.strip() for elective in electives_taken]

        print(course_choice, num_suggestions, electives_taken)
        courses, _, img_name = recommender.recommender(course_choice, num_suggestions, electives_taken)

        curr_dir = os.getcwd()
        image_list = os.listdir(curr_dir + '/static/images/')
        # Delete some images so it doesn't clog up
        if len(image_list) > 5:
            for image in image_list:
                if img_name not in image:
                    os.remove(curr_dir + '/static/images/' + image)

        #print(courses)
        flash('Here\'s your list of courses!', category='success')
        return render_template("electives.html", courses = courses, img_name=img_name)

    return render_template("home.html", form=form)

@app.route('/electives', methods=['GET', 'POST'])
def electives():
    courses = []
    img_name = []
    return render_template('electives.html', courses=courses, img_name=img_name)

@app.route('/others', methods=['GET', 'POST'])
def others():
    form = GetUserInputTyler()
    if form.validate_on_submit():
        course_num = int(form.course_choice.data)
        courses = ty_recommender.recommender_system(course_num, recommended_courses)
        flash('Here\'s your list of courses!', category='success')
        return render_template("online_courses.html", courses=courses)

    return render_template("others.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)