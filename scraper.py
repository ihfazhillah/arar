import requests
from regex_patterns import near_results, meaning_results, entity
import sqlite3
import os
from models import Hasil

EXPIRED_AFTER = 1 # in days


conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'req.db'))
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS
               pencarian(
               timestamp DATETIME NOT NULL,
               query TEXT NOT NULL,
               id INTEGER PRIMARY KEY AUTOINCREMENT)
               """)
cur.execute("""
               CREATE TABLE IF NOT EXISTS
               hasil(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               query_id INTEGER,
               label TEXT NOT NULL,
               arti TEXT NOT NULL,
               FOREIGN KEY(query_id) REFERENCES pencarian(id))
""")

conn.commit()
conn.close()


def get_meaning(q):
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'req.db'))
    cur = conn.cursor()
    query_db = cur.execute('''SELECT * FROM pencarian
                             WHERE query=? AND
                             CAST (
                             (julianday('now', 'localtime') - julianday(timestamp))
                             AS INTEGER) <= ?''', (q, EXPIRED_AFTER))

    if query_db.fetchone() is None:
        cur.execute('''INSERT INTO pencarian(timestamp, query)
                       VALUES(date('now', 'localtime'), ?)''', (q,))
        conn.commit()

        resp = requests.get(Endpoint.AL_WASEETH.format(q=q))

        entity = list(get_entity(meaning_results.search(resp.text).group(0)))
        entities = [(x.group('label'),
                     x.group('arti').replace('<br/>', '\n'),
                     q) for x in entity]

        cur.executemany('''INSERT INTO hasil(label, arti, query_id)
                           VALUES(?,?,
                           (SELECT id FROM pencarian WHERE query=?)
                           )''', entities)
        conn.commit()

        cur.execute('''SELECT label, arti FROM hasil
                       WHERE query_id=(
                       SELECT id FROM pencarian WHERE query=?)
                       ''', (q,))

        return cur.fetchall()

    cur.execute('''SELECT label, arti FROM hasil
                   WHERE query_id=(
                   SELECT id FROM pencarian WHERE query=?)
                   ''', (q,))
    return cur.fetchall()


def get_near(q):
    resp = requests.get(Endpoint.AL_WASEETH.format(q=q))
    return near_results.search(resp.text).group(0)


def get_entity(mean):
    """mean: hasil dari get_meaning / get_near

    return iterator object dari re.finditer"""
    return entity.finditer(mean)


class Endpoint(object):
    AL_WASEETH = "http://www.almaany.com/ar/dict/ar-ar/{q}/?c=المعجم الوسيط"
