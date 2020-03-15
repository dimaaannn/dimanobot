# import telebot
# import time
# from telebot import types
from bottoken import *
import re
from bot_func import *


bot.set_update_listener(listener) #регистрация вывода в консоль
gif_search_dict = {} #словарь запросов гифок
gifsearch = GifSearch(gif_search_dict) #имя экземпляра для поиска гифок
GifSearch.GIFAPI_TENOR = GIFAPI #нужно для класса гифок
gif_2_hdd = DataSaver('botdata', gif_search_dict=gif_search_dict)
print ('gif dictionary loaded is {}'.format(gif_2_hdd.load()))

temp_messages = {} #ID messages for deleting

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


@bot.message_handler(commands=['reply'])
def reply_to_message(message):
    msg = bot.reply_to(message, 'Шо ты от мены хочешь?')
    bot.register_for_reply(msg, lambda mess: bot.reply_to(mess, 'Мне пофиг')) #TODO довести до ума

@bot.message_handler(commands=['stickerid'])
def ask_sticker_reply(message):
    msg = bot.reply_to(message, 'reply this message with sticker')
    bot.register_for_reply(msg, get_sticker_id)

def get_sticker_id(message):
    # message_id = message.message_id
    # chat_id = message.chat.id
    print(message.reply_to_message)
    if message.content_type == 'sticker':
        sticker_obj = message.sticker
        sticker_id = getattr(sticker_obj, 'file_id')
        set_name = message.sticker.set_name
        emoji = message.sticker.emoji
        file_size = message.sticker.file_size
        # print ('sticker id:\n', sticker_id)
        # print (type (sticker_id))
        bot.reply_to(message, 'Sticker set name: {}\nEmoji: {}\nFile size: {}\nStickerID:\n{}\n ' .format\
            (set_name, emoji, file_size, sticker_id))
    else: ask_sticker_reply(message)

@bot.message_handler(commands=['test'])
def ask_sticker_reply(message):
    temp = message.reply_to_message.from_user.id
    print('reply :', temp)

# ОТВЕТ НА ВСЕ ТЫЧКИ
@bot.message_handler(func= lambda message: message.reply_to_message.from_user.id == 893733592)
def bot_reply(message):
    bot.reply_to(message, 'Ты чё, докопаться решил?!!')

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
# gifsearch = GifSearch(gif_search_dict) #создать общий класс (пока что)
@bot.message_handler(regexp=r'^(?i)gif (\d) (\w+)(?: |-|:)?(\w*)(?: |-|:)?(\w*)$')  # gif <1_digit> <word> <word_optional>
def send_gif(message):
    pattern = r'(?i)gif (\d) (\w+)(?: |-|:)?(\w*)(?: |-|:)?(\w*)$'
    search = re.match(pattern, message.text)
    wordlist = []
    word = str(search.group(2))
    count = int(search.group(1))
    if count <= 0:
        return
    wordlist = [str(search.group(3)), str(search.group(4))]
    for pos in wordlist:
        if pos: word += ' ' + pos
    gifs = gifsearch.search_gif_tenor(count, word)
    # print (gifs)
    if gifs == None:
        bot.send_message(message.chat.id, '"{}"\n Is not found. Sorry...'.format(word))
    else:
        for gif in gifs:
            bot.send_animation(message.chat.id, gif)
    gif_2_hdd.save() #сохранить результат на HDD

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

#реакция на вызов дельфиноспама
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        # bot.send_message(call.message.chat.id, 'Не сейчас. )')
        dolphinospam(gifsearch.search_gif_tenor, call.message.chat.id)
        gifsearch.search_gif_tenor(3,'str')
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


