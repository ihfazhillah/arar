"""Parser module, disini ada parser object"""
from almaany.config import ENTITY, MEANING_RESULT, TAGS


class Parser(object):
    """Parser object, semua logic tentang parsing disini"""

    def __init__(self, src):
        self.src = src

    @staticmethod
    def meaning(src):
        """mendapatkan result dengan class=meaning_results
        src: source code dari html"""
        mean = MEANING_RESULT.search(src).group(0)
        return mean

    @staticmethod
    def entity(mean):
        """Mendapatkan entity dari meaning...

        mean: kembalian dari Parser.meaning"""
        entities = ENTITY.finditer(mean)
        return entities

    def get_entities_with_query(self, query):
        """Mengembalikan tuple didalam list.
        tuple ada tiga item (secara urut):
        1. label
        2. arti
        3. query

        bila ditemukan, bila tidak akan mereturn None"""
        try:
            entities = list(Parser.entity(Parser.meaning(self.src)))
        except AttributeError:
            return

        return [(x.group('label'),
                 x.group('arti').replace('<br/>', '\n'),
                 query,
                ) for x in entities]

    @staticmethod
    def strip_tag(src):
        """strip tags"""
        return TAGS.sub("", src)
