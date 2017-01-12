import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), 'req.db')


class DatabaseConnection(object):
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)


class Pencarian(object):

    def __init__(self, id, query, timestamp):
        self.id = id
        self.query = query
        self.timestamp = timestamp

    @staticmethod
    def insert(q):
        db = DatabaseConnection()
        query = """INSERT INTO pencarian
                   (query, timestamp)
                   VALUES
                   (:query, DATE('now', 'localtime'))
                   """
        with db.connection as con:
            cursor = con.cursor()
            cursor.execute(query, {'query': q})
            con.commit()


class Hasil(object):

    def __init__(self, id, query_id, label, arti):
        self.id = id
        self.query_id = query_id
        self.label = label
        self.arti = arti
        # self.db = DatabaseConnection()

    @staticmethod
    def select(q, expire_after=None):
        db = DatabaseConnection()
        if expire_after:
            query = "select h.* from hasil h join pencarian p on (p.id=h.query_id) where p.query=:query and cast((julianday('now', 'localtime') - julianday(p.timestamp)) as integer) <= :expire_after"
            conn = db.connection
            cur = conn.cursor()
            rows = cur.execute(query, {'query': q,
                                       'expire_after': expire_after})
            for row in rows:
                yield Hasil(*row)

    @staticmethod
    def insert_many(data):
        """data adalah list berisi tuple, dengan 3 item.
        Item pertama : label
        Item kedua : arti
        Item ketiga: query pencarian
        """
        query = """INSERT INTO hasil(label, arti, query_id)
                   VALUES(?, ? (
                          SELECT id FROM pencarian
                          WHERE query=?))"""
        db = DatabaseConnection()

        with db.connection as con:
            cur = con.cursor()
            cur.execute_many(query, data)
            con.commit()

                
