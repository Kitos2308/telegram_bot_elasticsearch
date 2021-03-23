
from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command
from states import Test
from aiogram.dispatcher import FSMContext
from config import instance_es, username_es,pass_es




@dp.message_handler(state=Test.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer =message.text
    # await state.update_data(answer1=answer)

    await state.reset_state(with_data=False) #сбрасывает стейт но сохраняет данные стейта

    result=instance_es.delete_prohibited_route(answer, username_es, pass_es)

    if result:
        await message.answer(text=f"Ваш путь: {answer} успешно удален")
    else:
        await message.answer(text=f"Ваш путь: {answer} не существует")



@dp.message_handler(state=Test.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    # await state.update_data(answer1=answer)
    await message.answer(text=f"Ваш путь: {answer} успешно добавлен")
    await state.reset_state(with_data=False)  # сбрасывает стейт но сохраняет данные стейта
    instance_es.add_prohibited_route(answer, username_es, pass_es)







    # data = await state.get_data()
    # answer1 = data.get("answer1")
    # answer2 = message.text
    #
    # await message.answer("Спасибо за ответы")
    # await message.answer(f"Ответ 1: {answer1}")
    # await message.answer(f"Ответ 2: {answer2}")
    #
    # await state.reset_state(with_data=False) #сбрасывает стейт но сохраняет данные стейта





