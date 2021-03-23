from loader import bot, dp

from aiogram import types

from config import chat_id

from aiogram.dispatcher.filters import Command

from loader import loop

from aiogram import executor

from main import periodic



@dp.message_handler(Command("start"))
async def on_startup(message: types.Message):
    await bot.send_message(chat_id=chat_id, text="Бот запущен")


