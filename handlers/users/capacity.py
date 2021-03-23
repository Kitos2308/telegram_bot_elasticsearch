from elasticsearch import client

from analytic.es import connection_db

from loader import bot, dp

from aiogram import types

from config import chat_id,  pass_es, username_es

from aiogram.dispatcher.filters import Command


def find_(string):
    list=[]
    running = True
    cnt=0
    while running:
        position_start=string.find(" ")


        position_end=(string[position_start+1: len(string)]).find(" ")

        if string[position_end]==".":
            print("==========")
            position_end=(string[position_end+1:len(string)]).find(" ")

        list.append(string[position_start:position_end+3])
        string = string[position_end+1:len(string)]
        cnt=cnt+1
        if cnt==4:
            break
    return list



@dp.message_handler(Command("capacity"))
async def capacity(message: types.Message):

    es = connection_db(username_es, pass_es)
    string=client.CatClient(es).allocation()



    if str(message.chat["id"]) == chat_id:
        list=find_(string)

        await bot.send_message(chat_id=chat_id, text="disk.indices: "+list[0] + "\n" + "disk.used: "+ list[1]+  "\n"+"disk.avail: "+ list[2]+ "\n"+"disk.total: "+list[3])
    else:
        await message.answer(text="К сожалению ты тут не найдешь ничего интересного \n")





