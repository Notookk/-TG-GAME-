import random
import os

class WordLoader:
    def __init__(self, word_directory="words/"):
        """Initializes the WordLoader with the directory containing word files."""
        self.word_directory = word_directory

    def load_words(self, category):
        """Loads word pairs from the given category file."""
        file_path = os.path.join(self.word_directory, f"{category}.txt")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                word_pairs = [line.strip().split(" : ") for line in file]
                return word_pairs
        except FileNotFoundError:
            raise ValueError(f"No word file found for category: {category}")

    def get_random_word_pair(self, category):
        """Fetches a random word pair from the chosen category."""
        word_pairs = self.load_words(category)
        return random.choice(word_pairs)

    def get_random_category(self):
        """Randomly selects a category from available ones."""
        categories = ["sports", "food", "animal", "professions"]
        return random.choice(categories)
