"""Model module"""

import sqlite3
import os
from functools import wraps


DB_PATH = os.path.join(os.path.dirname(__file__), 'req.db')


def db_transaction(func):
    """membungkus sebuah fungsi, agar dapat berinteraksi
    dengan database.
    fungsi func harus didahului dengan argument cursor. 
    Setelah itu, argument yang diperlukan
    """
    @wraps(func)
    def _db_transaction(*args, **kwargs):
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            func(cursor, *args, **kwargs)
    return _db_transaction



class DatabaseConnection(object):
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)


class Pencarian(object):

    def __init__(self, id, query, timestamp):
        self.id = id
        self.query = query
        self.timestamp = timestamp

    @staticmethod
    @db_transaction
    def insert(cursor, q):
        query = """INSERT INTO pencarian
                   (query, timestamp)
                   VALUES
                   (:query, DATE('now', 'localtime'))
                   """
        cursor.execute(query, {'query': q})

class Hasil(object):

    def __init__(self, id, query_id, label, arti):
        self.id = id
        self.query_id = query_id
        self.label = label
        self.arti = arti


    @staticmethod
    @db_transaction
    def select(cursor, q, expire_after=None):
        if expire_after:
            query = ("""SELECT h.* FROM hasil h
                     JOIN pencarian p ON (p.id=h.query_id)
                     WHERE p.query=:query and 
                     CAST(                     
                        (JULIANDAY('now', 'localtime') - JULIANDAY(p.timestamp)) 
                        AS INTEGER) <= :expire_after"""
            
            rows = cursor.execute(query, {'query': q,
                                          'expire_after': expire_after})
            for row in rows:
                print(row)

    @staticmethod
    @db_transaction
    def insert_many(cursor, data):
        """data adalah list berisi tuple, dengan 3 item.
        Item pertama : label
        Item kedua : arti
        Item ketiga: query pencarian
        """
        query = """INSERT INTO hasil(label, arti, query_id)
                   VALUES(?, ?, (
                          SELECT id FROM pencarian
                          WHERE query=?))"""

        cursor.executemany(query, data)
        

                
