from .player_manager import PlayerManager
from .game_manager import GameManager
from .word_loader import WordLoader
from .logger import logger

# Initialize the utility classes
player_manager = PlayerManager()
game_manager = GameManager()
word_loader = WordLoader()

__all__ = [
    "player_manager",
    "game_manager",
    "word_loader",
    "logger"
]
