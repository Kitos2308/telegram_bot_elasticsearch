
from loader import bot, dp

from aiogram import types

from config import chat_id,  pass_es, username_es

from aiogram.dispatcher.filters import Command

from analytic.es import connection_db, get_name_indices

import os


@dp.message_handler(Command("delete"))
async def delete_docs(message: types.Message):
    command1= """
    curl  -k -u elastic:VgcEnBCQ4L3ahFwlidmM -XPUT -H "Content-Type: application/json" https://webchristmastree.mileonair.com:2929/_cluster/settings -d '{ "transient": { "cluster.routing.allocation.disk.threshold_enabled": false } }'
    
    """
    command2 = """
    curl  -k -u elastic:VgcEnBCQ4L3ahFwlidmM -XPUT -H "Content-Type: application/json" https://webchristmastree.mileonair.com:2929/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'
    
    """
    os.system(command1)

    os.system(command2)


    if str(message.chat["id"]) == chat_id:
        body = {"size": 10000, "query": { "match_all": {}}}
        es = connection_db(username_es,pass_es)
        list = get_name_indices(es)


        for name in list:
            print("name "+ name + "\n")
            es.delete_by_query(index=name, body=body, request_timeout=10)

        await bot.send_message(chat_id=chat_id, text="Документы удалены")
    else:
        await message.answer(text="К сожалению ты тут не найдешь ничего интересного \n")

