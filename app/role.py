from flask import render_template, request, flash, redirect, url_for
from app import app, db
from sqlalchemy import exc

class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(200), unique = True, nullable = False)

@app.route('/roles/')
def roles():
    roles = Role.query.all()
    
    return render_template('table.html', items = roles, headings = ['Name'], fields = ['name'], edit_url = 'roles_edit', delete_url = 'roles_delete', add_url = 'roles_add')

@app.route('/roles/add', methods=['POST', 'GET'])
def roles_add():
    if request.method == 'POST':
        name = request.form['name']

        if (len(name) > 200):
            return "Role name is more than 200 characters."
        
        role = Role(name = name)

        db.session.add(role)

        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session().rollback()
            app.logger.error(e)
            return "Add failed due to integrity error"

        return redirect(url_for('roles'))

    return render_template('form.html', title = 'Add Role', submit_url = "", fields = zip(['Name'], ['name']), item = None, action = 'Add')

@app.route('/roles/edit/<id>', methods=['POST', 'GET'])
def roles_edit(id):
    role = Role.query.get(id)

    if request.method == 'POST':
        name = request.form['name']

        if (len(name) > 200):
            return "Role name is more than 200 characters."

        if role:
            role.name = name

            try:
                db.session.commit()
            except exc.IntegrityError as e:
                db.session().rollback()
                app.logger.error(e)
                return "Edit failed due to integrity error"

        return redirect(url_for('roles'))

    return render_template('form.html', title = 'Edit Role', submit_url = url_for('roles_edit', id = id), fields = zip(['Name'], ['name']), item = role, action = 'Edit')

@app.route('/roles/delete/<id>', methods=['POST', 'GET'])
def roles_delete(id):
    role = Role.query.get(id)

    if (role):
        db.session.delete(role)

        try:
            db.session.commit()
        except exc.OperationalError as e:
            db.session().rollback()
            app.logger.error(e)
            return "Delete failed due to operational error."

    return redirect(url_for('roles'))
