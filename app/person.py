from flask import render_template, request, flash, redirect, url_for
from app import app, db
from sqlalchemy import exc
from util import get_url

class Person(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(200), unique = True, nullable = False)

@app.route('/persons')
def persons():
    persons = Person.query.all()
    
    return render_template('table.html', items = persons, headings = ['Name'], fields = ['name'], edit_url = 'persons_edit', edit_params = None, delete_url = 'persons_delete', delete_params = None, add_url = 'persons_add', add_params = None, get_url = get_url)

@app.route('/persons/add', methods=['POST', 'GET'])
def persons_add():
    if request.method == 'POST':
        name = request.form['name']

        if (len(name) > 200):
            return "Person name is more than 200 characters."

        person = Person(name = name)

        db.session.add(person)

        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session().rollback()
            return "Add failed due to integrity error"

        return redirect(url_for('persons'))

    return render_template('form.html', title = 'Add Person', submit_url = "", fields = zip(['Name'], ['name']), item = None, action = 'Add')

@app.route('/persons/edit/<id>', methods=['POST', 'GET'])
def persons_edit(id):
    person = Person.query.get(id)

    if request.method == 'POST':
        if person:
            person.name = request.form['name']

            db.session.commit()

        return redirect(url_for('persons'))

    return render_template('form.html', title = 'Edit Person', submit_url = url_for('persons_edit', id = id), fields = zip(['Name'], ['name']), item = person, action = 'Edit')

@app.route('/persons/delete/<id>', methods=['POST', 'GET'])
def persons_delete(id):
    person = Person.query.get(id)

    if (person):
        db.session.delete(person)

        try:
            db.session.commit()
        except exc.OperationalError as e:
            db.session().rollback()
            return "Delete failed due to operational error."

    return redirect(url_for('persons'))
