from telegram.ext import CallbackContext
from utils.player_manager import player_manager
from utils.logger import logger

def reminder_callback(context: CallbackContext):
    chat_id = context.job.context
    player_count = player_manager.player_count()
    if player_count < 6:
        context.bot.send_message(chat_id, f"⚠️ Only {player_count} players joined. Waiting for more!")
    else:
        context.job.schedule_removal()

def schedule_reminder(job_queue, chat_id, interval):
    job_queue.run_repeating(reminder_callback, interval=interval, context=chat_id)

def cancel_game_callback(context: CallbackContext):
    chat_id = context.job.context
    player_manager.end_game()
    context.bot.send_message(chat_id, "❌ Game canceled. Not enough players joined.")

def schedule_game_cancellation(job_queue, chat_id, timeout):
    job_queue.run_once(cancel_game_callback, timeout, context=chat_id)
