import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GAME_TIMEOUT = int(os.getenv("GAME_TIMEOUT", 300))  # 5 minutes default
REMINDER_INTERVAL = int(os.getenv("REMINDER_INTERVAL", 120))  # Remind every 2 minutes
MIN_PLAYERS = int(os.getenv("MIN_PLAYERS", 6))
LOG_FILE = "bot.log"
