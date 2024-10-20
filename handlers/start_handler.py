from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.logger import logger

START_TEXT = (
    "Welcome to the Spy Game Bot!\n\n"
    "Use /game to start a new game.\n"
    "Admins can use /forcestart to start forcefully.\n"
    "Players can join via inline buttons."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    logger.info("Received /start command.")
    keyboard = [
        [InlineKeyboardButton("Join Game", callback_data="join_game")],
        [InlineKeyboardButton("View Players", callback_data="view_players")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(START_TEXT, reply_markup=reply_markup)

start_handler = start
