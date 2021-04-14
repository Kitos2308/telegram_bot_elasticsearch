import datetime as dt
import json
import os
# from main_es import es
from elasticsearch import Elasticsearch, exceptions
from elasticsearch import RequestsHttpConnection
from ssl import create_default_context


def connection_db(username_es,pass_es):
    # context = create_default_context(cafile="/home/kitos/Desktop/repo_flydata/telegram_bot/__mileonair_com.pem")
    es = Elasticsearch(['https://christmastree.mileonair.com:2929'], connection_class=RequestsHttpConnection,http_auth=(username_es,pass_es),use_ssl=False, verify_certs=False)
    # es = Elasticsearch("http://localhost:9200")
    return es
# def connection_db():
#     es = Elasticsearch("http://localhost:9200")
#     return es


def init_microservices(es):
    # es.indices.delete(index='exclude_analytic')
    list_name = get_name_indices(es)
    cnt=0
    for name in list_name:
        if name != "prohibited_routes":
            cnt=cnt+1
            data = {"id": cnt, "name": name, "time": dt.datetime.now()}
            es.index(index='last_time_microservices', id=cnt, body=data)




def show_route(index, username_es, pass_es):
    body = {
        "from": 0,
        "size": 10000,
    }
    es = connection_db(username_es, pass_es)
    res = es.search(index=index, body=body)

    list = []
    res1 = res['hits']
    res2 = res1['hits']
    for count in res2:
        for key, value in count.items():
            if key == "_source":
                list.append(value['route'])

    return  list


def get_certain_data_without_time(index, param, es, from_):     # must fix when you will implement for microservices
    """
    index - name of table
    param - what kind of need to analyze

    """
    body = {

        "size": 10000,
        "query": {
            "bool": {
                "filter":[
                    {
            "match": {
                "message": param
            }}]

    }
    },
            "sort": [
                {"@timestamp": "asc"},

            ],
        "search_after": [
            from_
        ]
    }
    res = es.search(index=index, body=body)
    length=len(res["hits"]["hits"])

    cnt=0
    list=[]
    while length>cnt:
        list.append(res["hits"]["hits"][cnt]["_source"]["message"])
        cnt=cnt+1


    index = index

    return index, list


def get_certain_data(index, param, es):     # must fix when you will implement for microservices

    """
    index - name of table
    param - what kind of need to analyze
    """
    body = {
        'query': {
            'bool': {
                'must': [{
                    'match': {
                        "name": index

                    }
                }]
            }
        }
    }

    res = es.search(index='last_time_microservices', body=body)
    # id = res["hits"]["hits"][0]["_id"]

    if not res["hits"]["hits"]:


        pass

    else:
        last_time_db = res["hits"]["hits"][0]["_source"]["time"]
        body_ = {

            "size": 10000,
            "query": {
                "bool": {
                    "filter":[
                        {

                "match_phrase": {
                    "message": param
                }},

                    {
                "range": {
                    "@timestamp": {
                        "gte": last_time_db
                    }
                }

                }]


        }
        },
                "sort": [
                    {"@timestamp": "asc"},


                ],

        }
        res_ = es.search(index=index, body=body_)
        length=len(res_["hits"]["hits"])

        cnt=0
        list=[]

        while length>cnt:
            if res_["hits"]["hits"][cnt]["_source"]["message"]:
                # print(res_["hits"]["hits"][cnt]["_source"]["message"])
                list.append(res_["hits"]["hits"][cnt]["_source"]["message"])
            cnt=cnt+1
    last_time =get_last_time(index, es)
    # print("last_time_db", last_time_db)
    # print("last_time", last_time)
    if last_time_db == last_time:
        list=[]

    else:
        pass


        # # es.update(index="last_time_microservices", id=id, body=body_update)
        # # cnt_=0
        # for row in list:
        #     cnt_=cnt_+1
        #     data = {"message": row}
        #     es.index(index='tmp_message', id=cnt_, body=data)
        #
        # print(es.search(index="tmp_message", body={"from":0, "size":10000}))




    index = index
    # print(list)
    return index, list



