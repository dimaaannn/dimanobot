from bot_func import bot
from telebot import types

class Messager:
    def __init__(self, bot_instance, sql_instance):
        self.bot = bot_instance
        self.sql = sql_instance

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

        for i, row in enumerate(raw_list):
            print('2 stage row: ', raw_list[i])
            string += '*{}:* {}\nHaters: {}\n'.format(raw_list[i]['score'], raw_list[i]['first_name'], raw_list[i]['decl_first_name'])
        print('deathlist string: ', string)
        return string


