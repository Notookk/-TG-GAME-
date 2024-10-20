from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils import player_manager, game_manager, word_loader
import random

# Voting categories
CATEGORIES = ["Sports", "Food", "Animal", "Professions", "Random"]

async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the game and presents category voting."""
    keyboard = [
        [InlineKeyboardButton(category, callback_data=category.lower()) for category in CATEGORIES]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Vote for a category:", reply_markup=reply_markup)

async def category_vote_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles category voting and assigns words."""
    query = update.callback_query
    await query.answer()

    selected_category = query.data

    if selected_category == "random":
        selected_category = word_loader.get_random_category()

    game_manager.category = selected_category
    await query.edit_message_text(f"Category chosen: {selected_category.capitalize()}")

    # Distribute words to players
    await distribute_words(context)

async def distribute_words(context: ContextTypes.DEFAULT_TYPE):
    """Distributes words to players in private chat."""
    players = player_manager.players
    spy = random.choice(list(players.keys()))  # Randomly select the spy

    # Get a random word pair
    word_pair = word_loader.get_random_word_pair(game_manager.category)
    normal_word, spy_word = word_pair

    # Send words to each player in private chat
    for user_id in players:
        word = spy_word if user_id == spy else normal_word
        await context.bot.send_message(
            chat_id=user_id,
            text=f"Your word is: *{word}*",
            parse_mode="Markdown"
        )

    game_manager.spy = spy
    await announce_players(context)

async def announce_players(context: ContextTypes.DEFAULT_TYPE):
    """Announces the list of joined players."""
    player_list = player_manager.get_player_list()
    await context.bot.send_message(
        chat_id=game_manager.group_chat_id,
        text="Players:\n" + "\n".join(player_list),
        parse_mode="Markdown"
    )
