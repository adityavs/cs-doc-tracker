from flask import render_template, request, flash, redirect, url_for
from app import app, db
from sqlalchemy import exc

class Conference(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(200), unique = True, nullable = False)
    start_date = db.Column(db.Date, nullable = False)
    end_date = db.Column(db.Date, nullable = False)
    city = db.Column(db.String(100), db.ForeignKey('city.name'), nullable = True)
    state = db.Column(db.String(2), db.ForeignKey('state.abbreviation'), nullable = True)

@app.route('/conferences/')
def conferences():
    conferences = Conference.query.all()
    
    return render_template('table.html', items = conferences, headings = ['Name', 'Start Date', 'End Date', 'City', 'State'], fields = ['name', 'start_date', 'end_date', 'city', 'state'], edit_url = 'conferences_edit', delete_url = 'conferences_delete', add_url = 'conferences_add')

@app.route('/conferences/add', methods=['POST', 'GET'])
def conferences_add():
    if request.method == 'POST':
        name = request.form['name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        city = request.form['city']
        state = request.form['state']

        if (len(name) > 200):
            return "Conference name is more than 200 characters."
        if (len(start_date) == 0):
            start_date = None
        if (len(end_date) == 0):
            end_date = None
        if (len(city) == 0):
            city = None
        if (len(state) == 0):
            state = None
        
        conference = Conference(name = name, start_date = start_date, end_date = end_date, city = city, state = state)

        db.session.add(conference)

        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session().rollback()
            app.logger.error(e)
            return "Add failed due to integrity error"

        return redirect(url_for('conferences'))

    return render_template('form.html', title = 'Add Conference', submit_url = "", fields = zip(['Name', 'Start Date', 'End Date', 'City', 'State'], ['name', 'start_date', 'end_date', 'city', 'state']), item = None, action = 'Add')

@app.route('/conferences/edit/<id>', methods=['POST', 'GET'])
def conferences_edit(id):
    conference = Conference.query.get(id)

    if request.method == 'POST':
        name = request.form['name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        city = request.form['city']
        state = request.form['state']

        if (len(name) > 200):
            return "Conference name is more than 200 characters."
        if (len(start_date) == 0):
            start_date = None
        if (len(end_date) == 0):
            end_date = None
        if (len(city) == 0):
            city = None
        if (len(state) == 0):
            state = None

        if conference:
            conference.name = name
            conference.start_date = start_date
            conference.end_date = end_date
            conference.city = city
            conference.state = state

            try:
                db.session.commit()
            except exc.IntegrityError as e:
                db.session().rollback()
                app.logger.error(e)
                return "Edit failed due to integrity error"

        return redirect(url_for('conferences'))

    return render_template('form.html', title = 'Edit Conference', submit_url = url_for('conferences_edit', id = id), fields = zip(['Name', 'Start Date', 'End Date', 'City', 'State'], ['name', 'start_date', 'end_date', 'city', 'state']), item = conference, action = 'Edit')

@app.route('/conferences/delete/<id>', methods=['POST', 'GET'])
def conferences_delete(id):
    conference = Conference.query.get(id)

    if (conference):
        db.session.delete(conference)

        try:
            db.session.commit()
        except exc.OperationalError as e:
            db.session().rollback()
            app.logger.error(e)
            return "Delete failed due to operational error."

    return redirect(url_for('conferences'))
