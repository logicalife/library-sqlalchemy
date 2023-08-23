from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Numeric

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birth_date = Column(String)
    death_date = Column(String)

    def __init__(self, name, birth_date, death_date):
        self.name = name
        self.birth_date = birth_date
        self.death_date = death_date

    def __repr__(self):
        return str(self.name)


class Book(db.Model):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String)
    title = Column(String)
    publication_year = Column(String)
    author = Column(String)
    thumbnail_url = Column(String)

    def __init__(self, isbn, title, publication_year, author, thumbnail_url = ""):
        self.isbn = isbn
        self.title = title
        self.publication_year = publication_year
        self.author = author
        self.thumbnail_url = thumbnail_url

    def __repr__(self):
        return str(self.id)
