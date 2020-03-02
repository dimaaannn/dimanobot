import telebot
import time
from bottoken import *

bot = telebot.TeleBot(BOTTOKEN)

class BotTalk:

    creatingmsg = 'answer created'
    def __init__ (self, category, msg):
        self._category = category
        self._msgtext = msg
        return creatingmst + ' category: ' +  str(self.category) + '/ntext:/n' + self._msgtext

commands = ('Я ничего не умею')

# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    help_text = commands
#    for key in commands:  # generate help text out of the commands dictionary defined at the top
#        help_text += "/" + key + ": "
#        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

@bot.message_handler(commands=['start'])
def start_message (message):
	bot.send_message(message.chat.id, 'You will die.')
	time.sleep(3)
	bot.send_message(message.chat.id, 'Soon.')

@bot.message_handler(content_types = ['text'])
def reply_text(message):
	if message.text.lower() == 'привет':
		bot.send_message(message.chat.id, 'это тебя не спасёт')


bot.polling()


