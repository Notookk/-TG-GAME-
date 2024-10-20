from telegram import Update
from telegram.ext import CallbackContext
from utils.player_manager import player_manager

def players_handler(update: Update, context: CallbackContext):
    if player_manager.players:
        message = "Joined Players:\n"
        for player_id, name in player_manager.players.items():
            message += f"[{name}](tg://user?id={player_id})\n"
        update.message.reply_text(message, parse_mode="Markdown")
    else:
        update.message.reply_text("No players have joined yet.")
