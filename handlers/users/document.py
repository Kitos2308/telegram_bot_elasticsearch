

from loader import bot, dp

from aiogram import types

from analytic.analytic import Analytic

from config import chat_id, instance
import os
import pandas as pd
import datetime as dt


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_file(message: types.Message):

    if Analytic.bug=="ip":
        await  message.document.download()
        file_path = await bot.get_file(message.document.file_id)

        def convert_datetime(val):
            try:
                return dt.datetime.strptime(val, "%Y-%m-%d %H:%M:%S,%f")
            except ValueError:
                return

        path = os.path.abspath(file_path['file_path'])
        df = pd.read_csv(path, encoding='utf-8', sep=": ", engine='python',
                         names=["date", "level", "ip_address", "sid", "method", "api_route"],
                         usecols=["date", "level", "ip_address", "sid", "method", "api_route"],
                         converters={'date': convert_datetime}, index_col=False,
                         na_values=["<CIMultiDictProxy('Server'", "Traceback (most recent call last):"],

                         skip_blank_lines=True)



        instance.find_ip(df, instance.choice)

        path_result=instance.return_result()

        with open(path_result, "rb") as file:
            if os.path.getsize(path_result) > 0:
                await bot.send_document(chat_id=chat_id, document=file,
                                        caption="отчет аналитики при поиске двух ip в одной сессии")
            else:
                await message.reply(
                    " Аналитика прошла успешно, при указанном уровне логирования,  ip в одной сессии не обнаружено \n")

    if Analytic.bug=="api":
        pass













