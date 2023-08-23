import os, requests
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Book, Author

app = Flask(__name__)
app.secret_key = 'sbdvjh4bdcu'
file_path = os.path.abspath(os.getcwd())+"\data\library.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db.init_app(app)


def get_thumbnail_url(isbn):
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if f"ISBN:{isbn}" in data:
            book_info = data[f"ISBN:{isbn}"]
            thumbnail_url = book_info.get("thumbnail_url")
            if thumbnail_url:
                parts = thumbnail_url.rsplit("-", 1)
                if len(parts) == 2:
                    modified_url = parts[0] + "-M.jpg"
                    return modified_url
    return None


@app.route('/')
def home():
    books = Book.query.order_by(Book.title).all()
    return render_template('home.html', books=books)


@app.route('/add_author', methods=["GET", "POST"])
def add_author():
    if request.method == 'GET':
        return render_template('add_author.html')
  
    if request.method == 'POST':
        author = Author(name=request.form.get('name'), birth_date=request.form.get('birthdate'), death_date=request.form.get('death_date'))
        db.session.add(author)
        db.session.commit()
        flash('Record was successfully added')
        return redirect(url_for('add_author'))


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'GET':
        return render_template('add_book.html', authors=Author.query.all())
  
    if request.method == 'POST':
        thumbnail_url = get_thumbnail_url(request.form.get('isbn'))
        book = Book(request.form.get('isbn'), request.form.get('title'), request.form.get('publication_year'), request.form.get('author'), thumbnail_url)
        db.session.add(book)
        db.session.commit()
        flash('Record was successfully added')
        return redirect(url_for('add_book'))


@app.route('/sort_books', methods=['POST'])
def sort_books():
    sort_option = request.form.get('sort_option')
    if sort_option == 'title':
        books = Book.query.order_by(Book.title).all()
    elif sort_option == 'author':
        books = Book.query.order_by(Book.author).all()
    else:
        # Default sorting (by title)
        books = Book.query.order_by(Book.title).all()

    return render_template('home.html', books=books)


@app.route('/search_books', methods=['GET'])
def search_books():
    search_query = request.args.get('search_query').strip()
    if search_query:
        search_results = Book.query.filter(Book.title.ilike(f'%{search_query}%')).all()
        return render_template('home.html', books=search_results)
    else:
        no_results_message = "No books found for the search query."
        return render_template('home.html', no_results_message=no_results_message)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully')
    return redirect(url_for('home'))


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
