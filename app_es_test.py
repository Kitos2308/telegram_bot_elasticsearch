import urllib3
import asyncio

from handlers.users._stop_ import shutdown
from analytic.es import connection_db, get_name_indices, init_microservices
from utils.analytic_error_loop import *
from utils.chose_name import choose_name
from config import *


# from elasticsearch import client
async def periodic(sleep_for, es, list_exclude, list_prod, list_dev, extention_list, list_vsphere):
    update = Update(es, list_prod)
    update_dev = Update(es, list_dev)
    update_vsphere = Update(es, list_vsphere)
    new_list_name = update.exclude(list_exclude=list_exclude, list_name=list_name)
    factory = AbstactClass.create_service_analyzer()

    while True:
        await asyncio.sleep(sleep_for)
        await factory['Vsphere'].create_analyzer(es, list_vsphere, instance_es.path_vsphere, 'vsphere_result',
                                                 chat_id_=chat_id_vsphere)
        await factory['Production'].create_analyzer(es, list_prod, instance_es.path_result_prod, 'prod_result',
                                                    chat_id_=chat_id_prod)
        await factory['Developer'].create_analyzer(es, list_dev, instance_es.path_result_dev, 'dev_result',
                                                   extention_list, chat_id_=chat_id_dev)
        update.update_time()
        update_dev.update_time()
        update_vsphere.update_time()



async def startup(dp):
    pass

    # await bot.send_message(chat_id=chat_id, text="Бот запущен.")


# async  def on_shutdown(dp):
#     await bot.send_message(chat_id=chat_id, text="Бот остановлен")


if __name__ == "__main__":

    from aiogram import executor
    from handlers import dp
    list_vsphere_ = ['vsphere']
    list_exclude_ = ['logs-index_pattern_placeholder', 'metrics-index_pattern_placeholder', 'prohibited_routes',
                    'last_time_microservices', 'tmp_message']
    urllib3.disable_warnings()
    es = connection_db(username_es, pass_es)
    extention_list_ = ['bs_api']
    list_name = get_name_indices(es)

    # es.delete(index='last_time_microservices',id=15)
    # cnt = es.count(index="last_time_microservices")
    # data = {"id": cnt['count']+1, "name": "filebeat-7.11.1-2021.03.14-000001", "time": dt.datetime.now()}
    # es.index(index='last_time_microservices', id=cnt['count']+1, body=data)

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
        print(res['hits']['hits'][cnt]['_source'])
        cnt = cnt + 1
    list_prod_ = []
    list_dev_ = []

    init_microservices(es)


    _list_prod_, _list_dev_ = choose_name(list_name, list_prod_, list_dev_, list_exclude_)

    print(_list_prod_)
    print(_list_dev_)
    try:
        while True:
            dp.loop.create_task(periodic(30, es, list_exclude_, _list_prod_, _list_dev_, extention_list_, list_vsphere_))
            executor.start_polling(dp, on_startup=startup, on_shutdown=shutdown, skip_updates=True)
    except Exception as ex:
        print(ex)

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
