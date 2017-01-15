import requests
from regex_patterns import near_results, meaning_results, entity
import sqlite3
import os
from models import Hasil, Pencarian, create_tables
from parser import Parser


EXPIRED_AFTER = 10 # in days

create_tables()

def get_meaning(q):
    query_db = Hasil.select(q, EXPIRED_AFTER)

    if len(query_db) == 0:
        Pencarian.insert(q=q)

        resp = requests.get(Endpoint.AL_WASEETH.format(q=q))

        parser = Parser(resp.text)
        entities = parser.get_entities_with_query(q)

        Hasil.insert_many(data=entities)

        rows = Hasil.select(q=q, expire_after=EXPIRED_AFTER)

        return rows

    return query_db

class Endpoint(object):
    AL_WASEETH = "http://www.almaany.com/ar/dict/ar-ar/{q}/?c=المعجم الوسيط"
