from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from handlers import (
    start_handler, game_handler, join_handler, players_handler, force_start_handler
)
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

TOKEN = "YOUR_BOT_TOKEN"

# Create the bot application
app = ApplicationBuilder().token(TOKEN).build()

# Register command handlers
app.add_handler(CommandHandler("start", start_handler))
app.add_handler(CommandHandler("game", game_handler))
app.add_handler(CommandHandler("forcestart", force_start_handler))

# Register callback query handlers for buttons
app.add_handler(CallbackQueryHandler(join_handler, pattern="join_game"))
app.add_handler(CallbackQueryHandler(players_handler, pattern="view_players"))

# Start the bot
if __name__ == "__main__":
    app.run_polling()
