from telegram import Update
from telegram.ext import CallbackContext


class Comment:
    @staticmethod
    async def comment_handler(update: Update, context: CallbackContext) -> None:
        # Проверяем, является ли сообщение комментарием
        if update.message.reply_to_message:
            original_message = update.message.text
            response = f'Спасибо за ваш комментарий на сообщение: "{original_message}"'
            await update.message.reply_text(response)