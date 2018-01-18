from flask import render_template, request, flash, redirect, url_for
from app import app, db
from sqlalchemy import exc

class Committee(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(200), unique = True, nullable = False)

@app.route('/committees')
def committees():
    committees = Committee.query.all()
    
    return render_template('table.html', items = committees, headings = ['Name'], fields = ['name'], edit_url = 'committees_edit', delete_url = 'committees_delete', add_url = 'committees_add')

@app.route('/committees/add', methods=['POST', 'GET'])
def committees_add():
    if request.method == 'POST':
        name = request.form['name']

        if (len(name) > 200):
            return "Committee name is more than 200 characters."
        
        committee = Committee(name = name)

        db.session.add(committee)

        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session().rollback()
            app.logger.error(e)
            return "Add failed due to integrity error"

        return redirect(url_for('committees'))

    return render_template('form.html', title = 'Add Committee', submit_url = "", fields = zip(['Name'], ['name']), item = None, action = 'Add')

@app.route('/committees/edit/<id>', methods=['POST', 'GET'])
def committees_edit(id):
    committee = Committee.query.get(id)

    if request.method == 'POST':
        name = request.form['name']

        if (len(name) > 200):
            return "Committee name is more than 200 characters."

        if committee:
            committee.name = name

            try:
                db.session.commit()
            except exc.IntegrityError as e:
                db.session().rollback()
                app.logger.error(e)
                return "Edit failed due to integrity error"

        return redirect(url_for('committees'))

    return render_template('form.html', title = 'Edit Committee', submit_url = url_for('committees_edit', id = id), fields = zip(['Name'], ['name']), item = committee, action = 'Edit')

@app.route('/committees/delete/<id>', methods=['POST', 'GET'])
def committees_delete(id):
    committee = Committee.query.get(id)

    if (committee):
        db.session.delete(committee)

        try:
            db.session.commit()
        except exc.OperationalError as e:
            db.session().rollback()
            app.logger.error(e)
            return "Delete failed due to operational error."

    return redirect(url_for('committees'))
