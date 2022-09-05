"""init Flask app & import endpoints"""
from flask import Flask  # pylint: disable=import-error
from flask_sqlalchemy import SQLAlchemy

from app_data.secrets import DB_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)

from app_data import endpoints  # pylint: disable=wrong-import-position
