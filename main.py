import os
import typing

from background import keep_alive
from keyboards import generate_page_buttons, predictions_callback

from model.prediction import Prediction

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

bot_token = None

path = "bot_key"
if os.path.isfile(path):
    with open(path, "r") as file:
        bot_token = file.read()

if os.environ.get('bot_key') != None:
    bot_token = os.environ['bot_key']

bot = Bot(bot_token, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot, storage=MemoryStorage())


class State(StatesGroup):
    select_language = State()
    show_predictions = State()
    add_predictions = State()
    remove_predictions = State()


@dp.message_handler(state=State.select_language)
async def process_select_language(message: types.Message):
    await dp.get_current().current_state().update_data(lang=message.text)

    await show_page_prediction(message)


@dp.callback_query_handler(predictions_callback.filter(action='redo_page'), state=State.show_predictions)
async def process_redo_prediction_page(callback_query: types.callback_query, callback_data: typing.Dict[str, str]):
    await dp.get_current().current_state().update_data(lang=callback_data['lang'])

    await show_page_prediction(callback_query, int(callback_data['page']))


@dp.callback_query_handler(predictions_callback.filter(action='undo_page'), state=State.show_predictions)
async def process_undo_prediction_page(callback_query: types.callback_query, callback_data: typing.Dict[str, str]):
    await dp.get_current().current_state().update_data(lang=callback_data['lang'])

    await show_page_prediction(callback_query, int(callback_data['page']))


@dp.message_handler(state=State.show_predictions, commands=['current_lang'])
async def process_show_current_language(message: types.Message):
    data = await dp.get_current().current_state().get_data()

    await bot.send_message(message.from_user.id, 'Язык \"' + data['lang'] + '\" выбран')


@dp.message_handler(state=State.add_predictions, commands=['save'])
async def process_set_prediction_save(message: types.Message):
    data = await dp.get_current().current_state().get_data()

    prediction = await get_prediction()
    prediction.add(data['prediction'])

    await show_page_prediction(message)


@dp.message_handler(state=State.add_predictions, commands=['cancel'])
async def process_set_prediction_cancel(message: types.Message):

    await show_page_prediction(message)


@dp.message_handler(state=State.add_predictions)
async def process_set_prediction_text(message: types.Message):
    print('set_prediction_text')
    await dp.get_current().current_state().update_data(prediction={"title": message.text})

    await bot.send_message(message.from_user.id,
                           'Вы ввели предсказание:\n' + message.text + '\n\nДля сохранения или отмены используйте команды\n/save\n/cancel')


@dp.message_handler(state=State.show_predictions, commands=['add_prediction'])
async def process_add_prediction_command(message: types.Message):
    await State.add_predictions.set()
    await bot.send_message(message.from_user.id, 'Введите предсказание')


@dp.message_handler(state=State.show_predictions, commands=['remove_prediction'])
async def process_remove_prediction_command(message: types.Message):
    await State.remove_predictions.set()
    await bot.send_message(message.from_user.id, 'Введите номер предсказания которое хотите удалить')


@dp.message_handler(state=State.remove_predictions, commands=['remove'])
async def process_set_prediction_save(message: types.Message):
    data = await dp.get_current().current_state().get_data()

    prediction = await get_prediction()
    prediction.delete(data['prediction_id'])

    await show_page_prediction(message)


@dp.message_handler(state=State.remove_predictions, commands=['cancel'])
async def process_set_prediction_cancel(message: types.Message):

    await show_page_prediction(message)


@dp.message_handler(state=State.remove_predictions)
async def process_set_prediction_id_by_remove(message: types.Message):
    msg = 'Введите корректый номер'
    if message.text.isdigit():
        prediction = await get_prediction()
        ids = prediction.ids()
        index = int(message.text)
        if index >= 0 and index < len(ids):
            id = ids[index]

            pr = prediction.find(id)

            await dp.get_current().current_state().update_data(prediction_id=id)
        msg = 'Вы выбрали предскание:\n' + pr['title'] + '\n\nДля удаления или отмены используйте команды\n/remove\n/cancel'

    await bot.send_message(message.from_user.id, msg)


@dp.message_handler(state='*')
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Введите язык')
    await State.select_language.set()


async def get_prediction():
    lang = (await dp.get_current().current_state().get_data())['lang']
    prediction = Prediction(lang)

    return prediction


async def show_page_prediction(message, page=0):
    await dp.get_current().current_state().update_data(page=page)
    lang = (await dp.get_current().current_state().get_data())['lang']

    prediction = await get_prediction()
    await State.show_predictions.set()

    predictions = prediction.all(page)
    await bot.send_message(message.from_user.id,
                           'Язык \"' + lang + '\" выбран\n' + predictions[1],
                           reply_markup=generate_page_buttons(page, lang, predictions[0]))


keep_alive()

executor.start_polling(dp)
