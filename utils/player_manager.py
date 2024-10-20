from utils.logger import logger

class PlayerManager:
    def __init__(self):
        self.players = {}  # Stores player data as {user_id: username}
        self.game_active = False

    def add_player(self, user_id, username):
        """Add a player to the game if not already joined."""
        if user_id in self.players:
            logger.warning(f"User {username} (ID: {user_id}) tried to join again.")
            return False  # Player already joined
        self.players[user_id] = username
        logger.info(f"Player added: {username} (ID: {user_id})")
        return True

    def remove_player(self, user_id):
        """Remove a player from the game."""
        if user_id in self.players:
            username = self.players.pop(user_id)
            logger.info(f"Player removed: {username} (ID: {user_id})")
        else:
            logger.warning(f"Attempted to remove non-existent player with ID: {user_id}")

    def get_player_list(self):
        """Returns a list of players in Markdown format."""
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
        """Starts the game if the minimum player requirement is met."""
        if self.player_count() < 6:
            logger.error("Cannot start game: Not enough players (min 6 required).")
            return False
        self.game_active = True
        logger.info("Game started successfully.")
        return True

    def end_game(self):
        """Ends the game and resets the player list."""
        self.players.clear()
        self.game_active = False
        logger.info("Game ended, and player list cleared.")
