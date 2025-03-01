from telegram import Update
from telegram.ext import CallbackContext

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from dotenv import dotenv_values

from telethon import TelegramClient

from util.my_db import JsonDB


api_id = dotenv_values(".env").get('API_ID')
api_hash = dotenv_values(".env").get('API_HASH')


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

            client = TelegramClient('defsefs', api_id, api_hash)
            client.start()
            chat_id = update.message.chat_id
            async with client:
                await client.send_message(chat_id, response, reply_to=update.message.message_id)


            # await update.message.reply_text(response)

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