def get_index_time(index, es):     # must fix when you will implement for microservices
    """
       index - name of table
       param - what kind of need to analyze
       """
    body = {
        'query': {
            'bool': {
                'must': [{
                    'match': {
                        "name": index

                    }
                }]
            }
        }
    }

    res = es.search(index='last_time_microservices', body=body)
    # id = res["hits"]["hits"][0]["_id"]

    if not res["hits"]["hits"]:
        cnt = check_count(es)
        last_time = get_last_time(index, es)
        data = {"id": cnt, "name": index, "time": last_time}
        es.index(index='last_time_microservices', id=cnt + 1, body=data)
    else:
        last_time_db = res["hits"]["hits"][0]["_source"]["time"]
        body_ = {

            "size": 10000,
            "query": {
                "bool": {
                    "filter": [

                        {
                            "range": {
                                "@timestamp": {
                                    "gte": last_time_db
                                }
                            }

                        }]

                }
            },
            "sort": [
                {"@timestamp": "asc"},

            ],

        }
        res_ = es.search(index=index, body=body_)
        length = len(res_["hits"]["hits"])

        cnt = 0
        list = []

        while length > cnt:
            if res_["hits"]["hits"][cnt]["_source"]["message"]:
                # print(res_["hits"]["hits"][cnt]["_source"]["message"])
                list.append(res_["hits"]["hits"][cnt]["_source"]["message"])
            cnt = cnt + 1
    last_time = get_last_time(index, es)
    # print("last_time_db", last_time_db)
    # print("last_time", last_time)
    if last_time_db == last_time:
        list = []

    else:
        pass

        # # es.update(index="last_time_microservices", id=id, body=body_update)
        # # cnt_=0
        # for row in list:
        #     cnt_=cnt_+1
        #     data = {"message": row}
        #     es.index(index='tmp_message', id=cnt_, body=data)
        #
        # print(es.search(index="tmp_message", body={"from":0, "size":10000}))

    index = index
    # print(list)
    return index, list




# def get_index(name_index, es, from_):
#     list=[]
#
#
#     body_1 ={
#
#
#         "size": 10000,
#         "sort": [
#             {"@timestamp": "asc"}
#
#         ],
#
#         "search_after": [
#             from_
#         ]
#     }
#
#     res = es.search(index=name_index, body=body_1)
#     list=[]
#     res1 = res['hits']
#     res2 = res1['hits']
#     for count in res2:
#         for key, value in count.items():
#             if key=="_source":
#                 list.append(value['message'])
#                 host=value['host']
#     return host, list



def convert_time(frame_data):

    time_list = []
    for row in frame_data:
        symbol = row.find(": ")
        try:
            time_ = dt.datetime.strptime(row[0:symbol], "%Y-%m-%d %H:%M:%S,%f")
            time_list.append(time_)

        except ValueError:
            pass

    return time_list


def get_sid(frame):      # frame is index from elasticsearch after function  get_index this is list
    list_=[]
    for row in frame:
        cnt = 0
        tmp_row = row

        while cnt != 3:
            symbol = tmp_row.find(": ")
            tmp_row = tmp_row[symbol + 1:len(row)]
            cnt = cnt + 1
            symbol_end = tmp_row.find(": ")

        list_.append(tmp_row[1:symbol_end])

    return list(set(list_))

def get_route(frame):      # frame is index from elasticsearch after function  get_index this is list
    cnt=0
    while cnt != 5:
        symbol = frame.find(": ")
        frame = frame[symbol + 1:len(frame)]
        cnt = cnt + 1
        symbol_end = frame.find(": ")

    return frame[1:symbol_end]



def get_ip(frame):      # frame is index from elasticsearch after function  get_index this is list
    list_=[]
    for row in frame:
        cnt = 0
        tmp_row = row
        while cnt != 2:
            symbol = tmp_row.find(": ")
            tmp_row = tmp_row[symbol + 1:len(row)]
            cnt = cnt + 1
            symbol_end = tmp_row.find(": ")

        list_.append(tmp_row[0:symbol_end])

    return list_


def add_prohibited_route(route, username_es, pass_es):
    body_1 = {
        "from": 0,
        "size": 10000

    }


    es = connection_db(username_es, pass_es)
    res = es.search(index='prohibited_routes', body=body_1)
    cnt=len(res["hits"]["hits"])
    # print(cnt)
    route = {"route": route}
    # print(route)
    es.index(index='prohibited_routes', id=cnt+1, body=route)



