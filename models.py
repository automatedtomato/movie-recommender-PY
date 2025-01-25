import csv
import re

class Movie:
    def __init__(self, title, genres, description, release_year, rating):

        # Basic validation
        if not title:
            raise ValueError("Title cannot be empty")

        if release_year < 1888 or release_year > 2025:
            raise ValueError(f"Invalid release year: {release_year}")

        if rating < 0 or rating > 10:
            raise ValueError(f"Invalid rating: {rating}")

        if len(genres) == 0:
            raise ValueError(f"Movie must have at least one genre")

        self.title = title
        self.genres = genres
        self.description = description
        self.release_year = release_year
        self.rating = rating

    def __str__(self):
       return f"Title: {self.title}\nGenres: {', '.join(self.genres)}\nDescription: {self.description}\nRelease Year: ({self.release_year}\nRating: {self.rating}"

    def to_genre_vector(self):
        # List of all possible genres
        all_genres = [
            "Action", "Comedy", "Drama",
            "Sci-Fi", "Horror", "Romance",
            "Animation", "Documentary"
        ]

        # Create a vector with 0s and 1s
        genre_vector = [0] * len(all_genres)

        # Mark genres that exist in the movie
        for i, genre in enumerate(all_genres):
            if genre in self.genres:
                genre_vector[i] = 1

        return genre_vector

def load_movies(filename):
    movies = []
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            try:
                movie = Movie(
                    title = row[0],
                    genres = row[1].split(','),
                    description = row[2],
                    release_year = int(row[3]),
                    rating = float(row[4])
                )
                movies.append(movie)
            except ValueError as e:
                print(f"Error loading movie: {e}")
    return movies