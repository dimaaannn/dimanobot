import json #for Datasaver
import os #for Datasaver
from bottoken import *
import psycopg2

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





#словарь обращений к боту
#дельфиноспам по рэндом таймеру
#сделать диалоговый модуль



user_dict = {161613125:{'first_name':'Dima',
                        'last_name':'K.',
                        'username':'dimaaannn',
                        'steps':0,
                        'is_bot':False,
                        'chats_id':[222]}
             }

myid = 161613125
notmyid = 161613126
notmyiddict = {'first_name':'Vasya',
               'last_name':'B.',
               'steps':5,
               'is_bot':True}

dict2 = {'abc':342, 'dasf':'ddddeeet', 3424:'jjjeeeej'}

#---------end---------
userid = 7
increment = 1

botdata = SqlData(dbname=postgresql_bd, user=postgresql_username,
                        password=postgresql_password, host=postgresql_host)
conn = botdata.db_connect()
cursor = conn.cursor()

#test request
cursor.execute('SELECT step, user_id FROM botdata.users where user_id=%s', (str(userid)))
temp = cursor.fetchone()
print('RAW STRING: ', temp)
# conn.commit()
cursor.close()
print ('close connection = ', botdata.db_disconnect())

#bd chat_id, user_id, message_id, date, text, reply_to_message_id

