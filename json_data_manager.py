import json
import requests
from data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, json_file):
        self.json_file = json_file

    def _load_data(self):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
        return data['users']  # Return the list of users directly

    def _write_data(self, data):
        with open(self.json_file, 'w') as file:
            json.dump({'users': data},
                      file)  # Write the list of users wrapped in a dictionary

    def list_all_users(self):
        data = self._load_data()
        return data

    def get_user_movies(self, user_id):
        data = self._load_data()
        for user in data:
            if user['user_id'] == user_id:
                return user['movies']
        return []

    def add_movie(self, user_id, name, director, year, rating):
        data = self._load_data()
        for user in data:
            if user['user_id'] == user_id:
                movie = {
                    'name': name,
                    'director': director,
                    'year': year,
                    'rating': rating,
                    'id': len(user['movies']) + 1
                }
                user['movies'].append(movie)
                break
        self._write_data(data)

    def get_movie(self, user_id, movie_id):
        user_id = str(user_id)  # Convert user_id to string
        movie_id = str(movie_id)  # Convert movie_id to string
        data = self._load_data()
        for user in data:
            if user['user_id'] == user_id:
                for movie in user['movies']:
                    if movie['id'] == movie_id:
                        return movie
        return None

    def update_movie(self, user_id, movie_id, updated_movie):
        user_id = str(user_id)  # Convert user_id to string
        movie_id = int(movie_id)  # Convert movie_id to integer
        data = self._load_data()
        for user in data:
            if user['user_id'] == user_id:
                for movie in user['movies']:
                    if movie['id'] == movie_id:
                        movie.update(updated_movie)
                        self._write_data(
                            data)  # Save updated data back to source
                        return  # Exit the function after saving data
        return  # Exit the function if no matching movie is found

    def delete_movie(self, user_id, movie_id):
        user_id = str(user_id)  # Convert user_id to string
        movie_id = int(movie_id)  # Convert movie_id to integer
        data = self._load_data()
        for user in data:
            if user['user_id'] == user_id:
                user['movies'] = [movie for movie in user['movies']
                                  if movie['id'] != movie_id]
                break
        self._write_data(data)
