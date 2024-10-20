from telegram.ext import (
    Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
)
from handlers import start_handler, game_handler, join_handler, admin_handler, error_handler

def main():
    updater = Updater(token="YOUR_BOT_TOKEN", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_handler.start_handler))
    dispatcher.add_handler(CommandHandler("game", game_handler.game_handler))
    dispatcher.add_handler(CommandHandler("forcestart", admin_handler.force_start_handler))
    dispatcher.add_handler(CallbackQueryHandler(game_handler.join_game_handler, pattern="join"))
    dispatcher.add_error_handler(error_handler.error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
