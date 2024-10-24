from telegram import Update
from telegram.ext import CallbackContext
from utils.player_manager import player_manager
from utils.logger import logger

async def forcestart(update: Update, context: CallbackContext):
    """Force start the game if the user is admin and enough players have joined."""
    chat_id = update.effective_chat.id
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name

    # Check if the user is an admin
    member = await context.bot.get_chat_member(chat_id, user_id)
    if member.status not in ("administrator", "creator"):
        await update.message.reply_text(
            f"[{username}](tg://user?id={user_id}), only admins can use /forcestart.",
            parse_mode="Markdown"
        )
        logger.warning(f"User {username} tried to use /forcestart but isn't an admin.")
        return

    # Check if enough players have joined
    if player_manager.player_count() < 6:
        await update.message.reply_text("At least 6 players are required to start the game!")
        logger.info("Not enough players to start the game.")
        return

    # Start the game
    if player_manager.start_game():
        await update.message.reply_text("The game has started! 🎮")
        logger.info("Game started by an admin.")
