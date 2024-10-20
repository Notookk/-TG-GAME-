import random
import os

BASE_PATH = os.path.dirname(__file__)
WORDS_FOLDER = os.path.join(BASE_PATH, "words")

def load_words_from_file(category):
    """Loads word pairs from the given category file."""
    file_path = os.path.join(WORDS_FOLDER, f"{category}.txt")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No word file found for category: {category}")

    with open(file_path, 'r') as f:
        pairs = [line.strip().split(" : ") for line in f if " : " in line]
    return pairs

def load_random_pair(category):
    """Select a random word pair from the chosen category."""
    try:
        word_pairs = load_words_from_file(category)
        return random.choice(word_pairs)
    except Exception as e:
        print(f"Error loading words: {e}")
        # Fallback to a default pair if the category is unavailable
        return ("Error", "Fallback")
