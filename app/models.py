from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50), nullable=False)
    # Last name is optional
    last_name = db.Column(db.String(50))

    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    addresses = db.relationship('Address', backref = 'owner', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.user_id} | {self.username}>"

    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)

    # get_id override for UserMixin
    # needed because default searches for 'id'
    # but naming convention in 'class_id'
    def get_id(self):
        return (self.user_id)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Address(db.Model):
    address_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    # Last name is optional
    last_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))
    address = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Address {self.address_id} | by User {self.user_id}>"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'first_name', 'last_name', 'phone_number', 'address'}:
                setattr(self, key, value)
        db.session.commit()    

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # get_id override for UserMixin
    # needed because default searches for 'id'
    # but naming convention in 'class_id'
    def get_id(self):
        return (self.user_id)
