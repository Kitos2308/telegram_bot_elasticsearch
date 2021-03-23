import urllib3
import asyncio
from loader import bot
from config import chat_id, instance_es, pass_es, username_es, chat_id_bs_api, chat_id_wallet
import datetime as dt
import os
from handlers.users._stop_ import shutdown
# from elasticsearch import Elasticsearch, exceptions
from analytic.es import  connection_db, get_last_time, get_certain_data, get_name_indices, init_microservices, get_certain_data_supervisor
from utils.list_to_order import list_to_order
from notify import notify
# from elasticsearch import client
async def periodic(sleep_for, es):
    while True:





        list_name=get_name_indices(es)

        # updated_microservices = add_or_update_microservices(es)
#
        await asyncio.sleep(sleep_for)







        for name in list_name:
            if name != "prohibited_routes" :



                # # try:
                if name != "last_time_microservices":
                    if name != "tmp_message":
                        print(name)
                        tmp_critical_index, tmp_critical_list=get_certain_data(name, 'CRITICAL:', es)
                        tmp_critical_index_vsphere, tmp_critical_list_vsphere = get_certain_data('vsphere', 'CRITICAL:', es)

                        tmp_error_index, tmp_error_list = get_certain_data(name, 'ERROR:', es)

                        tmp_error_index_vsphere, tmp_error_list_vsphere = get_certain_data('vsphere', 'ERROR:',  es)

                        # list_ip_vsphere = instance_es.find_ip('vsphere', es)


                        if name=="bs_api":

                            list_ip=instance_es.find_ip(name, es)
                        else:
                            list_ip=None

                        list_prohibited=instance_es.prohibited_combination(name,es)

                        # list_prohibited_vsphere = instance_es.prohibited_combination('vsphere', es)

                        list_prohibited_db=instance_es.prohibited_routes(name,es,username_es,pass_es)

                        # index, list_supervisor = get_certain_data_supervisor(name, "/var/log/host/supervisor/chat.err.bs_api.log",
                        #                                           es)

                        # list_prohibited_db_vsphere = instance_es.prohibited_routes('vsphere', es, username_es, pass_es)

                        if name != "vsphere":




                            if tmp_critical_list :
                                print(tmp_critical_list)
                                list_to_order(tmp_critical_list, str("CRITICAL " + name),1, instance_es.path_result)
                                # tmp_critical_list=[]

                            if tmp_error_list:
                                print(tmp_error_list)
                                list_to_order(tmp_error_list, str("ERROR " + name), 1, instance_es.path_result)
                                # tmp_error_list=[]


                            if list_ip:
                                print(list_ip)
                                list_to_order(list_ip, str("IP в одной сессии "+ name), 1, instance_es.path_result)
                                # list_ip=[]

                            if list_prohibited:
                                print(list_prohibited)
                                list_to_order(list_prohibited, str("Запрещенные переходы " + name), 2, instance_es.path_result)
                                # list_prohibited=[]

                            if list_prohibited_db:
                                list_to_order(list_prohibited_db, str("Запрещенные переходы из базы "+ name), 1, instance_es.path_result)
                        else:

                            if tmp_critical_list_vsphere:
                                print(tmp_critical_list_vsphere)
                                list_to_order(tmp_critical_list_vsphere, str("CRITICAL " + name), 1, instance_es.path_vsphere)
                                tmp_critical_list_vsphere = []

                            if tmp_error_list_vsphere:
                                print(tmp_error_list_vsphere)
                                list_to_order(tmp_error_list_vsphere, str("ERROR " + name), 1, instance_es.path_vsphere)
                                tmp_error_list_vsphere = []

                            # if list_ip_vsphere:
                            #     print(list_ip_vsphere)
                            #     list_to_order(list_ip_vsphere, str("IP в одной сессии " + name), 1, instance_es.path_vsphere)
                            #     list_ip_vsphere = []
                            #
                            # if list_prohibited_vsphere:
                            #     print(list_prohibited_vsphere)
                            #     list_to_order(list_prohibited_vsphere, str("Запрещенные переходы " + name), 2,
                            #                   instance_es.path_vsphere)
                            #     list_prohibited_vsphere = []
                            #
                            # if list_prohibited_db_vsphere:
                            #     list_to_order(list_prohibited_db_vsphere, str("Запрещенные переходы из базы " + name), 1,
                            #                   instance_es.path_vsphere)




        ##############################UPDATE TIME############################################################

                        last_time_=get_last_time(name,es)

                        body = {
                            'query': {
                                'bool': {
                                    'must': [{
                                        'match': {
                                            "name": name

                                        }
                                    }]
                                }
                            }
                        }

                        res = es.search(index='last_time_microservices', body=body)
                        id = res["hits"]["hits"][0]["_id"]

                        body_update = {
                            "doc": {
                                "time": last_time_
                            }
                        }
                        print("================================================")
                        print(res["hits"]["hits"])
                        print("================================================")
                        if id:


                            es.update(index="last_time_microservices", id=id, body=body_update)
                            es.update(index="last_time_microservices", id=id, body=body_update)
                        else:
                            # cnt=es.count(index="last_time_microservices")
                            # es.update(index="last_time_microservices", id=cnt['count']+1, body=body_update)
                            # es.update(index="last_time_microservices", id=cnt['count']+1, body=body_update)

                            cnt = es.count(index="last_time_microservices")
                            data = {"id": cnt['count']+1, "name": name, "time": dt.datetime.now()}
                            es.index(index='last_time_microservices', id=cnt['count']+1, body=data)

            if name=="bs_api" or name=="partnership_service" or name=="order_listener":

                if notify(tmp_error_list, tmp_critical_list, list_prohibited, list_prohibited_db, list_ip,
                          instance_es.path_bsapi):


                    if os.stat(instance_es.path_bsapi).st_size != 0:
                        with open(instance_es.path_bsapi, 'rb') as out:
                            await bot.send_document(chat_id_bs_api, document=out,
                                                    caption="result " + name + " " + str(dt.datetime.now()))
                            open(instance_es.path_bsapi, 'w').close()
                    else:
                        pass

            if name=="wallet_api":
                if notify(tmp_error_list, tmp_critical_list, list_prohibited, list_prohibited_db, list_ip,
                          instance_es.path_wallet):

                    if os.stat(instance_es.path_wallet).st_size != 0:
                        with open(instance_es.path_wallet, 'rb') as out:
                            await bot.send_document(chat_id_wallet, document=out,
                                                    caption="result " + name + " " + str(dt.datetime.now()))
                            open(instance_es.path_wallet, 'w').close()
                    else:
                        pass





