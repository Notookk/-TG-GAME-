from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from utils.config import BOT_TOKEN
from handlers.game_handler import (
    start_handler, game_handler, forcestart_handler, category_selection_handler
)
from handlers.player_handler import players_handler

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler("start", start_handler))
    dp.add_handler(CommandHandler("game", game_handler))
    dp.add_handler(CommandHandler("forcestart", forcestart_handler))
    dp.add_handler(CommandHandler("players", players_handler))
    dp.add_handler(CallbackQueryHandler(category_selection_handler, pattern="^category_"))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
