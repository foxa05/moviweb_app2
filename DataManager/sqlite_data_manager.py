from .data_manager_interface import DataManagerInterface
from models import User, Movie
from database import db


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app=None):
        if app:
            self.db = app.extensions['sqlalchemy'].db
            self.app = app
        else:
            self.db = None

    def list_all_users(self):
        users = User.query.all()
        return users

    def get_user_movies(self, user_id):
        user = User.query.get(user_id)
        if user:
            movies = user.movies
            return movies
        return []

    def add_movie(self, user_id, movie_title):
        try:
            user = User.query.get(user_id)
            if user:
                new_movie = Movie(title=movie_title)

                # Associate the movie with the user
                user.movies.append(new_movie)

                # Manually handle the session within a context
                with self.app.app_context():
                    self.db.session.add(new_movie)
                    self.db.session.commit()
                return None  # Return None on success
            else:
                return "User not found"
        except Exception as e:
            return str(e)  # Return the error message as a string

    def get_movie(self, user_id, movie_id):
        movie = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
        return movie

    def update_movie(self, user_id, movie_id, updated_movie):
        movie = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
        if movie:
            # Update the movie fields based on updated_movie
            movie.title = updated_movie['title']
            movie.director = updated_movie['director']
            movie.year = updated_movie['year']
            movie.rating = updated_movie['rating']
            self.db.session.commit()
        else:
            return "Movie not found"

    def delete_movie(self, user_id, movie_id):
        movie = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
        if movie:
            # Delete the movie from the session and commit
            self.db.session.delete(movie)
            self.db.session.commit()
        else:
            return "Movie not found"
