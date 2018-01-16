from flask import render_template, request, flash, redirect, url_for
from app import app, db
from sqlalchemy import exc

class City(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    state_id = db.Column(db.String(2), db.ForeignKey('state.abbreviation'), nullable = False)
    state = db.relationship('State', lazy = False)

@app.route('/cities/')
def cities():
    cities = City.query.all()
    
    return render_template('table.html', items = cities, headings = ['City', 'State'], fields = ['name', 'state_id'], edit_url = 'cities_edit', delete_url = 'cities_delete', add_url = 'cities_add')

@app.route('/cities/add', methods=['POST', 'GET'])
def cities_add():
    if request.method == 'POST':
        name = request.form['name']
        state_id = request.form['state_id']

        if (len(name) > 100):
            return "City name is more than 100 characters."
        if (len(state_id) > 2):
            return "State abbreviation is more than 2 characters."

        city = City(name = name, state_id = state_id)

        db.session.add(city)

        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session().rollback()
            return "Add failed due to integrity error"

        return redirect(url_for('cities'))

    return render_template('form.html', title = 'Add City', submit_url = "", fields = zip(['City', 'State'], ['name', 'state_id']), item = None, action = 'Add')

@app.route('/cities/edit/<id>', methods=['POST', 'GET'])
def cities_edit(id):
    city = City.query.get(id)

    if request.method == 'POST':
        if city:
            city.name = request.form['name']
            city.state_id = request.form['state_id']

            db.session.commit()

        return redirect(url_for('cities'))

    return render_template('form.html', title = 'Edit City', submit_url = url_for('cities_edit', id = id), fields = zip(['City', 'State'], ['name', 'state_id']), item = city, action = 'Edit')

@app.route('/cities/delete/<id>', methods=['POST', 'GET'])
def cities_delete(id):
    city = City.query.get(id)

    if (city):
        db.session.delete(city)

        try:
            db.session.commit()
        except exc.OperationalError as e:
            db.session().rollback()
            return "Delete failed due to operational error."

    return redirect(url_for('cities'))
