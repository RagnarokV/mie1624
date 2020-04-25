from flask import Flask, render_template, url_for, flash, redirect
from forms import GetUserInput
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import recommender
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = 'd41f5843ea7c2f1f9de25b9b3d22fefe'

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
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


if __name__ == '__main__':
    app.run(debug=True)