from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.game_manager import game_manager
from utils.config import CATEGORIES

def start_handler(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Use /game to start a game.")

def game_handler(update: Update, context: CallbackContext):
    if game_manager.game_in_progress:
        update.message.reply_text("A game is already in progress.")
    else:
        keyboard = [[InlineKeyboardButton(cat.capitalize(), callback_data=f"category_{cat}") for cat in CATEGORIES]]
        update.message.reply_text("Choose a category:", reply_markup=InlineKeyboardMarkup(keyboard))

def forcestart_handler(update: Update, context: CallbackContext):
    if not game_manager.game_in_progress:
        update.message.reply_text("No game in progress to force start.")
    else:
        game_manager.assign_roles()
        update.message.reply_text("Game forcibly started!")

def category_selection_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    category = query.data.split("_")[1]
    game_manager.start_game(category)
    query.edit_message_text(f"Category selected: {category.capitalize()}")
