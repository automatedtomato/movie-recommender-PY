import math
import re

def preprocess(text):

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation using regex
    text = re.sub(r'[^\w\s]', '', text)

    # Split into words and remove empty strings
    return [word for word in text.split() if word]

def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def magnitude(v):
    return math.sqrt(sum(x * x for x in v))

def genre_similarity(movie1, movie2):
    v1 = movie1.to_genre_vector()
    v2 = movie2.to_genre_vector()

    dot = dot_product(v1, v2)
    mag1 = magnitude(v1)
    mag2 = magnitude(v2)

    if mag1 == 0 or mag2 == 0:
        return 0

    return dot / (mag1 * mag2)

def calculate_term_frequency(words):
    # Count word occurrences
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1

    # Calculate term frequency
    total_words = len(words)
    term_frequency = {}
    for word, count in word_counts.items():
        term_frequency[word] = count / total_words

    return term_frequency

def calculate_idf(all_documents):
    total_documents = len(all_documents)
    word_document_counts = {}

    for document in all_documents:
        unique_words = set(document)
        for word in unique_words:
            word_document_counts[word] = word_document_counts.get(word, 0) + 1

    idf_scores = {}
    for word, document_count in word_document_counts.items():
        idf_scores[word] = math.log(total_documents / document_count)

    return idf_scores


def calculate_tfidf(movies):
    # Preprocess movie descriptions
    preprocessed_doc = [preprocess(movie.description) for movie in movies]

    # Calculate IDF for each word first
    idf_scores = calculate_idf(preprocessed_doc)

    # Calculate TF for each word in each document
    tfidf_vectors = {}

    for i, document in enumerate(preprocessed_doc):
        movie_title = movies[i].title

        # Calculate TF
        tf_scores = calculate_term_frequency(document)

        tfidf_vector = {}
        for word, tf in tf_scores.items():
            # Debugging print
            idf = idf_scores.get(word, 0)
            tfidf_value = tf * idf
            tfidf_vector[word] = tfidf_value

        tfidf_vectors[movie_title] = tfidf_vector

    return tfidf_vectors


def cosine_similarity(v1, v2):
    dot_product = 0.0
    for word, tfidf in v1.items():
        dot_product += tfidf * v2.get(word, 0)  # Use .get() with default 0

    mag1 = math.sqrt(sum(val*val for val in v1.values()))
    mag2 = math.sqrt(sum(val*val for val in v2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0

    return dot_product / (mag1 * mag2)