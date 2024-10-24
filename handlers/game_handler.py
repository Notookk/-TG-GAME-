from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ContextTypes
from utils.player_manager import PlayerManager
from utils.game_manager import GameManager
from utils.logger import logger

player_manager = PlayerManager()
game_manager = GameManager()

# Game messages
GAME_START_TEXT = "A new game is starting! Click below to join."
GAME_CANCEL_TEXT = "Game canceled due to insufficient players (min 6 required)."
PLAYER_LIST_TEXT = "Current Players:\n\n{}"
JOIN_SUCCESS_TEXT = "You have successfully joined the game, {}!"
ALREADY_JOINED_TEXT = "You are already in the game!"
FORCE_START_ERROR_TEXT = (
    "Minimum 6 players are required to start the game. Current players: {}"
)
FORCE_START_ADMIN_ONLY = "Only admins can use the /forcestart command, {}."

# Pinned message tracker
pinned_message_id = None

async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /game command to start a new game."""
    logger.info("Received /game command.")
    player_manager.end_game()  # Reset any ongoing game

    keyboard = [
        [InlineKeyboardButton("Join Game", callback_data="join_game")],
        [InlineKeyboardButton("View Players", callback_data="view_players")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = await update.message.reply_text(GAME_START_TEXT, reply_markup=reply_markup)

    # Pin the message in the group
    global pinned_message_id
    pinned_message_id = message.message_id
    await update.message.chat.pin_message(pinned_message_id)

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback for joining a game."""
    user = update.effective_user
    chat = update.effective_chat

    if player_manager.add_player(user.id, user.username):
        await update.callback_query.answer(JOIN_SUCCESS_TEXT.format(user.full_name))

        # Announce in the group that the player has joined
        join_announcement = f"[{user.full_name}](tg://user?id={user.id}) has joined the game!"
        await context.bot.send_message(chat_id=chat.id, text=join_announcement, parse_mode="Markdown")
    else:
        await update.callback_query.answer(ALREADY_JOINED_TEXT)

async def view_players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback to view the list of players."""
    player_list = "\n".join(player_manager.get_player_list())
    await update.callback_query.answer()
    await update.callback_query.message.edit_text(PLAYER_LIST_TEXT.format(player_list))

async def forcestart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /forcestart command to forcefully start the game."""
    user = update.effective_user
    chat = update.effective_chat

    # Check if the user is an admin
    member = await chat.get_member(user.id)
    if not member.status in ("administrator", "creator"):
        await update.message.reply_text(FORCE_START_ADMIN_ONLY.format(user.full_name))
        return

    # Ensure enough players have joined
    if player_manager.player_count() < 6:
        await update.message.reply_text(
            FORCE_START_ERROR_TEXT.format(player_manager.player_count())
        )
        return

    if player_manager.start_game():
        await update.message.reply_text("Game is starting!")
    else:
        await update.message.reply_text("Game could not be started.")

async def end_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ends the game and unpins the pinned message."""
    global pinned_message_id
    player_manager.end_game()

    await update.message.reply_text("Game has ended and reset.")
    if pinned_message_id:
        await context.bot.unpin_chat_message(update.effective_chat.id, pinned_message_id)
        pinned_message_id = None

# Handlers
game_handler = game
join_handler = join
players_handler = view_players
forcestart_handler = forcestart
endgame_handler = end_game
