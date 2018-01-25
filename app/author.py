from flask import render_template, request, flash, redirect, url_for
from app import app, db, person
from sqlalchemy import exc
from sqlalchemy.sql import select
from util import get_url

class Author(db.Model):
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'), primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key = True)
    publication = db.relationship('Publication', lazy = False)
    author = db.relationship('Person', lazy = False)

@app.route('/publications/<publication_id>/authors')
def authors(publication_id):
    authors = db.session.query(Author).filter(Author.publication_id == publication_id)

    url_params = { 'publication_id' : publication_id }

    return render_template('table.html', items = [author.author for author in authors], headings = ['Name'], fields = ['name'], edit_url = 'authors_edit', edit_params = url_params, delete_url = 'authors_delete', delete_params = url_params, add_url = 'authors_add', add_params = url_params, get_url = get_url)

@app.route('/publications/<publication_id>/authors/add', methods = ['POST', 'GET'])
def authors_add(publication_id):
    if request.method == 'POST':
        name = request.form['name']

        author_id = db.session.scalar(select([person.Person.__table__.c.id]).where(person.Person.__table__.c.name == name))

        if author_id:
            publication_author_mapping = Author(publication_id = publication_id, author_id = author_id)
            db.session.add(publication_author_mapping)

            db.session.commit()
        else:
            return 'No author found with name' + name

        return redirect(url_for('authors', publication_id = publication_id))

    return render_template('form.html', title = 'Add Author', submit_url = "", fields = zip(['Name'], ['name']), item = None, action = 'Add')

@app.route('/publications/<publication_id>/authors/edit/<id>', methods=['POST', 'GET'])
def authors_edit(publication_id, id):
    author = Author.query.filter(Author.publication_id == publication_id, Author.author_id == id).first()

    if request.method == 'POST':
        if author:
            author.author.name = request.form['name']

            db.session.commit()

        return redirect(url_for('authors', publication_id = publication_id))

    return render_template('form.html', title = 'Edit Author', submit_url = url_for('authors_edit', publication_id = publication_id, id = id), fields = zip(['Name'], ['name']), item = author.author, action = 'Edit')

@app.route('/publications/<publication_id>/authors/delete/<id>', methods=['POST', 'GET'])
def authors_delete(publication_id, id):
    author = Author.query.filter(Author.publication_id == publication_id, Author.author_id == id).first()

    if author:
        db.session.delete(author)

        try:
            db.session.commit()
        except exc.OperationalError as e:
            db.session().rollback()
            return "Delete failed due to operation error."

    return redirect(url_for('authors', publication_id = publication_id))
