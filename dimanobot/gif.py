from requests import get  # for GifSearch
import json  # for GifSearch
import re


# GifSearch.GIFAPI_TENOR = GIFAPI  # Указать ключ api

class GifSearch:
    GIFAPI_TENOR = str  # задать ключ АПИ
    re_query = r'(?i)^gif (\d) (\w+)(?: |-|:)?(\w*)(?: |-|:)?(\w*)$'

    def __init__(self, gif_search_dict: dict):
        """
        :param gif_search_dict: Словарь для сохранения запросов
        """
        self._word_request = gif_search_dict
        self.content_filter = ['off', 'low', 'medium', 'high']

    def request_pos(self, search_request: str):
        """
        Позиция поиска
        :param search_request: слово запроса
        :return: позиция поиска или добавление слова в словарь
        """
        if self._word_request.get(search_request):
            return self._word_request.get(search_request)
        else:
            self._word_request[search_request] = 0
            return 0

    def set_pos(self, search_request: str, search_position: int):
        search_request = search_request.lower()
        self._word_request[search_request] = search_position

    def search_gif_tenor(self, limit: int, search_request: str):
        """
        Поиск гифок на tenor.com
        :param limit: Кол-во гифок в запросе
        :param search_request: Запрос
        :return: Список ссылок
        """
        search_request = search_request.lower()
        search_pos = self.request_pos(search_request)  # последний адрес поиска
        search_result = [None] * limit

        try:
            search = get(
                "https://api.tenor.com/v1/search?q=%s&key=%s&contentfilter=%s&media_filter=minimal&limit=%s&pos=%s" \
                % (search_request, GifSearch.GIFAPI_TENOR, self.content_filter[0], limit, search_pos))
            gif = dict(json.loads(search.content.decode('utf-8')))
        except:
            print('something wrong with request')
            return ['request error']
        for position, result in enumerate(gif['results']):
            search_result[position] = result['url']

        self.set_pos(search_request, int(gif['next']))  # обновление последнего адреса поиска
        if None in search_result:
            self.set_pos(search_request, 0)
        if search_result[0] == None:
            search_result = None
            self.set_pos(search_request, 0)
        return search_result

    def request(self, text):
        search = re.match(self.re_query, text)  # разбираем строку поиска
        wordlist = []
        word = str(search.group(2))
        count = int(search.group(1))
        if count <= 0:
            return
        wordlist = [str(search.group(3)), str(search.group(4))]
        for pos in wordlist:
            if pos: word += ' ' + pos
        return self.search_gif_tenor(count, word)

