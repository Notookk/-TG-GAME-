from utils.word_loader import load_random_pair
from utils.player_manager import player_manager
from utils.logger import logger
import random

class GameManager:
    def __init__(self):
        self.spy = None
        self.category = None
        self.game_in_progress = False

    def start_game(self, category):
        self.category = category
        self.game_in_progress = True
        self.assign_roles()

    def assign_roles(self):
        players = list(player_manager.players.keys())
        self.spy = random.choice(players)
        spy_word, player_word = load_random_pair(self.category)

        for player_id in players:
            word = spy_word if player_id == self.spy else player_word
            player_manager.send_message(player_id, f"Your word: {word}")

    def end_game(self):
        self.game_in_progress = False
        self.category = None
        player_manager.end_game()
