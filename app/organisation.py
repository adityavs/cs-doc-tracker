from flask import render_template, request, flash, redirect, url_for
from app import app, db
from sqlalchemy import exc
from util import get_url

class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(200), unique = True, nullable = False)
    abbreviation = db.Column(db.String(10), unique = True, nullable = True, default = None)
    parent_id = db.Column(db.Integer, db.ForeignKey('organisation.id'), nullable = True)
    parent = db.relationship('Organisation', lazy = False)
    children = db.relationship('Organisation', lazy = True)

@app.route('/organisations')
def organisations():
    organisations = Organisation.query.all()
    
    return render_template('table.html', items = organisations, headings = ['Name', 'Abbreviation', 'Parent Id'], fields = ['name', 'abbreviation', 'parent_id'], edit_url = 'organisations_edit', delete_url = 'organisations_delete', add_url = 'organisations_add', get_url = get_url)

@app.route('/organisations/add', methods=['POST', 'GET'])
def organisations_add():
    if request.method == 'POST':
        name = request.form['name']
        abbreviation = request.form['abbreviation']
        parent_id = request.form['parent_id']

        if (len(name) > 200):
            return "Organisation name is more than 200 characters."
        if (len(abbreviation) > 10):
            return "Organisation abbreviation is more than 10 characters."
        if (len(abbreviation) == 0):
            abbreviation = None
        if (len(parent_id) == 0):
            parent_id = None
        
        organisation = Organisation(name = name, abbreviation = abbreviation, parent_id = parent_id)

        db.session.add(organisation)

        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session().rollback()
            app.logger.error(e)
            return "Add failed due to integrity error"

        return redirect(url_for('organisations'))

    return render_template('form.html', title = 'Add Organisation', submit_url = "", fields = zip(['Organisation', 'Abbreviation', 'Parent Id'], ['name', 'abbreviation', 'parent_id']), item = None, action = 'Add')

@app.route('/organisations/edit/<id>', methods=['POST', 'GET'])
def organisations_edit(id):
    organisation = Organisation.query.get(id)

    if request.method == 'POST':
        name = request.form['name']
        abbreviation = request.form['abbreviation']
        parent_id = request.form['parent_id']

        if (len(name) > 200):
            return "Organisation name is more than 200 characters."
        if (len(abbreviation) > 10):
            return "Organisation abbreviation is more than 10 characters."
        if (len(abbreviation) == 0):
            abbreviation = None
        if (len(parent_id) == 0):
            parent_id = None

        if organisation:
            organisation.name = name
            organisation.abbreviation = abbreviation
            organisation.parent_id = parent_id

            try:
                db.session.commit()
            except exc.IntegrityError as e:
                db.session().rollback()
                app.logger.error(e)
                return "Edit failed due to integrity error"

        return redirect(url_for('organisations'))

    return render_template('form.html', title = 'Edit Organisation', submit_url = url_for('organisations_edit', id = id), fields = zip(['Name', 'Abbreviation', 'Parent Id'], ['name', 'abbreviation', 'parent_id']), item = organisation, action = 'Edit')

@app.route('/organisations/delete/<id>', methods=['POST', 'GET'])
def organisations_delete(id):
    organisation = Organisation.query.get(id)

    if (organisation):
        db.session.delete(organisation)

        try:
            db.session.commit()
        except exc.OperationalError as e:
            db.session().rollback()
            app.logger.error(e)
            return "Delete failed due to operational error."

    return redirect(url_for('organisations'))
