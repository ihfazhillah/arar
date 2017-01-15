# pylint : disabled=C0103,W0622
"""Model module"""

import sqlite3
import os
from functools import wraps
from regex_patterns import tags

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
            ret = func(cursor, *args, **kwargs)
            return ret
    return _db_transaction


@db_transaction
def create_tables(cursor):
    """Fungsi untuk membuat table yang diperlukan"""

    cursor.execute("""CREATE TABLE IF NOT EXISTS
                   pencarian(
                   timestamp DATETIME NOT NULL,
                   query TEXT NOT NULL,
                   id INTEGER PRIMARY KEY AUTOINCREMENT)
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS
                   hasil(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   query_id INTEGER,
                   label TEXT NOT NULL,
                   arti TEXT NOT NULL,
                   FOREIGN KEY(query_id) REFERENCES pencarian(id))
    """)


class Pencarian(object):
    """Models untuk tabel pencarian
    params: id, query, timestamp"""
    def __init__(self, id, query, timestamp): 
        self.id = id 
        self.query = query
        self.timestamp = timestamp

    @staticmethod
    @db_transaction
    def insert(cursor, q):
        """Memasukkan pencarian"""
        query = """INSERT INTO pencarian
                   (query, timestamp)
                   VALUES
                   (:query, DATE('now', 'localtime'))
                   """
        cursor.execute(query, {'query': q})

class Hasil(object):
    """Model untuk tabel hasil,
    params : id, query_id, label, arti"""

    def __init__(self, id, query_id, label, arti):
        self.id = id
        self.query_id = query_id
        self.label = label
        self.arti = arti


    @staticmethod
    @db_transaction
    def select(cursor, q, expire_after=None):
        """mendapatkan semua hasil berdasarkan query(q) dan
        timestamp <= (expire_after)

        Bila expire_after None maka akan mengebalikan NotImplementedError

        return HasilCollections"""
        if expire_after:
            query = """SELECT h.* FROM hasil h
                     JOIN pencarian p ON (p.id=h.query_id)
                     WHERE p.query=:query and 
                     CAST(                     
                        (JULIANDAY('now', 'localtime') - JULIANDAY(p.timestamp)) 
                        AS INTEGER) <= :expire_after"""
            
            rows = cursor.execute(query, {'query': q,
                                          'expire_after': expire_after})
            return HasilCollections(rows)
        raise NotImplementedError

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

    def strip_tags(self):
        """Menghilangkan tags"""

        self.label = tags.sub("", self.label)
        self.arti = tags.sub("", self.arti)
        return self
        

class HasilCollections(object):
    """Karena hasil adalah generator object, 
    maka hanya bisa kita lakukan sekali saja:
    - untuk iterasi
    """
    def __init__(self, collections):
        # self.collections = collections
        import itertools

        self.lama, self.baru = itertools.tee(collections)
        self.count = sum(1 for _ in self.baru)

    def __iter__(self):
        return (Hasil(*row) for row in self.lama)

    def __len__(self):
        return self.count

    def length(self):
        """return length of HasilCollections"""
        return self.count
