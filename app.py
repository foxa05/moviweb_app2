from flask import Flask, render_template, request, redirect, url_for
from DataManager.sqlite_data_manager import SQLiteDataManager
from DataManager.data_manager_interface import DataManagerInterface
from models import User, Movie
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/larissamatteau/PycharmProjects/moviweb_app/data/library.sqlite'
db.init_app(app)

data_manager = SQLiteDataManager(app)  # Initialize the data manager


@app.route('/')
def home():
    """Renders the home page.

    Returns:
        A rendered template of the home page.
    """
    return render_template('home.html')


@app.route('/users')
def list_users():
    """Renders a page listing all users.

    Returns:
        A rendered template of the users page, with all users passed
        to the template.
    """
    users = data_manager.list_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def user_movies(user_id):
    """Renders a page showing all movies of a specific user.

    Args:
        user_id (str): The ID of the user.

    Returns:
        A rendered template of the user's movies page, with the user's
        ID and movies passed to the template.
    """
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user_id=user_id, movies=movies)


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """Renders a page to add a new movie for a specific user and handles
    the submission of the form.

    Args:
        user_id (str): The ID of the user.

    Returns:
        If the form is submitted successfully, redirects to the
        user's movies page.
        Otherwise, renders the add movie page with an error message.
    """
    error_message = None
    if request.method == 'POST':
        movie_title = request.form.get('name')

        try:
            user = User.query.get(user_id)
            if user:
                new_movie = Movie(title=movie_title)

                # Associate the movie with the user
                user.movies.append(new_movie)

                # Commit the session once after all changes
                db.session.commit()

                return redirect(url_for('user_movies', user_id=user_id))
            else:
                error_message = "User not found"
        except Exception as e:
            # Handle exceptions and log them as needed
            db.session.rollback()
            error_message = str(e)

    return render_template('add_movie.html', user_id=user_id,
                           error_message=error_message)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Renders a page to update a specific movie for a specific user and
    handles the submission of the form.

    Args:
        user_id (str): The ID of the user.
        movie_id (str): The ID of the movie.

    Returns:
        If the form is submitted successfully, redirects to the user's
        movies page.
        Otherwise, renders the update movie page with the current movie data.
    """
    if request.method == 'POST':
        updated_movie = {
            'title': request.form.get('title'),
            'director': request.form.get('director'),
            'year': int(request.form.get('year')),
            'rating': float(request.form.get('rating'))
        }
        data_manager.update_movie(user_id, movie_id, updated_movie)
        return redirect(url_for('user_movies', user_id=user_id))
    movie = data_manager.get_movie(user_id, movie_id)
    return render_template('update_movie.html', user_id=user_id,
                           movie=movie, movie_id=movie_id)


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    """Deletes a specific movie for a specific user and redirects
    to the user's movies page.

    Args:
        user_id (str): The ID of the user.
        movie_id (str): The ID of the movie.

    Returns:
        Redirects to the user's movies page.
    """
    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    """Renders a 404 page when a page is not found.

    Args:
        e (Exception): The exception that occurred.

    Returns:
        A rendered template of the 404 page, with a status code of 404.
    """
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
