from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object('config')

app.secret_key = os.environ['APP_SECRET_KEY']

db = SQLAlchemy(app)

from app import city, state
