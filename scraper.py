import requests
from regex_patterns import near_results, meaning_results, entity


def get_meaning(q):
    resp = requests.get(Endpoint.AL_WASEETH.format(q=q))
    return meaning_results.search(resp.text).group(0)


def get_near(q):
    resp = requests.get(Endpoint.AL_WASEETH.format(q=q))
    return near_results.search(resp.text).group(0)


def get_entity(mean):
    """mean: hasil dari get_meaning / get_near

    return iterator object dari re.finditer"""
    return entity.finditer(mean)


class Endpoint(object):
    AL_WASEETH = "http://www.almaany.com/ar/dict/ar-ar/{q}/?c=المعجم الوسيط"
