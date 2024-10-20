import random
from utils.player_manager import player_manager
from utils.logger import logger

class GameManager:
    def __init__(self):
        self.words = {}
        self.votes = {}
        self.spy = None
        self.game_in_progress = False

    def start_game(self):
        self.game_in_progress = True
        logger.info("Game started.")
        self.assign_roles()

    def assign_roles(self):
        players = list(player_manager.players.keys())
        self.spy = random.choice(players)

        word_pair = self.get_random_word_pair()
        spy_word, player_word = word_pair

        # Send individual word assignments via DM to keep them secret
        for player_id in players:
            word = spy_word if player_id == self.spy else player_word
            player_manager.send_message(player_id, f"Your word: {word}")

        logger.info(f"Spy assigned: {player_manager.players[self.spy]}")

    def get_random_word_pair(self):
        """Load a random word pair."""
        from utils.word_loader import load_random_pair
        return load_random_pair()

    def vote_player(self, voter_id, voted_id):
        if not self.game_in_progress:
            return "⚠️ No game in progress."

        if voter_id not in player_manager.players:
            return "🚫 You are not part of the game."

        self.votes[voter_id] = voted_id
        return f"✅ You voted for {player_manager.players[voted_id]}."

    def check_game_over(self):
        if len(self.votes) == len(player_manager.players):
            result = self.evaluate_votes()
            self.end_game()
            return result
        return None

    def evaluate_votes(self):
        votes_count = {}
        for voted_id in self.votes.values():
            votes_count[voted_id] = votes_count.get(voted_id, 0) + 1

        most_voted = max(votes_count, key=votes_count.get)
        if most_voted == self.spy:
            return f"🎉 Players win! The spy was {player_manager.players[self.spy]}."
        return f"😈 The spy wins! {player_manager.players[self.spy]} fooled everyone."

    def end_game(self):
        self.game_in_progress = False
        self.words.clear()
        self.votes.clear()
        self.spy = None
        player_manager.end_game()
        logger.info("Game e
