from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.player_manager import PlayerManager
from utils.game_manager import GameManager
from utils.logger import logger

player_manager = PlayerManager()
game_manager = GameManager()

GAME_START_TEXT = "A new game is starting! Click below to join."
GAME_CANCEL_TEXT = "Game canceled due to insufficient players (min 6 required)."
PLAYER_LIST_TEXT = "Current Players:\n\n{}"
JOIN_SUCCESS_TEXT = "You have successfully joined the game!"
ALREADY_JOINED_TEXT = "You have already joined the game."

async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /game command to start a new game."""
    logger.info("Received /game command.")
    player_manager.end_game()  # Reset any ongoing game

    keyboard = [
        [InlineKeyboardButton("Join Game", callback_data="join_game")],
        [InlineKeyboardButton("View Players", callback_data="view_players")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(GAME_START_TEXT, reply_markup=reply_markup)

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback for joining a game."""
    user = update.effective_user
    if player_manager.add_player(user.id, user.username):
        await update.callback_query.answer(JOIN_SUCCESS_TEXT)
    else:
        await update.callback_query.answer(ALREADY_JOINED_TEXT)

async def players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback to view the list of players."""
    player_list = "\n".join(player_manager.get_player_list())
    await update.callback_query.answer()
    await update.callback_query.message.edit_text(PLAYER_LIST_TEXT.format(player_list))

# Handlers for the /game command and joining via buttons
game_handler = game
join_handler = join
players_handler = players
