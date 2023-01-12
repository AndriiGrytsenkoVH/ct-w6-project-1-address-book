from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm
from app.models import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()

    # print(form.data)
    if form.validate_on_submit():
        print('From Submitted and Validated')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)

        # TODO research a better way to check for user
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).first()
        if check_user:
            flash('A user with that email and/or username already exists.', 'danger')
            # TODO make so that info remains on page in case of failed user check
            return redirect(url_for('signup'))

        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        flash(f'Thank you for signing up, {new_user.first_name} {new_user.last_name}', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)