import requests
from models import Hasil, Pencarian, create_tables
from parser import Parser
from config import EXPIRED_AFTER

create_tables()

class Endpoint(object):
    AL_WASEETH = "http://www.almaany.com/ar/dict/ar-ar/{q}/?c=المعجم الوسيط"

class Almaany(object):
    """class tentang almaany"""
    def __init__(self, mujam, expire_after=None):
        """mujam: pilihan mu'jam (waseeth, )
        expire_after: setelah berapa lama nanti dia expired"""
        self.mujam = mujam
        self.expire_after = expire_after

    def tarjamah(self, query):
        """terjemahkan query, menurut self.mujam"""
        if self.mujam == 'waseeth':
            return self.waseeth(query)

        return NotImplementedError

    def waseeth(self, query):
        query_db = Hasil.select(query, self.expire_after)

        if len(query_db) > 0:
            return query_db

        resp_text = requests.get(Endpoint.AL_WASEETH.format(q=query)).text
        parser = Parser(resp_text)

        entities = parser.get_entities_with_query(query)

        if entities:
            Pencarian.insert(query)
            Hasil.insert_many(entities)
            rows = Hasil.select(query, self.expire_after)
            return rows
        return

