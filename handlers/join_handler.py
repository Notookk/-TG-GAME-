from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.player_manager import player_manager
from utils.logger import logger

async def join_callback(update: Update, context: CallbackContext):
    """Handles the Join button callback."""
    query = update.callback_query
    user = query.from_user
    username = user.username or user.first_name
    user_id = user.id
    chat_id = query.message.chat_id

    # Check if the user accessed the bot via a deep link
    if not context.args:
        deep_link_url = f"https://t.me/{context.bot.username}?start=join_{chat_id}"
        await query.answer(
            "Click the button below to start the bot and join the game.",
            show_alert=True
        )
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Start & Join", url=deep_link_url)]])
        await context.bot.send_message(chat_id=chat_id, text="Click to join:", reply_markup=keyboard)
        return

    # Add player to the game and announce in the group
    if player_manager.add_player(user_id, username):
        announcement = f"🎉 [{username}](tg://user?id={user_id}) has joined the game!"
        await context.bot.send_message(chat_id=chat_id, text=announcement, parse_mode="Markdown")
        logger.info(f"User {username} joined the game.")
    else:
        await query.answer("You’ve already joined the game!", show_alert=True)

    await query.answer()
