

GIFAPI = 'JJYG01W4CPTP'
lmtgif = 3
search_term = "dolphin"
media_filter = 'minimal'
position = 1

class Chat:
    def __init__(self, chatname):
        self._chatname = chatname
        self.chat_users = {} #id:[name, lastname]

#перенести класс для поиска гифок в прод
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
        assert type(search_position) is int, 'Wrong search position'
        if search_position > self._word_request.get(search_request, 0):
            self._word_request[search_request] = search_position
        else:
            self._word_request[search_request] = 0

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
        search_result = []

        try:
            search = get(
                "https://api.tenor.com/v1/search?q=%s&key=%s&media_filter=minimal&limit=%s&pos=%s" \
                % (search_request, GifSearch.GIFAPI_TENOR, limit, search_pos))
            gif = dict(json.loads(search.content.decode('utf-8')))
        except:
            print('something wrong with request')
            return ['request error']
        if int(gif['next']) > 0:
            self.set_pos(search_request, int(gif['next'])) #обновление последнего адреса поиска
        else:
            return ['{} is not found'.format(search_request)] #при позиции 0 вернуть "not found"
        # for a in gif.items():
        #     print (a)
        for result in gif['results']:
            search_result.append(result['url'])
        return search_result

GifSearch.GIFAPI_TENOR = GIFAPI #инициализация АПИ

#Написать класс пользователя
class BotUser:
    def __init__(self, dict_of_users:dict):
        '''
        Known user class
        '''
        self.dict_of_users = dict_of_users

        # self.__id = int(user_id)
        # self.first_name = None
        # self.last_name = None
        # self.username = None
        # self.steps = 0
        # self.is_bot = bool     #бот ли пользователь
        # self.chats_id = []    #список ID чатов, в которых сост. пользовтель

    def known(self,id):
        if id in self.dict_of_users.keys(): return True
        else: return False

    def initialise(self, id, **kwargs):
        '''
        сканирует словарь и дополняет при необходимости
        '''
        default_var = {'first_name':None, 'last_name':None, 'username':None,
                        'steps':0, 'is_bot':False, 'chats_id':[]}
        if self.dict_of_users.get(id):
            self.dict_of_users[id].update(kwargs)
        else:
            self.dict_of_users[id] = default_var
            self.dict_of_users[id].update(kwargs)

    def get_params(self, id:int, *args):
        params_list = []
        if len(args) == 1:
            return self.dict_of_users.get(id).get(*args)
        else:
            for key in args:
                params_list.append(self.dict_of_users.get(id).get(key))
            return *params_list,
    def set_params(self, id:int, **kwargs):
        if self.dict_of_users.get(id):
            for key, var in kwargs.items():
                self.dict_of_users[id][key]
                self.dict_of_users[id][key] = var

#Написать метод группировки словарей для сохранения
#Написать метод распаковки словарей из словаря

#сделать список чятов бота
#словарь обращений к боту
#дельфиноспам по рэндом таймеру
#сделать диалоговый модуль


# chat = GifSearch('testchat')
# print ('search link: ',chat.search_gif_tenor(1, 'asadfadsff'))

user_dict = {161613125:{'first_name':'Dima', 'last_name':'K.', 'username':'dimaaannn',
                        'steps':0, 'is_bot':False, 'chats_id':[222]}
             }
myid = 161613125
notmyid = 161613126
notmyiddict = {'first_name':'Vasya', 'last_name':'B.',
                        'steps':5, 'is_bot':True}
users = BotUser(user_dict)
users.initialise(myid, **notmyiddict) #добавить пользователя


print (f'known user {myid} is {users.known(myid)}')
print (users.dict_of_users)
print ('params = {}'.format(users.get_params(myid, 'first_name', 'last_name')))

users.set_params(myid, first_name='aaaa')

# user1 = BotUser(161613125)
# user1.initialise(-346674731, first_name='Dima', last_name='K.', is_bot=False, username='dimaaannn')
# print (f'userID = {user1.id}\nName = {user1.first_name}, {user1.last_name}')

