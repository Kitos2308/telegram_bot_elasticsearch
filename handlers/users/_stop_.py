
from loader import bot, dp, loop

from aiogram import types

from config import chat_id

from aiogram.dispatcher.filters import Command







@dp.message_handler(Command("stop"))
async def shutdown(message: types.Message):
    await bot.send_message(chat_id=chat_id, text="Бот остановлен")
    exit()




