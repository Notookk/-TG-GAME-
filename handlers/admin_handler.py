from telegram import Update
from telegram.ext import ContextTypes
from utils.player_manager import player_manager
from utils.logger import logger

FORCE_START_TEXT = "Game forcefully started by admin."
NOT_ADMIN_TEXT = "Only admins can use /forcestart!"
GAME_NOT_STARTED_TEXT = "Not enough players to start the game."

async def force_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin-only command to force start the game."""
    user = update.effective_user
    if not user.get_admin_rights():
        await update.message.reply_text(NOT_ADMIN_TEXT)
        return

    if player_manager.force_start_game(is_admin=True):
        await update.message.reply_text(FORCE_START_TEXT)
    else:
        await update.message.reply_text(GAME_NOT_STARTED_TEXT)

force_start_handler = force_start
