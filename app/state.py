from flask import render_template, request, flash, redirect, url_for
from app import app, db
from sqlalchemy import exc

class State(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    abbreviation = db.Column(db.String(2), unique = True, nullable = False)
    cities = db.relationship('City', lazy = True)

@app.route('/states')
def states():
    states = State.query.all()
    
    return render_template('table.html', items = states, headings = ['Name', 'Abbreviation'], fields = ['name', 'abbreviation'], edit_url = 'states_edit', delete_url = 'states_delete', add_url = 'states_add')

@app.route('/states/add', methods=['POST', 'GET'])
def states_add():
    if request.method == 'POST':
        state = State(name = request.form['name'], abbreviation = request.form['abbreviation'])

        db.session.add(state)

        db.session.commit()

        return redirect(url_for('states'))

    return render_template('form.html', title = 'Add State', submit_url = "", fields = zip(['Name', 'Abbreviation'], ['name', 'abbreviation']), item = None, action = 'Add')

@app.route('/states/edit/<id>', methods=['POST', 'GET'])
def states_edit(id):
    state = State.query.get(id)

    if request.method == 'POST':
        if state:
            state.name = request.form['name']
            state.abbreviation = request.form['abbreviation']

            db.session.commit()

        return redirect(url_for('states'))

    return render_template('form.html', title = 'Edit State', submit_url = url_for('states_edit', id = id), fields = zip(['Name', 'Abbreviation'], ['name', 'abbreviation']), item = state, action = 'Edit')

@app.route('/states/delete/<id>', methods=['POST', 'GET'])
def states_delete(id):
    state = State.query.get(id)

    if state:
        db.session.delete(state)

        try:
            db.session.commit()
        except exc.OperationalError as e:
            db.session().rollback()
            return "Delete failed due to operation error."

    return redirect(url_for('states'))
