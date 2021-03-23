# from analytic.es import add_or_update_microservices, connection_db, check_count
from config import pass_es, username_es, instance_es
import urllib3
import datetime as dt
import requests
from ssl import create_default_context
from elasticsearch import Elasticsearch, exceptions
from elasticsearch import RequestsHttpConnection
from analytic.es import get_name_indices, get_last_time, check_count


es = Elasticsearch("http://localhost:9200")
# es.indices.create(index="last_time_microservices", ignore=[400, 404])


print(instance_es.show_prohibited_route(es))