def get_id_route(route, username_es, pass_es):
    body = {
        'query': {
            'bool': {
                'must': [{
                    'match_phrase': {
                        'route': route
                    }
                }]
            }
        }
    }
    es = connection_db(username_es, pass_es)
    res = es.search(index='prohibited_routes', body=body)
    cnt=len(res["hits"]["hits"])
    list_id= res["hits"]["hits"]
    id = []
    for row in list_id:
        id.append(row["_id"])
    return id


def delete_route_(id, username_es, pass_es):
    es = connection_db(username_es, pass_es)
    es.delete(index="prohibited_routes", id=id)



def update_microservices(es):
    list=get_name_indices(es)
    for name in list:
        last_time=get_last_time()
        body = {
            'query': {
                'bool': {
                    'must': [{
                        'match_phrase': {
                            "name_microservice": name
                        }
                    }]
                }
            }
        }
        res = es.search(index='last_time_microservices', body=body)


    cnt = len(res["hits"]["hits"])
    data = {"name": name, "time": last_time}



    es.index(index='last_time_microservices', id=cnt + 1, body=route)




    microservices = {}
    list_name=get_name_indices(es)

    for name in list_name:
        if name != "prohibited_routes":

            last_time=get_last_time(name, es)
            # print(last_time)
            if last_time==None:
                pass
            else:
                microservices[name]=last_time

    return microservices

def check_count(es_):
    list_name = get_name_indices(es_)
    last_count={}
    cnt=0
    for name in list_name:
        if name != "prohibited_routes" or ".async-search":
            cnt = es_.count(index=name)
            last_count[name] = cnt['count']
    # print("=+===========================================================================")
    # print(last_count)
    # print("============================================================================+=")
    return last_count





def get_last_time(index, es):
    body = {

        "size": 1,

        "sort": [
            {"@timestamp": "desc"},

        ]

    }
    res =  es.search(index=index, body=body)
    cnt =  es.count(index=index)
    # print(index)
    # print(cnt)
    if cnt["count"] !=0:
        last_time = res["hits"]["hits"][0]["_source"]["@timestamp"]
    else:
        last_time=None

    return last_time





def get_name_indices(es):
    list=[]
    for index in es.indices.get('*'):
        # print(index)
        s=index.find(".")

        if s == -1:
            list.append(index)

    return list









# print(type(res["hits"]["hits"]))
#
# print(res["hits"]["hits"][4]["_source"]["route"])

# get_certain_data("bs_api",)









def get_certain_data_supervisor(index, param, es):     # must fix when you will implement for microservices

    """
    index - name of table
    param - what kind of need to analyze
    """
    body = {
        'query': {
            'bool': {
                'must': [{
                    'match': {
                        "name": index

                    }
                }]
            }
        }
    }

    res = es.search(index='last_time_microservices', body=body)
    # id = res["hits"]["hits"][0]["_id"]
    print(res)
    if not res["hits"]["hits"]:


        pass

    else:
        last_time_db = res["hits"]["hits"][0]["_source"]["time"]
        body_ = {

            "size": 100,
            "query": {
                "bool": {
                    "filter":[
                        {

                "match_phrase": {
                    "log.file.path": param
                }}
                        ,

                #     {
                # "range": {
                #     "@timestamp": {
                #         "gte": last_time_db
                #     }
                # }
                #
                # }
                    ]


        }
        },
                "sort": [
                    {"@timestamp": "desc"},


                ],

        }
        res_ = es.search(index=index, body=body_)
        length=len(res_["hits"]["hits"])

        cnt=0
        list=[]

        # print(res_)

        while length>cnt:



            # if res_["hits"]["hits"][cnt]["_source"]['log']['file']['path']==param:
            print(res_["hits"]["hits"][cnt]["_source"]['log']['file']['path'])
            list.append(res_["hits"]["hits"][cnt]["_source"]["message"])
            cnt=cnt+1
    last_time =get_last_time(index, es)
    # print("last_time_db", last_time_db)
    # print("last_time", last_time)
    if last_time_db == last_time:
        list=[]

    else:
        pass


        # # es.update(index="last_time_microservices", id=id, body=body_update)
        # # cnt_=0
        # for row in list:
        #     cnt_=cnt_+1
        #     data = {"message": row}
        #     es.index(index='tmp_message', id=cnt_, body=data)
        #
        # print(es.search(index="tmp_message", body={"from":0, "size":10000}))




    index = index
    # print(list)
    return index, list