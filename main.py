
import asyncio
from utils.read_file import read_file, get_mask, last_time, mask_time, time_before_last
from loader import bot
# from config import chat_id, path, path_result_two_ip, instance, path_critical, path_error, path_prohibited_api,path_secuence,path_elastic
import os
from handlers.users._stop_ import shutdown
from analytic.es import get_certain_data



async def periodic(sleep_for):
    while True:
        await asyncio.sleep(sleep_for)
        df = read_file(path)
        frame_critical = get_mask(df, "CRITICAL")
        frame_error = get_mask(df, "ERROR")
        host, critical = get_certain_data("bs_api", 'CRITICAL')

        last_time_critical = last_time(frame_critical)
        last_time_error = last_time(frame_error)
        last_time_frame=last_time(df)
        time_before=time_before_last(df)




        if (not frame_critical.empty) and  (Analytic.time_critical != last_time_critical):
            new_frame=mask_time(frame_critical, Analytic.time_critical)
            open(path_critical, 'w').close()
            # print(new_frame)
            if (not new_frame.empty):
                for items in new_frame.iterrows():
                    with open(path_critical, 'a') as out:
                        out.write('\n')
                        out.write(str(items) + '\n')
                        out.write("======================================")
                        out.close()
                with open(path_critical, 'rb') as out:
                    print(out)
                    await bot.send_document(chat_id, document=out, caption="отчет о CRITICAL")
            Analytic.time_critical=last_time_critical

            open(path_elastic, 'w').close()

            for row in critical:
                with open(path_elastic, 'a') as out_es:
                    out_es.write(row + '\n')
                    out_es.close()

            with open(path_elastic, 'rb') as out_es__:
                print(out_es__)
                await bot.send_document(chat_id, document=out_es__, caption="отчет о критикал от elastic")



        if (not frame_error.empty) and (Analytic.time_error != last_time_error):
            new_frame=mask_time(frame_error, Analytic.time_error)
            open(path_error, 'w').close()
            # print(new_frame)


            if (not new_frame.empty):
                for items in new_frame.iterrows():
                    with open(path_error, 'a') as out:
                        out.write('\n')
                        out.write(str(items) + '\n')
                        out.write("=====================================")
                        out.close()

                with open(path_error, 'rb') as out:
                    await bot.send_document(chat_id, document=out, caption="отчет о ERROR")
            Analytic.time_error=last_time_error

        prohibited = instance.prohibit_route(df, Analytic.time_)
        instance.find_ip_auto(df, Analytic.time_)
        find_secuence=instance.find_secuence(df, Analytic.time_sequence)
        if (Analytic.time_ != last_time_frame):
            Analytic.time_ = last_time_frame
            Analytic.time_sequence=time_before

            with open(path_result_two_ip, "rb") as file:
                if os.path.getsize(path_result_two_ip) > 0:
                    await bot.send_document(chat_id=chat_id, document=file,
                                            caption="ip которые работают в одной сессии")

            if prohibited:
                open(path_prohibited_api, 'w').close()
                with open(path_prohibited_api, 'a') as out:
                    out.write('\n')
                    out.write(str(prohibited) + '\n')
                    out.close()

                with open(path_prohibited_api, 'rb') as out:
                    await bot.send_document(chat_id=chat_id, document=out,
                                            caption="запрещенные апи")


            if find_secuence:
                open(path_secuence, 'w').close()
                with open(path_secuence, 'a') as out:
                    out.write('\n')
                    out.write(str(find_secuence) + '\n')
                    out.close()

                with open(path_secuence, 'rb') as out:
                    await bot.send_document(chat_id=chat_id, document=out,
                                            caption="Запретные переходы login,confirm,register")







        # if (Analytic.time_ != last_time_frame):
        #     Analytic.time_ = last_time_frame
        #     prohibited=instance.prohibit_route(df)
        #     print(prohibited)
        #     if not prohibited.empty:
        #         await bot.send_message(chat_id, str(prohibited))




async def startup(dp):
    await bot.send_message(chat_id=chat_id, text="Бот запущен.")

# async  def on_shutdown(dp):
#     await bot.send_message(chat_id=chat_id, text="Бот остановлен")



if __name__=="__main__":

    from aiogram import executor
    from handlers import dp
    from analytic.analytic import Analytic


    Analytic.time_critical="2019-12-14 17:09:23,464"
    Analytic.time_error="2019-12-14 17:09:23,464"
    Analytic.time_="2019-12-14 17:09:23,464"
    Analytic.time_sequence="2019-12-14 17:09:23,464"


    while True:

        dp.loop.create_task(periodic(5))
        executor.start_polling(dp, on_startup=startup, on_shutdown=shutdown,skip_updates=True)
















