from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    filters,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
)

from telegram import (
    InlineKeyboardMarkup,
    Update,
)

from handlers.admin import view 

from util.my_db import JsonDB


START_ROUTES, INPUT_LETTER, INPUT_ANSWER, DELETE= range(4)


async def __admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text='Выберете дейсвие', reply_markup=view.main_keyboard)

    return START_ROUTES


async def __view_letters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    letters = JsonDB.get_dict_from_db()
    reply_markup = view.main_keyboard

    if not letters:
        await update.message.reply_text(text="Нет созданных предложений\nВыберете действие:", 
                                      reply_markup=reply_markup)
    else:
        letter_answer = JsonDB.dict_to_str(letters)
        await update.message.reply_text('Ваши предложения: {предложение}: {ответ}')
        await update.message.reply_text('\n'.join(letter_answer), reply_markup=reply_markup)
    
    return START_ROUTES


async def __create_letter_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text='Напишите предложение', reply_markup=view.back_menu)
    return INPUT_LETTER


async def __input_letter(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    user_data = context.user_data
    letter = update.message.text
    
    user_data['letter'] = letter
    await update.message.reply_text(text='Напишите ответ', reply_markup=view.back_menu)

    return INPUT_ANSWER


async def __input_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    answer = update.message.text 
    letter = user_data['letter']

    if answer == view.back_button:
        user_data.clear()
        await update.message.reply_text(f"Действие отмененно\nВыберете действие:",
                                        reply_markup=view.main_keyboard)
        return START_ROUTES
     
    JsonDB.set_letter(letter, answer)
    await update.message.reply_text(f"Предложение и ответ внесенны\nВвыберете действие:",
                                     reply_markup=view.main_keyboard)
    return START_ROUTES


async def __choice_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    letters = JsonDB.get_dict_from_db()

    if not letters:
        await update.message.reply_text(text="Нет созданных предложений\nВыберете действие:", 
                                        reply_markup=view.main_keyboard)
        return START_ROUTES
    
    reply_markup = InlineKeyboardMarkup(view.letter_buttons(letters=letters))
    
    await update.message.reply_text(f"Выберите предложение для удаления", reply_markup=reply_markup)
    return DELETE


async def __delete_letter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    id_letter = int(query.data)
    
    JsonDB.delete_letter(id_letter)
    await query.edit_message_text(f"Предложение удаленно")

    return START_ROUTES


def admin_panel() -> ConversationHandler:

    admin_handlers = ConversationHandler(
        entry_points=[CommandHandler('admin_panel', __admin_panel)],
        states={
            START_ROUTES: [
                MessageHandler(filters.Regex("^(Создать)"), __create_letter_menu),
                MessageHandler(filters.Regex("^(Удалить)"), __choice_delete),
                MessageHandler(filters.Regex("^(Просмотр)"), __view_letters),
            ],
            INPUT_LETTER: [
                MessageHandler(filters.Regex(view.back_button), __admin_panel),
                MessageHandler(filters.TEXT, __input_letter)
            ],
            INPUT_ANSWER:[
                MessageHandler(filters.TEXT, __input_answer)
            ],
            DELETE:{
                CallbackQueryHandler(__delete_letter)
            }
        },
        fallbacks=[]
    )

    return admin_handlers