import telebot
import time
from telebot import types
from bottoken import *
from requests import get #for GifSearch
import json              #for GifSearch
# from testfunctions import SqlData
import dimanobot.sql

#основная функция бота!
bot = telebot.TeleBot(BOTTOKEN)
# bot.set_update_listener(listener) #регистрация вывода в консоль



def dolphinospam(gifsearch, chatid):
    count = 3
    word = 'dolphin'
    gifs = gifsearch(count, word)
    # gifs = searchgif(GIFAPI, 0, word, count)
    for gif in gifs:
        bot.send_animation(chatid, gif)

botdata = dimanobot.sql.SqlData(dbname=postgresql_bd, user=postgresql_username,
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


