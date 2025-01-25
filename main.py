from models import load_movies, Movie
from similarity import genre_similarity, calculate_tfidf, cosine_similarity


def main():
    print('Movie recommender system initialized')
    movies = load_movies('data/movies.csv')

    if not movies:
        print("No movies loaded. Exiting.")
        return

    # Calculate TF-IDF vectors
    tfidf_vectors = calculate_tfidf(movies)

    # Let's analyze "The Matrix" similarities
    matrix = movies[0]
    print(f'\nGenre similarities (cosine-similarity) with {matrix.title}')
    for movie in movies[1:]:
        similarity = genre_similarity(matrix, movie)
        if similarity > 0.5:
            print(f'- {movie.title}: {similarity:.2f}')

    print(f'\nDescription-based similarities (TF-IDF similarity):')
    for movie in movies[1:]:
        desc_similarity = cosine_similarity(
            tfidf_vectors[matrix.title],
            tfidf_vectors[movie.title]
        )
        if desc_similarity > 0:  # Lowered threshold
            print(f'- {movie.title}: {desc_similarity:.2f}')


# Add this to ensure the script runs
if __name__ == "__main__":
    main()