import telebot
import time
from telebot import types
from bottoken import *
from requests import get #for GifSearch
import json              #for GifSearch
# from testfunctions import SqlData
import psycopg2

#основная функция бота!
bot = telebot.TeleBot(BOTTOKEN)
# bot.set_update_listener(listener) #регистрация вывода в консоль

class SqlData:
    def __init__(self, **kwargs):
        self.__connect_data = kwargs
        self.connection = None

    def db_connect(self):
        '''
        Connect to DB
        '''
        self.connection = psycopg2.connect(**self.__connect_data)
        return self.connection

    def db_disconnect(self):
        '''
        Disconnect with DB
        '''
        if not self.connection.closed:
            return
        self.connection.close()
        return bool(self.connection.closed)

    def message_logger(self, message):
        with self.connection.cursor() as cursor1:
            reply_to = 0
            try:
                reply_to = message.reply_to_message.message_id
            except AttributeError:
                pass
            cursor1.execute('''
            INSERT INTO botdata.messages (chat_id, user_id, message_id, time_stamp, text, reply_to) 
            VALUES (%s, %s, %s, (TIMESTAMPTZ 'epoch' + %s * '1 second'::interval), %s, %s) 
            ''', (str(message.chat.id), str(message.from_user.id), str(message.message_id), str(message.date),\
                  str(message.text), str(reply_to)))
            self.connection.commit()
        return cursor1.statusmessage


def dolphinospam(gifsearch, chatid):
    count = 3
    word = 'dolphin'
    gifs = gifsearch(count, word)
    # gifs = searchgif(GIFAPI, 0, word, count)
    for gif in gifs:
        bot.send_animation(chatid, gif)

botdata = SqlData(dbname=postgresql_bd, user=postgresql_username,
                        password=postgresql_password, host=postgresql_host)
#вывод сообщений в консоль
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    botdata.db_connect()
    for message in messages:
        botdata.message_logger(message)
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.from_user.first_name) + " " + \
                  str(m.from_user.last_name) + "ID - " + str(m.from_user.id) + \
                  " \n[" + str(m.chat.id) + "]: " + m.text)




class GifSearch:
    GIFAPI_TENOR = str #задать ключ АПИ
    def __init__(self, gif_search_dict:dict):
        '''
        :param name: Название чата в котором был запрос
        :param word_request: Словарь запросов в чате:номер поиска
        '''
        self._word_request = gif_search_dict
        self.content_filter = ['off', 'low', 'medium', 'high']

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
        search_request = search_request.lower()
        self._word_request[search_request] = search_position

    def search_gif_tenor(self, limit:int, search_request:str):
        '''
        Поиск гифок на tenor.com
        :param limit: Кол-во гифок в запросе
        :param search_request: Запрос
        :return: Список ссылок
        '''
        search_request = search_request.lower()
        search_pos = self.request_pos(search_request) #последний адрес поиска
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

        self.set_pos(search_request, int(gif['next'])) #обновление последнего адреса поиска
        if None in search_result:
            self.set_pos(search_request, 0)
        if search_result[0] == None:
            search_result = None
            self.set_pos(search_request, 0)
        return search_result

GifSearch.GIFAPI_TENOR = GIFAPI #инициализация АПИ

class DataSaver:
    """
    Сохраняет словари или списки в файлы внутри папки
    :param foldername: имя папки
    :param kwargs: dictname=dictionary
    """

    def __init__(self, foldername: str, **kwargs):
        self.dict_list = kwargs
        self.save_folder = foldername

    def save(self):
        """
        сохраняет в файлы все переданные ранее словари
        :return: True
        """
        from os.path import isdir
        from os import mkdir
        success_list = {}

        if not isdir(self.save_folder):  # создать папку если её нет
            try:
                mkdir(self.save_folder)
            except OSError:
                print("Creation of the directory %s failed" % self.save_folder)
        for k, link in self.dict_list.items():  # создаём файлы словарей
            if type(link) == dict or list:
                with open(r'%s\%s.json' % (self.save_folder, k), 'w') as filename:
                    json.dump(link, filename)
                    success_list[k] = True  # удачная запись файла
            else:
                success_list[k] = False  # если не удалось записать
                continue
        return success_list

    def load(self):
        """
        Загружает из файлов всю информацию
        :return: True
        """
        checklist = {}
        for k, link in self.dict_list.items():
            try:
                with open(r'%s\%s.json' % (self.save_folder, k), 'r') as filename:
                    if type(link) == dict:
                        link.update(json.load(filename))
                        checklist[k] = True
                    elif type(link) == list:
                        link.insert(0, json.load(filename))
                        checklist[k] = True
                    else:
                        print('item must be list or dict, your type {}'.format(type(link)))
                        checklist[k] = None
                        continue
            except FileNotFoundError:
                checklist[k] = False
                continue
        return checklist

#тестирование
word = 'chrysalys'
if __name__ == "__main__":
    giff = GifSearch(123)
    giff.set_pos(word, 4)
    result = giff.search_gif_tenor(5,word)
    print (result)


