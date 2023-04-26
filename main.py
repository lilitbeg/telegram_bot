"""
Это код для телеграмм-бота для изучения иностранных языков, который умеет выдавать ссылки и заполнять словарь.
На данный момент функционал реализован только для английского языка.
"""

import telebot
from telebot import types
import random

f = open('token.txt', 'r')
token = f.read()
bot = telebot.TeleBot(token)


# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.chat.id, photo=open('welcome.jpg', 'rb'))
    mess = f'Привет, <b>{message.from_user.first_name}</b>. Какой язык ты изучаешь?'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    markup = types.InlineKeyboardMarkup(row_width=1)
    english = types.InlineKeyboardButton('Английский 🇬🇧', callback_data='english')
    french = types.InlineKeyboardButton('Французский 🇫🇷', callback_data='french')
    german = types.InlineKeyboardButton('Немецкий 🇩🇪', callback_data='german')
    other = types.InlineKeyboardButton('Другой', callback_data='other')
    markup.add(english, french, german, other)
    bot.send_message(message.chat.id, 'Выбери язык', reply_markup=markup)


# Обработка команды /menu
@bot.message_handler(commands=['menu'])
def helper(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    one = types.InlineKeyboardButton('Сгенерировать полезную ссылку 👀', url=random.choice(open('links.txt').readlines()))
    two = types.InlineKeyboardButton('Запись слов в словарь 📝', callback_data='words')
    three = types.InlineKeyboardButton('Просмотреть словарь 📖', callback_data='dictionary')
    four = types.InlineKeyboardButton('Посмотреть фильм 📺', callback_data='film')
    markup.add(one, two, three, four)
    bot.send_message(message.chat.id, 'Выбери действие', reply_markup=markup)


# Обработка действий
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'english':
        bot.send_message(call.message.chat.id, 'Fine! 👍')
        bot.send_message(call.message.chat.id, 'Введи команду /menu, чтобы начать')

    elif call.data == 'french' or call.data == 'german' or call.data == 'other':
        bot.send_message(call.message.chat.id, 'К сожалению, этот язык не поддерживается. Выбери другой 😔')
        markup = types.InlineKeyboardMarkup(row_width=1)
        english = types.InlineKeyboardButton('Английский 🇬🇧', callback_data='english')
        french = types.InlineKeyboardButton('Французский 🇫🇷', callback_data='french')
        german = types.InlineKeyboardButton('Немецкий 🇩🇪', callback_data='german')
        other = types.InlineKeyboardButton('Другой', callback_data='other')
        markup.add(english, french, german, other)
        bot.send_message(call.message.chat.id, 'Выбери язык', reply_markup=markup)

    elif call.data == 'words':
        bot.send_message(call.message.chat.id, 'Введи слово на иностранном и перевод <b>ЧЕРЕЗ ЗАПЯТУЮ</b>',
                         parse_mode='html')

    elif call.data == 'dictionary':
        with open('dictionary.txt', 'rb') as file:
            doc = file.read()
        bot.send_document(call.message.chat.id, doc, visible_file_name='MyDictionary')

    elif call.data == 'film':
        markup = types.InlineKeyboardMarkup(row_width=1)
        level_first = types.InlineKeyboardButton('⭐', url=random.choice(open('films_level_first.txt').readlines()))
        level_two = types.InlineKeyboardButton('⭐⭐', url=random.choice(open('films_level_two.txt').readlines()))
        level_three = types.InlineKeyboardButton('⭐⭐⭐', url=random.choice(open('films_level_three.txt').readlines()))
        markup.add(level_first, level_two, level_three)
        bot.send_message(call.message.chat.id, 'Выбери уровень сложности', reply_markup=markup)


# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text(message):
    if len(message.text.split(',')) == 2:
        bot.send_message(message.chat.id, 'Слово успешно добавлено! 🥳')
        d = open('dictionary.txt', 'a')
        d.write(message.text + '\n')
        d.close()


bot.polling()
