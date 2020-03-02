import telebot
import time
from telebot import types
from bottoken import *

#основная функция бота!
bot = telebot.TeleBot(BOTTOKEN)
# bot.set_update_listener(listener) #регистрация вывода в консоль

searchdict = {}

#декоратор для цикла позиции поиска гифок
def cyclesearch(sgif):

    searchpos = 0

    def wrapper(gifapikey, searchposition: int, word: str = 'dolphin', limit=1):
        # nonlocal searchpos
        global searchdict                          #  УБРАТЬ КОСТЫЛЬ!!!
        if word not in searchdict:
            searchdict[word] = 0
        elif searchdict[word] >= 30:
            searchdict[word] = 0
        else: searchdict[word] += limit
        # if searchpos >= 50:
        #     searchpos = 0
        # else:
        #     searchpos += limit
        return sgif(gifapikey, searchdict[word], word, limit)

    return wrapper

#поиск гифок
@cyclesearch
def searchgif(gifapikey, searchposition: int, word: str = 'dolphin', limit=1):
    '''возвращает список ссылок найденных гифок по запросу 'word'
    в количестве 'limit' штук начиная с результата с номером 'searchposition' '''
    from requests import get
    import json
    try:
        search = get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&media_filter=minimal&limit=%s&pos=%s" \
            % (word, gifapikey, limit, searchposition))
        gif = dict(json.loads(search.content.decode('utf-8')))
    except:
        print ('something wrong with request')
    # print (gif)
    listlink = []
    for result in gif['results']:
        listlink.append(result['url'])
    return listlink

def dolphinospam(chatid):
    count = 3
    word = 'dolphin'
    gifs = searchgif(GIFAPI, 0, word, count)
    for gif in gifs:
        bot.send_animation(chatid, gif)

#вывод сообщений в консоль
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.from_user.first_name) + " " + \
                  str(m.from_user.last_name) + "ID - " + str(m.from_user.id) +\
                  " \n[" + str(m.chat.id) + "]: " + m.text)

class GifSearch:
    GIFAPI_TENOR = str #задать ключ АПИ
    def __init__(self, chatid:str):
        '''
        :param name: Название чата в котором был запрос
        :param word_request: Словарь запросов в чате:номер поиска
        '''
        self._word_request = {}
        self.chatid = chatid

    @property
    def name(self):
        return self._chatname

    def request_pos(self, search_request:str):
        '''
        Позиция поиска
        :param search_request: слово запроса
        :return: позиция поиска или добавление слова в словарь
        '''
        if self._word_request.get(search_request):
            return self._word_request.get(search_request)
        else:
            self._word_request[search_request] = 0
            return 0

    def set_pos(self, search_request:str, search_position:int):
        search_request.lower()
        self._word_request[search_request] = search_position

    def search_gif_tenor(self, limit:int, search_request:str):
        '''
        Поиск гифок на tenor.com
        :param limit: Кол-во гифок в запросе
        :param search_request: Запрос
        :return: Список ссылок
        '''
        from requests import get
        import json
        search_pos = self.request_pos(search_request) #последний адрес поиска
        search_result = [None] * limit

        try:
            search = get(
                "https://api.tenor.com/v1/search?q=%s&key=%s&media_filter=minimal&limit=%s&pos=%s" \
                % (search_request, GifSearch.GIFAPI_TENOR, limit, search_pos))
            gif = dict(json.loads(search.content.decode('utf-8')))
        except:
            print('something wrong with request')
            return ['request error']
        for position, result in enumerate(gif['results']):
            search_result[position] = result['url']

        self.set_pos(search_request, int(gif['next'])) #обновление последнего адреса поиска
        if None in search_result:
            self.set_pos(search_request, 0)
        if search_result[0] == None:
            search_result = None
            self.set_pos(search_request, 0)
        return search_result

GifSearch.GIFAPI_TENOR = GIFAPI #инициализация АПИ


#тестирование
word = 'chrysalys'
if __name__ == "__main__":
    giff = GifSearch(123)
    giff.set_pos(word, 4)
    result = giff.search_gif_tenor(5,word)
    print (result)
