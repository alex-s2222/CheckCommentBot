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

from util.my_db import DB 

START_ROUTES, INPUT_DATA = range(2)


async def __admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text='Выберете дейсвие', reply_markup=view.main_keyboard)

    return START_ROUTES


async def __view_letters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    letters = await DB.get_letters()
    reply_markup = view.main_keyboard

    if not letters:
        await update.message.reply_text(text="Нет созданных предложений\nВыберете действие:", 
                                      reply_markup=reply_markup)
    else:
        await update.message.reply_text('\n'.join(letters), reply_markup=reply_markup)
    
    return START_ROUTES


async def __create_letter_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text='Напишите предложение', reply_markup=view.back_menu)
    return INPUT_DATA


async def __insert_letter(update: Update, context: ContextTypes.DEFAULT_TYPE):

    letter = update.message.text
    
    await DB.write_letter(letter)
    await update.message.reply_text(text='Успешно!')
    await update.message.reply_text(text='Выберете дейсвие', reply_markup=view.main_keyboard)
    
    return START_ROUTES


async def __delete_letter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    letters = await DB.get_letters()

    if not letters:
        await update.message.reply_text(text="Нет созданных предложений\nВыберете действие:", 
                                      reply_markup=view.main_keyboard)
        return START_ROUTES
    
    reply_markup = InlineKeyboardMarkup(view.letter_buttons(letters=letters))
    
    await update.message.reply_text(f"Выберите предложение для удаления", reply_markup=reply_markup)
    return DELETE




def admin_panel() -> ConversationHandler:
    ONE, TWO, THREE = range(3)

    admin_handlers = ConversationHandler(
        entry_points=[CommandHandler('admin_panel', __admin_panel)],
        states={
            START_ROUTES: [
                MessageHandler(filters.Regex("^(Создать)"), __create_letter_menu),
                MessageHandler(filters.Regex("^(Удалить)"), __delete_letter),
                MessageHandler(filters.Regex("^(Просмотр)"), __view_letters),
            ],
            
            INPUT_DATA: [
                MessageHandler(filters.Regex("⬅️ Назад в главное меню"), __admin_panel),
                MessageHandler(filters.TEXT, __insert_letter)
            ],
        },
        fallbacks=[]
    )

    return admin_handlers