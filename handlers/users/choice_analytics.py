import logging

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

# from keyboards.inline.callback_datas import buy_callback
from keyboards.inline.choice_buttons import choice, prohibited_api, find_ip, logging_deep, prohibited_api_
from loader import dp, bot
from analytic.analytic import Analytic
from analytic.analytic_es import Analytic_es
from states import Test
from config import instance
from config import instance_es, chat_id, username_es,pass_es


@dp.message_handler(Command("items"))
async def show_items(message: Message):

    if str(message.chat["id"])==chat_id:
        await message.answer(text="Выбирите тип проверки запрещенные апи или поиск двух ip в одной сессии. \n"
                                  "Если вам ничего не нужно - жмите отмену",
                             reply_markup=choice)
    else:
        await message.answer(text="К сожалению ты тут не найдешь ничего интересного \n")


#
# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "pear"
@dp.callback_query_handler(text_contains="запрещенные апи")
async def prohibited_api(call: CallbackQuery):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    Analytic.bug="api"
    Analytic_es.bug = "api"
    await call.answer(cache_time=10)

    callback_data = call.data

    # Отобразим что у нас лежит в callback_data
    # logging.info(f"callback_data='{callback_data}'")
    # В Python 3.8 можно так, если у вас ошибка, то сделайте предыдущим способом!
    logging.info(f"call = {callback_data}")

    await call.message.answer("Вы выбрали тестировать запрещенные апи, отправьте запрещенный путь",
                              reply_markup=prohibited_api_)
#
#
# Попробуем использовать фильтр от CallbackData
@dp.callback_query_handler(text_contains="поиск двух ip")
async def find_ip(call: CallbackQuery):
    Analytic.bug = "ip"

    await call.answer(cache_time=10)

    callback_data = call.data
    # Выведем callback_data и тут, чтобы сравнить с предыдущим вариантом.
    logging.info(f"call = {callback_data}")


    await call.message.answer("Вы выбрали искать два ip в одной сессии,  выбирите уровень логирования и отправьте боту файл для аналитики",
                              reply_markup=logging_deep)
#
#
@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery):
    # Ответим в окошке с уведомлением!
    await call.answer("Вы нажали отмену", show_alert=True)

    # Вариант 1 - Отправляем пустую клваиатуру изменяя сообщение, для того, чтобы ее убрать из сообщения!
    await call.message.edit_reply_markup(reply_markup=None)

    # Вариант 2 отправки клавиатуры (по API)
    # await bot.edit_message_reply_markup(chat_id=call.from_user.id,
    #                                     message_id=call.message.message_id,
    #                                     reply_markup=None)


@dp.callback_query_handler(text="INFO")
async def info(call: CallbackQuery):

    await call.answer ("Вы выбрали INFO, теперь отправьте файл боту для аналитки", show_alert=True)
    await call.message.edit_reply_markup(reply_markup=None)
    Analytic.choice="INFO"




@dp.callback_query_handler(text="DEBUG")
async def debug(call: CallbackQuery):

    await call.answer ("Вы выбрали DEBUG, теперь отправьте файл боту для аналитки", show_alert=True)
    await call.message.edit_reply_markup(reply_markup=None)
    Analytic.choice = "DEBUG"



@dp.callback_query_handler(text="WARNING")
async def warning(call: CallbackQuery):

    await call.answer("Вы выбрали WARNING, теперь отправьте файл боту для аналитки", show_alert=True)
    await call.message.edit_reply_markup(reply_markup=None)
    Analytic.choice = "WARNING"



@dp.callback_query_handler(text="ERROR")
async def error(call: CallbackQuery):

    await call.answer("Вы выбрали ERROR, теперь отправьте файл боту для аналитки", show_alert=True)
    await call.message.edit_reply_markup(reply_markup=None)
    Analytic.choice = "ERROR"



@dp.callback_query_handler(text="CRITICAL")
async def critical(call: CallbackQuery):

    await call.answer("Вы выбрали CRITICAL, теперь отправьте файл боту для аналитки", show_alert=True)
    await call.message.edit_reply_markup(reply_markup=None)
    Analytic.choice = "CRITICAL"


@dp.callback_query_handler(text="добавить путь")
async def add_prohibited_api(call: CallbackQuery):

    await call.answer("Вы выбрали добавить путь, напишите мне путь", show_alert=True)
    await call.message.edit_reply_markup(reply_markup=None)
    await Test.Q2.set()


@dp.callback_query_handler(text="удалить путь")
async def add_prohibited_api(call: CallbackQuery):

    await call.answer("Вы выбрали удалить путь, напишите мне путь", show_alert=True)
    await call.message.edit_reply_markup(reply_markup=None)
    await Test.Q1.set()


@dp.callback_query_handler(text="показать пути")
async def show(call: CallbackQuery):

    # result=instance.show()
    result=instance_es.show_prohibited_route(username_es, pass_es)
    str1=""
    for row in result:
        str1+=str(row)+"\n"
    await call.message.answer(text=str1)