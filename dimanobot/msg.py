from bot_func import bot
from telebot import types

class Messager:
    def __init__(self, instance):
        self.bot = instance

    def test(self, chatid, text):
        self.bot.send_message(chatid, text)

    def parser(self, message, count):
        chat = message.chat.id
        message_id = message.message_id
        self.bot.send_message(chat, message_id)


