from loader import bot, dp

from aiogram import types

from config import chat_id


@dp.message_handler()
async def echo(message: types.Message):

    text = f"Привет, ты написал: {message.text}"
    await bot.send_message(chat_id=chat_id, text=text)

    await message.answer(text=text)