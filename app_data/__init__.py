"""init Flask app & import endpoints"""

from flask import Flask  # pylint: disable=import-error

app = Flask(__name__)

from app_data import endpoints  # pylint: disable=wrong-import-position
