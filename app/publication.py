from flask import render_template, request, flash, redirect, url_for
from app import app, db
from sqlalchemy import exc

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(200), unique = True, nullable = False)
    kind = db.Column(db.String(20), nullable = False)
    publication_date = db.Column(db.Date, nullable = False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('organisation.id'), nullable = False)

@app.route('/publications')
def publications():
    publications = Publication.query.all()
    
    return render_template('table.html', items = publications, headings = ['Title', 'Kind', 'Publiction Date', 'Publisher Id'], fields = ['title', 'kind', 'publication_date', 'publisher_id'], edit_url = 'publications_edit', delete_url = 'publications_delete', add_url = 'publications_add')

@app.route('/publications/add', methods=['POST', 'GET'])
def publications_add():
    if request.method == 'POST':
        title = request.form['title']
        kind = request.form['kind']
        publication_date = request.form['publication_date']
        publisher_id = request.form['publisher_id']

        if (len(title) > 200):
            return "Publication title is more than 200 characters."
        if (len(kind) > 20):
            return "Publication kind is more than 20 characters."
        if (len(publication_date) == 0):
            publication_date = None
        if (len(publisher_id) == 0):
            publisher_id = None
        
        publication = Publication(title = title, kind = kind, publication_date = publication_date, publisher_id = publisher_id)

        db.session.add(publication)

        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session().rollback()
            app.logger.error(e)
            return "Add failed due to integrity error"

        return redirect(url_for('publications'))

    return render_template('form.html', title = 'Add Publication', submit_url = "", fields = zip(['Title', 'Kind', 'Publiction Date', 'Publisher Id'], ['title', 'kind', 'publication_date', 'publisher_id']), item = None, action = 'Add')

@app.route('/publications/edit/<id>', methods=['POST', 'GET'])
def publications_edit(id):
    publication = Publication.query.get(id)

    if request.method == 'POST':
        title = request.form['title']
        kind = request.form['kind']
        publication_date = request.form['publication_date']
        publisher_id = request.form['publisher_id']

        if (len(title) > 200):
            return "Publication title is more than 200 characters."
        if (len(kind) > 20):
            return "Publication kind is more than 20 characters."
        if (len(publication_date) == 0):
            publication_date = None
        if (len(publisher_id) == 0):
            publisher_id = None

        if publication:
            publication.title = title
            publication.kind = kind
            publication.publication_date = publication_date
            publication.publisher_id = publisher_id

            try:
                db.session.commit()
            except exc.IntegrityError as e:
                db.session().rollback()
                app.logger.error(e)
                return "Edit failed due to integrity error"

        return redirect(url_for('publications'))

    return render_template('form.html', title = 'Edit Publication', submit_url = url_for('publications_edit', id = id), fields = zip(['Title', 'Kind', 'Publiction Date', 'Publisher Id'], ['title', 'kind', 'publication_date', 'publisher_id']), item = publication, action = 'Edit')

@app.route('/publications/delete/<id>', methods=['POST', 'GET'])
def publications_delete(id):
    publication = Publication.query.get(id)

    if (publication):
        db.session.delete(publication)

        try:
            db.session.commit()
        except exc.OperationalError as e:
            db.session().rollback()
            app.logger.error(e)
            return "Delete failed due to operational error."

    return redirect(url_for('publications'))
