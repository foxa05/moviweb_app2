from database import db


class User(db.Model):
    """Represents a user in the database."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    movies = db.relationship('Movie', backref='user', lazy=True)


class Movie(db.Model):
    """Represents a movie in the database."""
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    director = db.Column(db.String(100), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
