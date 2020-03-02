# import telebot
# import time
# from telebot import types
from bottoken import *
import re
from bot_func import *

# bot = telebot.TeleBot(BOTTOKEN)
bot.set_update_listener(listener) #регистрация вывода в консоль

user_dict = {}

temp_data = []
temp_messages = {}
# commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "You will die.")
    time.sleep(5)
    bot.send_message(message.chat.id, 'Soon.')

@bot.message_handler(commands=['dolphin'])
def send_dolphin(message):
    keyboard = types.InlineKeyboardMarkup();
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');  # кнопка «Да»
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
    keyboard.add(key_no);
    question = 'Псс. Хочешь немного дельфинов?';
    msg = bot.send_message(message.chat.id, text=question, reply_markup=keyboard)
    if not temp_messages.get(msg.chat.id):
        temp_messages[msg.chat.id] = []
    temp_messages[msg.chat.id].append(msg.message_id)

# новый участник в чяте
@bot.message_handler(func=lambda m: True, content_types=['new_chat_participant'])
def on_user_joins(message):
    def send_welcome(message):
        bot.reply_to(message, "You will die.")
        time.sleep(5)
        bot.send_message(message.chat.id, 'Soon.')


@bot.message_handler(content_types = ['reply_to_message'])
def reply_to_message(message):
    bot.reply_to(message, 'Шо ты от мены хочешь?')

# echo
@bot.message_handler(regexp=r'(?i)echo (.*)')  # потом упростить
def text_answers(message):
    pattern = r'(?i)echo (.*)'
    echo = re.match(pattern, message.text)
    msg = bot.reply_to(message, 'you message :\n' + echo.group(1))
    # msg = bot.send_message(message.chat.id, 'тестовое сообщение для удаления')
    if not temp_messages.get(msg.chat.id):
        temp_messages[msg.chat.id] = []
    temp_messages[msg.chat.id].append(msg.message_id)
    # print (temp_messages)
    time.sleep(5)
    delmessage = temp_messages[msg.chat.id].pop(0)
    bot.delete_message(msg.chat.id, delmessage)


#поиск гифок по запросу (до 9шт
gifsearch = GifSearch(123) #создать общий класс (пока что) FIXME
@bot.message_handler(regexp=r'^(?i)gif (\d) (\w+)(?: |-|:)?(\w*)(?: |-|:)?(\w*)$')  # gif <1_digit> <word> <word_optional>
def send_gif(message):
    pattern = r'^(?i)gif (\d) (\w+)(?: |-|:)?(\w*)(?: |-|:)?(\w*)$'
    search = re.match(pattern, message.text)
    wordlist = []
    word = str(search.group(2))
    count = int(search.group(1))
    if count <= 0:
        return
    wordlist = [str(search.group(3)), str(search.group(4))]
    for pos in wordlist:
        if pos: word += ' ' + pos
    # word = str(search.group(2))
    # word += ' ' + str(search.group(3))
    # word += ' ' + str(search.group(4))
    gifs = searchgif(GIFAPI, 0, word, count)
    gifs = gifsearch.search_gif_tenor(count, word)
    # print (gifs)
    if gifs == None:
        bot.send_message(message.chat.id, '"{}"\n Is not found. Sorry...'.format(word))
    else:
        for gif in gifs:
            bot.send_animation(message.chat.id, gif)

# Если lambda возвращает True - запускается функция
@bot.message_handler(func=lambda m: m.text == 'hello')
def reply_hello(message):
	bot.reply_to(message, message.text)


#ответы лично мне, если начинаются с ~
@bot.message_handler(func=lambda message: message.from_user.id == myid and str(message.text).startswith('~') ) # временно включено
def reply_diman(message):
    #данные
    if str(message.text).replace('~', '', 1) == 'test':
        bot.reply_to(message, 'you message id: {}\n\
you chat type: {}\n\
chat ID: {}\n\
test: '.format (message.message_id, message.chat.type, message.chat.id))

    #просто отправить сообщение
    elif message.text == 'noreply':
        bot.send_message(message.chat.id, 'abc') #Send message to chat

    elif message.text == 'gif':
        bot.send_animation(message.chat.id, 'https://media1.tenor.com/images/c82e08b996362f154dd242d4036ad545/tenor.gif?itemid=9957543')

#парсер всех текстов
@bot.message_handler(content_types = ['text'])
def text_answers(message):
    # print ('text message check \n')
    # Твоё имя
    if message.text == 'msginfo':
        bot.reply_to(message, 'you name: \n\
{} {}\nYou ID: {}'.format(message.from_user.first_name, message.from_user.last_name, message.from_user.id))
    # #КЛОВИОТУРКА
    # elif message.text == 'button':
    #     keyboard = types.InlineKeyboardMarkup();
    #     # keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
    #     key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');  # кнопка «Да»
    #     keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
    #     key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
    #     keyboard.add(key_no);
    #     question = 'Псс. Хочешь немного дельфинов?';
    #     bot.send_message(message.chat.id, text=question, reply_markup=keyboard)

#реакция на клавиатуру
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        # bot.send_message(call.message.chat.id, 'Не сейчас. )')
        dolphinospam(call.message.chat.id)
        try:
            bot.delete_message(call.message.chat.id, temp_messages[call.message.chat.id].pop(0))
        except: print ('del exception')
        # bot.delete_message(temp_data[0]['chatid'], temp_data[0]['msgid'])
    elif call.data == "no":
        bot.answer_callback_query(call.id, show_alert=True, text='ДА И ПОШЁЛ БЫ ТЫ, ПОНЯЛ?\nЧо звал ваще?')
        time.sleep(3)
        try:
            bot.delete_message(call.message.chat.id, temp_messages[call.message.chat.id].pop(0))
        except: print ('del exception')


bot.polling()