##############################################################################################################################################





        if os.stat(instance_es.path_result).st_size != 0:
            with open(instance_es.path_result, 'rb') as out:
                await bot.send_document(chat_id, document=out, caption="result " + str(dt.datetime.now()))
                open(instance_es.path_result, 'w').close()
        if os.stat(instance_es.path_vsphere).st_size != 0:
            with open(instance_es.path_vsphere, 'rb') as out:
                await bot.send_document(chat_id, document=out, caption="result_vsphere " + str(dt.datetime.now()))
                open(instance_es.path_vsphere, 'w').close()

        else:
            pass


        





async def startup(dp):
    await bot.send_message(chat_id=chat_id, text="Бот запущен.")





# async  def on_shutdown(dp):
#     await bot.send_message(chat_id=chat_id, text="Бот остановлен")



if __name__=="__main__":

    from aiogram import executor
    from handlers import dp

    urllib3.disable_warnings()
    es = connection_db(username_es, pass_es)

    # body = {
    #     "size":10000,
    #   "query": {
    #     "match_all": {}
    #   }
    # }
    #
    # res=es.delete_by_query(index="supervisor", body=body, request_timeout=60)


    # es.indices.create(index='prohibited_routes', ignore=[400, 404])
    # es.indices.create(index="last_time_microservices", ignore=[400, 404])
    # es.indices.create(index='tmp_message', ignore=[400, 404])

    init_microservices(es)

    while True:

        dp.loop.create_task(periodic(5, es))
        executor.start_polling(dp, on_startup=startup, on_shutdown=shutdown,skip_updates=True)