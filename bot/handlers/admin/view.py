from telegram import (
    InlineKeyboardButton,
    ReplyKeyboardMarkup
)

__stage = [i for i in range(3)]

__main_menu = [
      ['Создать предложение', 'Удалить предложениe'],
      ['Просмотр предложений']
]

back_button = "⬅️ Назад в главное меню"

main_keyboard = ReplyKeyboardMarkup(__main_menu, resize_keyboard=True)
back_menu = ReplyKeyboardMarkup([[back_button]], resize_keyboard=True, one_time_keyboard=True)

def letter_buttons(letters: dict):
    letters_keybord = []

    for i , letter in enumerate(letters.keys()):
            letters_keybord.append([InlineKeyboardButton(letter, callback_data=str(i))])

    return letters_keybord