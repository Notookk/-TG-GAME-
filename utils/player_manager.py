class PlayerManager:
    def __init__(self):
        self.players = {}
        self.game_active = False

    def add_player(self, user_id, username):
        if user_id in self.players:
            return False  # Already joined
        self.players[user_id] = username
        return True

    def remove_player(self, user_id):
        self.players.pop(user_id, None)

    def get_player_list(self):
        return [f"[{username}](tg://user?id={user_id})" for user_id, username in self.players.items()]

    def player_count(self):
        return len(self.players)

    def is_game_active(self):
        return self.game_active

    def start_game(self):
        self.game_active = True

    def end_game(self):
        self.players.clear()
        self.game_active = False
