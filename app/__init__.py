from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
# TODO how did we get .env file?
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import routes, models