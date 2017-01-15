from regex_patterns import entity, meaning_results, tags


class Parser(object):

    def __init__(self, src):
        self.src = src

    def meaning(self, src):
        mean = meaning_results.search(src).group(0)
        return mean

    def entity(self, mean):
        entities = entity.finditer(mean)
        return entities

    def get_entities_with_query(self, query):
        try:
            entities = list(self.entity(self.meaning(self.src)))
        except AttributeError:
            return

        return [(x.group('label'),
                 x.group('arti').replace('<br/>', '\n'),
                query,
                ) for x in entities]
