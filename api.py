from flask import Blueprint, jsonify, request
from DataManager.sqlite_data_manager import SQLiteDataManager

api = Blueprint('api', __name__)


@api.route('/users', methods=['GET'])
def get_users():
    users = SQLiteDataManager.list_all_users()
    return jsonify(users)


@api.route('/users/<user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    movies = SQLiteDataManager.get_user_movies(user_id)
    return jsonify(movies)


@api.route('/users/<user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    # Parse the movie data from the request (e.g., using request.json)
    movie_data = request.json

    # Check if the required fields are present in the request
    if not movie_data or 'title' not in movie_data:
        return jsonify({'error': 'Invalid request data'}), 400

    # Get the movie title from the request data
    movie_title = movie_data['title']

    # Add the movie to the user's list using data_manager.add_movie
    error_message = SQLiteDataManager.add_movie(user_id, movie_title)

    if error_message:
        return jsonify({'error': error_message}), 400

    # Return a success message
    return jsonify({'message': 'Movie added successfully'}), 201
