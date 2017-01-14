import requests
from regex_patterns import near_results, meaning_results, entity
import sqlite3
import os
from models import Hasil, Pencarian, create_tables

EXPIRED_AFTER = 10 # in days

create_tables()

def get_meaning(q):
    query_db = Hasil.select(q, EXPIRED_AFTER)

    if len(query_db) == 0:
        Pencarian.insert(q=q)

        resp = requests.get(Endpoint.AL_WASEETH.format(q=q))

        try:
            entity = list(get_entity(meaning_results.search(resp.text).group(0)))
        except AttributeError:
            return

        entities = [(x.group('label'),
                     x.group('arti').replace('<br/>', '\n'),
                     q) for x in entity]

        Hasil.insert_many(data=entities)

        rows = Hasil.select(q=q, expire_after=EXPIRED_AFTER)

        return rows

    return query_db


def get_near(q):
    resp = requests.get(Endpoint.AL_WASEETH.format(q=q))
    return near_results.search(resp.text).group(0)


def get_entity(mean):
    """mean: hasil dari get_meaning / get_near

    return iterator object dari re.finditer"""
    return entity.finditer(mean)


class Endpoint(object):
    AL_WASEETH = "http://www.almaany.com/ar/dict/ar-ar/{q}/?c=المعجم الوسيط"
