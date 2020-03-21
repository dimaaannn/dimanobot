# import telebot
# import time
# from telebot import types
from bottoken import *
import re
from bot_func import *
import dimanobot.roll
import dimanobot.gif
import dimanobot.msg

messager = dimanobot.msg.Messager(bot, botdata)

bot.set_update_listener(listener) #регистрация вывода в консоль
gif_search_dict = {} #словарь запросов гифок
gifsearch = dimanobot.gif.GifSearch(gif_search_dict) #имя экземпляра для поиска гифок
dimanobot.gif.GifSearch.GIFAPI_TENOR = GIFAPI #нужно для класса гифок
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

@bot.message_handler(commands=['deathlist'])
def deathlist(message):
    botdata.db_connect()
    if message.reply_to_message:
        added = messager.user_to_deathlist(message)
        print(added)
        if added == 'INSERT 0 1':
            text = str('User {} added to deathlist'.format(message.reply_to_message.from_user.first_name))
            bot.send_message(message.chat.id, text)
        else:
            text = str('User {} alredy in your deathlist'.format(message.reply_to_message.from_user.first_name))
            bot.send_message(message.chat.id, text)
    else:
        text = messager.deathlist(message.chat.id)
        text += '\nЧтобы добавить хуманса в список, ответь командой /deathlist на его сообщение'
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

#  TESTING
@bot.message_handler(commands=['test'])
def test_reply(message):
    # *bold text*  _italic text_  [text](URL) parse_mode="Markdown"
    reply = None
    if message.reply_to_message:
        reply = message.reply_to_message.message_id
    temp = list ([message.chat.id, message.from_user.id, message.message_id, message.date,\
                  message.text, reply])
    # print('reply :', temp) #reply info
    text = 'some rand text *bold* _italic_\n'
    text += '[text_mention](tg://user?id={})'.format(myid)
    bot.send_message(message.chat.id, text, parse_mode="Markdown")
    messager.parser(message, 3)



# ОТВЕТ НА ВСЕ ТЫЧКИ текстом
@bot.message_handler(func= lambda message: not message.reply_to_message == None \
                                           and message.reply_to_message.from_user.id == bot_id)
# not reply to msg нужна чтобы не выдал ошибку при обращении ко второй части
def bot_reply(message):
    print(message)
    bot.reply_to(message, 'Ты докопаться решил?!!')

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
@bot.message_handler(regexp=dimanobot.gif.GifSearch.re_query)  # gif <1_digit> <word> <word_optional>
def send_gif(message):
    gifs = gifsearch.request(message.text)

    if gifs == None:
        bot.send_message(message.message_id, '"{}"\n Is not found. Sorry...'.format(word))
    else:
        for gif in gifs:
            bot.send_animation(message.chat.id, gif)
    gif_2_hdd.save() #сохранить результат на HDD


# roll dice
@bot.message_handler(regexp=dimanobot.roll.Dice.roll_pattern)
def roll(message):
    roll_answer = str(message.from_user.username) + ' делает бросок на\n'
    roll_answer += dimanobot.roll.dice.roll(message.text)
    bot.send_message(message.chat.id, roll_answer, parse_mode="Markdown")


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


