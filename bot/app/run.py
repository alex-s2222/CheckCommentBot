from dotenv import dotenv_values

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from handlers.answer_comment import Comment as chat
from handlers import self_bot as bot


def run_bot():
    TOKEN = dotenv_values(".env").get('TG_TOKEN')
    
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(MessageHandler(filters.REPLY, chat.comment_handler))

    app.run_polling()


if __name__ == '__main__':
    run_bot()