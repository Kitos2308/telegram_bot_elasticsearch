from elasticsearch import client

from analytic.es import connection_db

from loader import bot, dp

from aiogram import types

from config import chat_id, pass_es, username_es

from aiogram.dispatcher.filters import Command

import pandas as pd


def find_(string):
    inputs = list(map(str, string.split()))
    return inputs



@dp.message_handler(Command("show"))
async def capacity(message: types.Message):
    es = connection_db(username_es, pass_es)
    list_ = []
    body = {
        "size": 100,

        "sort": [
            {"id": "asc"},

        ],
    }

    res = es.search(index='last_time_microservices', body=body)
    length = len(res['hits']['hits'])
    cnt = 0
    while length - 1 > cnt:
        list_.append(str(res['hits']['hits'][cnt]['_source']['name']))
        cnt = cnt + 1

    if str(message.chat["id"]) == chat_id:
        string_ = ''.join(str(e + '\n') for e in list_)
        await bot.send_message(chat_id=chat_id, text=string_)
    else:
        await message.answer(text="К сожалению ты тут не найдешь ничего интересного \n")
