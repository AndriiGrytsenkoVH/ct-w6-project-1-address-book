from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-duper-secret(not)'

from . import routes