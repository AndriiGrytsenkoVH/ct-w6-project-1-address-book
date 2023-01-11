from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()

    # print(form.data)
    if form.validate_on_submit():
        print('From Submitter and Validated')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)
        # TODO check if user already exists
        # if username == 'bs':
        #     flash('The user already exists', 'danger')
        #     return render_template('signup.html', form=form)
        flash('Thank you for signing up!', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)