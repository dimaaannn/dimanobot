from bot_func import bot
import time
from random import randint
from random import choice

from telebot import types


class Messager:

    def __init__(self, bot_instance, sql_instance):
        self.bot = bot_instance
        self.sql = sql_instance
        self.f_data = {}



    def test(self, chatid, text):
        self.bot.send_message(chatid, text)

    def parser(self, message, count):
        chat = message.chat.id
        message_id = message.message_id
        self.bot.send_message(chat, message_id)

    def user_to_deathlist(self, message):

        parse = {}
        parse['user_id'] = message.reply_to_message.from_user.id
        parse['first_name'] = message.reply_to_message.from_user.first_name
        parse['last_name'] = message.reply_to_message.from_user.last_name
        parse['username'] = message.reply_to_message.from_user.username
        parse['decl_user_id'] = message.from_user.id
        parse['decl_first_name'] = message.from_user.first_name
        parse['decl_last_name'] = message.from_user.last_name
        parse['decl_username'] = message.from_user.username
        print('user_to_deathlist parse: ', parse)

        return self.sql.add_deathlist(message.chat.id, **parse)

    def deathlist(self, chat_id):
        names = {0: 'score',
                 1: 'first_name',
                 2: 'decl_first_name',
                 3: 'decl_user_id'}
        raw_list = {}
        raw_list = self.sql.get_deathlist(chat_id)
        print('deathlist raw: ', raw_list)
        string = 'Deathlist score:\n\n'
        if raw_list is None:
            return 'Deathlist is empty'
        for i, row in enumerate(raw_list):
            print('2 stage row: ', raw_list[i])
            string += '*{}:* {}\nHaters: {}\n'.format(raw_list[i]['score'], raw_list[i]['first_name'], raw_list[i]['decl_first_name'])
        print('deathlist string: ', string)
        return string

    def f_detector(self, message):
        f_sticker = 'CAACAgIAAxkBAAII0F55JXavA7Y2W63eIHcXV4bSYRAEAAImAQACTptkAqTiIzqwhw-vGAQ'
        f_pack = 'FforRespect'
        if message.content_type == 'sticker':
            sticker_pack_name = message.sticker.set_name
            if sticker_pack_name == f_pack:
                result = self.f_checker(message)
                if result:
                    bot.send_chat_action(message.chat.id, 'typing')
                    time.sleep(3)
                    bot.send_sticker(message.chat.id, f_sticker)  # КОСТЫЛЬ, сообщение не передаётся в функцию
                return True
        elif message.content_type == 'text':
            if str(message.text).lower() == 'f':
                result = self.f_checker(message)
                return result
        else:
            return False

    def f_checker(self, message):
        chat_id = message.chat.id
        message_id = message.message_id
        from_user = message.from_user.id
        # Сравниваем значения с прошлыми записями
        try:
            if self.f_data[chat_id]['msglist'][0] == int(message_id) - 1:  # If previous message F
                self.f_data[chat_id]['msglist'].insert(0, message_id)
                f_list = len(self.f_data[chat_id]['msglist'])
                print('Combo F size {}'.format(f_list))
                if f_list >= 2:  # if X previous message is F
                    self.f_data[chat_id]['msglist'].clear()
                    self.f_data[chat_id]['msglist'].insert(0, message_id)
                    return True
                return False
            elif self.f_data[chat_id]['msglist'][0] <= int(message_id) - 5:  # If last 5 messages NOT f
                print('Short F detected')
                self.f_data[chat_id]['msglist'].clear()
                self.f_data[chat_id]['msglist'].insert(0, int(message_id))
                check = randint(1,10)
                if check >= 8:  # random send F
                    return True
                else:
                    return False
            else:
                self.f_data[chat_id]['msglist'][0] = int(message_id) + 5  # write last F
                print('dupl_f detect')
                return False

        except (KeyError, IndexError):  # If writes is not exist, create new write
            self.f_data[chat_id] = {'msglist': []}
            self.f_data[chat_id]['msglist'].insert(0, int(message_id))
            print('f created')
            check = randint(1, 10)
            if check >= 8:
                return True
            else:
                return False

    def f_selecter(self, list):
        return choice(list)



