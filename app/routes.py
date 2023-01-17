from app import app
from flask import render_template, redirect, url_for, flash, request
from app.forms import SignUpForm, LoginForm, AddressForm
from app.models import User, Address
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def index():
    if current_user.is_authenticated:
        addresses = Address.query.filter_by(user_id=current_user.user_id).all()
    else:
        addresses = []
    return render_template('index.html', addresses=addresses)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        print('From Submitted and Validated')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).first()
        if check_user:
            flash('A user with that email and/or username already exists.', 'danger')
            # TODO make so that info remains on page in case of failed user check
            return redirect(url_for('signup'))

        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        flash(f'Thank you for signing up, {new_user.first_name} {new_user.last_name}', 'success')
        login_user(new_user)
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print('From Submitted and Validated')
        username = form.username.data
        password = form.password.data
        print(username, password)

        # TODO research a better way to check for user
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f'{user.username} is now logged in', 'success')
            return redirect(url_for('index'))
        else:
            flash(f"Incorrect username or password", "warning")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out","warning")
    return redirect(url_for('index'))

# TODO why does it behave weird when routs have '-' in them
@app.route("/create-address", methods=["GET", "POST"])
@login_required
def create():
    form = AddressForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        print(first_name, last_name, phone_number, address, current_user)
        new_address = Address(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address, user_id=current_user.user_id)
        flash(f"{new_address.first_name} {new_address.last_name} is now in you address book!", 'success')
        return redirect(url_for('index'))
    return render_template('create-address.html', form=form)

@app.route('/addresses/<int:address_id>/edit', methods=["GET", "POST"])
@login_required
def edit_address(address_id):
    address_object = Address.query.get(address_id)
    if not address_object:
        flash(f"An address with id {address_id} does not exist", "danger")
        return redirect(url_for('index'))
    # Make sure the address owner is the current user
    if address_object.owner != current_user:
        flash("You do not have permission to edit this address", "danger")
        return redirect(url_for('index'))
    form = AddressForm()
    if request.method == 'GET':
        # Pre-Fill form with old data
        form.first_name.data = address_object.first_name
        form.last_name.data = address_object.last_name
        form.phone_number.data = address_object.phone_number
        form.address.data = address_object.address
        #
    if form.validate_on_submit():
        # Get the form data
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        # update the address using the .update method
        address_object.update(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address)
        flash(f"{address_object.first_name} {address_object.last_name} address has been updated!", "success")
        return redirect(url_for('index', address_id=address_object.address_id))
    return render_template('edit-address.html', address=address_object, form=form)

@app.route('/addresses/<address_id>/delete')
@login_required
def delete_address(address_id):
    address_object = Address.query.get(address_id)
    if not address_object:
        flash(f"An address with id {address_id} does not exist", "danger")
        return redirect(url_for('index'))
    # Make sure the address owner is the current user
    if address_object.owner != current_user:
        flash("You do not have permission to delete this address", "danger")
        return redirect(url_for('index'))
    address_object.delete()
    flash(f"Address for {address_object.first_name} {address_object.last_name} has been deleted", "info")
    return redirect(url_for('index'))