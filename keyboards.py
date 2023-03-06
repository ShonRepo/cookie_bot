from aiogram.utils.callback_data import CallbackData

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

predictions_callback = CallbackData('prediction', 'page', 'lang', 'action')

def generate_page_buttons(current_page, lang, next_page):
    inline_buttons = InlineKeyboardMarkup()

    if current_page > 0:
        inline_buttons.add(InlineKeyboardButton('Назад',
                                                callback_data=predictions_callback.new(page=current_page - 1,
                                                                                       lang=lang,
                                                                                       action='undo_page')))

    if next_page:
        inline_buttons.add(InlineKeyboardButton('Вперед',
                                                callback_data=predictions_callback.new(page=current_page + 1,
                                                                                       lang=lang,
                                                                                       action='redo_page')))

    return inline_buttons
