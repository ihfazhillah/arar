"""init script"""
from almaany.scraper import Almaany

def waseeth(query, expire_after):
    """api untuk waseeth
    query: pencarian
    expire_after: pencarian akan disimpan didatabase,
                  setelah expire_after habis, maka dia akan
                  melakukan livescrape ulang

    return: 
        - HasilCollection dengan attribute: 1. label 2. arti 3. length 
        bila ditemukan
        - None bila tidak ditemukan hasil"""
    return Almaany('waseeth', expire_after).tarjamah(query)
# import sys
# sys.path.append(".")
