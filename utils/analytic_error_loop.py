import abc
from analytic.analytic_es import *
from config import *
from loader import bot
import datetime as dt
from utils.list_to_order import list_to_order


class AbstactClass(abc.ABC):
    caption: str
    variant: int

    @staticmethod
    def create_service_analyzer():
        services = {
            'Vsphere': Vsphere(),
            'Production': Prod(),
            'Developer': Dev(),

        }
        return services

    async def create_analyzer(self, es, list_name, path_, caption_document, extention_list=None, chat_id_=None):
        if await self.create_analytic(es, list_name, path_):
            await self.create_notifier(caption_document, path_, chat_id_)
        if extention_list:
            if await self.create_extent_analytic(es, extention_list, path_):
                await self.create_notifier(caption_document, path_, chat_id_)
        else:
            pass

    async def create_notifier(self, caption, path_, chat_id_):
        if os.stat(path_).st_size != 0:
            with open(path_, 'rb') as out:
                await bot.send_document(chat_id_, document=out, caption=caption + str(dt.datetime.now()))
                open(path_, 'w').close()
                open(path_, 'a').close()

    def create_order(self, list_, caption, name, variant, path_):
        list_to_order(list_, caption + name, variant, path_)

    async def create_analytic(self, es, list_name, path_):
        flag = 0
        for row in list_name:
            try:
                tmp_error_index, tmp_error_list = get_certain_data(row, 'ERROR:', es)
                tmp_critical_index, tmp_critical_list = get_certain_data(row, 'CRITICAL:', es)
                if tmp_critical_list:
                    flag = 1
                    AbstactClass.caption = row + ' Critical '
                    AbstactClass.variant = 1
                    self.create_order(tmp_critical_list, AbstactClass.caption, row, AbstactClass.variant, path_)
                if tmp_error_list:
                    flag = 1
                    AbstactClass.variant = 1
                    AbstactClass.caption = row + ' Error '
                    self.create_order(tmp_error_list, AbstactClass.caption, row, AbstactClass.variant, path_)
            except Exception as ex:
                await bot.send_message(chat_id=chat_id, text=str(ex))
        return flag

    async def create_extent_analytic(self, es, extend_list, path_):
        flag = 0
        for row in extend_list:
            try:
                list_ip = instance_es.find_ip(row, es)
                list_prohibited = instance_es.prohibited_combination(row, es)
                list_prohibited_db = instance_es.prohibited_routes(row, es, username_es, pass_es)
                if list_ip:
                    flag = 1
                    AbstactClass.variant = 1
                    AbstactClass.caption = row + ' Ip в оной сессии: '
                    self.create_order(list_ip, AbstactClass.caption, row, AbstactClass.variant, path_)
                if list_prohibited:
                    flag = 1
                    AbstactClass.caption = row + ' Запрещенные переходы '
                    AbstactClass.variant = 2
                    self.create_order(list_prohibited, AbstactClass.caption, row, AbstactClass.variant, path_)

                if list_prohibited_db:
                    flag = 1
                    AbstactClass.variant = 1
                    AbstactClass.caption = row + ' Запрещенные переходы из базы '
                    self.create_order(list_prohibited_db, AbstactClass.caption, row, AbstactClass.variant, path_)
            except Exception as ex:
                await bot.send_message(chat_id=chat_id, text=str(ex))
        return flag


class Vsphere(AbstactClass):
    pass


class Prod(AbstactClass):
    pass


class Dev(AbstactClass):
    pass


class Update():

    def __init__(self, es, list_name):
        self.es = es
        self.list_name = list_name

    def exclude(self, list_exclude=None, list_name=None, id_=None, delete=None):

        for row in list_exclude:
            list_name.remove(row)

        if delete:
            self.es.delete(index='last_time_microservices', id=id_)
        else:
            pass

        return list_name

    def get_exclude(self):
        list_exclude = []

        body = {
            "size": 100,

            "sort": [
                {"id": "asc"},

            ],
        }
        res = self.es.search(index='exclude_analytic', body=body)
        length = len(res['hits']['hits'])
        cnt = 0
        while length - 1 > cnt:
            list_exclude.append(res['hits']['hits'][cnt]['_source'])
            cnt = cnt + 1
        return list_exclude

    def get_list_time_microservices(self):
        list_time = []

        body = {
            "size": 100,

            "sort": [
                {"id": "asc"},

            ],
        }
        res = self.es.search(index='last_time_microservices', body=body)
        length = len(res['hits']['hits'])
        cnt = 0
        while length - 1 > cnt:
            list_time.append(res['hits']['hits'][cnt]['_source'])
            cnt = cnt + 1
        return list_time

    def update_time(self):

        for name in self.list_name:
            if name != "prohibited_routes":
                if name != "last_time_microservices":
                    if name != "tmp_message":
                        if name != "metrics-index_pattern_placeholder":
                            if name != "logs-index_pattern_placeholder":
                                if name != "data_replicator_prod":
                                    ##############################UPDATE TIME###########################################                                    print(name)
                                    last_time_ = get_last_time(name, self.es)
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

                                    res = self.es.search(index='last_time_microservices', body=body)
                                    id = res["hits"]["hits"][0]["_id"]

                                    body_update = {
                                        "doc": {
                                            "time": last_time_
                                        }
                                    }
                                    print("================================================")
                                    print(res["hits"]["hits"])
                                    print("================================================")
                                    try:
                                        if id:

                                            list_ = self.get_list_time_microservices()
                                            for row in list_:
                                                if row['time'] == None:
                                                    self.exclude(row['name'], id, delete=True)

                                            self.es.update(index="last_time_microservices", id=id, body=body_update)
                                            self.es.update(index="last_time_microservices", id=id, body=body_update)
                                        else:

                                            list_ = self.get_list_time_microservices()
                                            for row in list_:
                                                if row['time'] == None:
                                                    self.exclude(row['name'], id, delete=True)

                                            cnt = self.es.count(index="last_time_microservices")
                                            data = {"id": cnt['count'] + 1, "name": name, "time": dt.datetime.now()}
                                            self.es.index(index='last_time_microservices', id=cnt['count'] + 1,
                                                          body=data)

                                    except Exception as ex:
                                        print(ex)
                                        # await bot.send_message(chat_id=chat_id, text=str(ex))

                                        # cnt = self.es.count(index="last_time_microservices")
                                        # self.es.update(index="last_time_microservices", id=cnt['count'] + 1, body=body_update)
                                        # self.es.update(index="last_time_microservices", id=cnt['count'] + 1, body=body_update)
