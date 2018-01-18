from flask import render_template
from app import app

@app.route('/')
def index():
    return render_template('index.html', items = ['Cities', 'States', 'Conferences', 'Committees', 'Roles', 'Publications', 'Persons', 'Organisations'])
