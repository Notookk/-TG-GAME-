from utils.logger import logger
from datetime import datetime, timedelta

class PlayerManager:
    def __init__(self):
        self.players = {}  # {user_id: username}
        self.game_active = False
        self.game_start_time = None  # Tracks when the game started
        self.TIMEOUT = timedelta(minutes=5)  # 5-minute join window

    def add_player(self, user_id, username):
        """Add a player to the game if not already joined."""
        if user_id in self.players:
            logger.warning(f"User {username} (ID: {user_id}) tried to join again.")
            return False  # Player already joined

        self.players[user_id] = username
        logger.info(f"Player added: {username} (ID: {user_id})")

        # Automatically set game start time on the first player join
        if len(self.players) == 1:
            self.game_start_time = datetime.now()
            logger.info(f"Game join window started at {self.game_start_time}.")
        
        return True

    def remove_player(self, user_id):
        """Remove a player from the game."""
        if user_id in self.players:
            username = self.players.pop(user_id)
            logger.info(f"Player removed: {username} (ID: {user_id})")
        else:
            logger.warning(f"Tried to remove non-existent player with ID: {user_id}")

    def get_player_list(self):
        """Returns the current list of players in Markdown format."""
        if not self.players:
            logger.info("No players have joined yet.")
            return ["No players have joined."]
        return [f"[{username}](tg://user?id={user_id})" for user_id, username in self.players.items()]

    def player_count(self):
        """Returns the total number of players."""
        return len(self.players)

    def is_game_active(self):
        """Check if the game is currently active."""
        return self.game_active

    def start_game(self):
        """Starts the game if enough players are present."""
        if self.player_count() < 6:
            logger.error("Cannot start game: Not enough players (min 6 required).")
            return False

        self.game_active = True
        logger.info("Game started successfully.")
        return True

    def force_start_game(self, is_admin):
        """Allows only admins to force-start the game, even with fewer players."""
        if not is_admin:
            logger.warning("Unauthorized user attempted to force-start the game.")
            return False

        self.game_active = True
        logger.info("Game forcefully started by admin.")
        return True

    def end_game(self):
        """Ends the game and clears the player list."""
        self.players.clear()
        self.game_active = False
        self.game_start_time = None
        logger.info("Game ended, and player list cleared.")

    def check_timeout(self):
        """Checks if the join window has expired."""
        if self.game_start_time and datetime.now() > self.game_start_time + self.TIMEOUT:
            logger.info("Game join window expired. Cancelling the game.")
            self.end_game()
            return True
        return False
