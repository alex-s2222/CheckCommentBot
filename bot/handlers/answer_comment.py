from telegram import Update
from telegram.ext import CallbackContext

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from util.my_db import JsonDB


class Comment:
    @staticmethod
    async def comment_handler(update: Update, context: CallbackContext) -> None:
        # Проверяем, является ли сообщение комментарием
        if update.message.reply_to_message:
            original_message = update.message.text
            answer = Comment.__get_answer(original_message)
            if not answer:
                return None
            
            response = f'{answer}'
            await update.message.reply_text(response)

    @staticmethod
    def __get_answer(user_message: str):
        db_data = JsonDB.get_dict_from_db()
        if not db_data:
            return None

        #WRatio второй способ
        #token_set_ratio
        best_match, score = process.extractOne(user_message, db_data.keys(), scorer=fuzz.WRatio)
        if score < 80:
            return None 
        
        return db_data[best_match] 