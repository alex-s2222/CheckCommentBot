from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext



async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я бот, который отвечает на комментарии.', reply_markup=ReplyKeyboardRemove())
