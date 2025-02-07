from telegram import (
    InlineKeyboardButton,
    ReplyKeyboardMarkup
)

__stage = [i for i in range(3)]

main_menu = [
      ['Создать предложение', 'Удалить предложениe'],
      ['Просмотр предложений']
]

main_keyboard = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
back_menu = ReplyKeyboardMarkup([['⬅️ Назад в главное меню']], resize_keyboard=True, one_time_keyboard=True)

def letter_buttons(letters):
    letters_keybord = []

    for i , letter in enumerate(letters):
            letters_keybord.append([InlineKeyboardButton(letter, callback_data=str(i))])

    return letters_keybord