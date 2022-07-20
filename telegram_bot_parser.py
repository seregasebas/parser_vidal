import telebot
import json
import requests
import datetime
from telebot import types #импорт клавиатуры
from telebot import util # Для разбивки большого текста на части
import info_for_bot

bot = telebot.TeleBot('5484059170:AAEUnC5sGBRqSvKlhBpW-Zf1dgPx-5lWuco')

help_info_text = 'парисинг музыкального сайта(рок-музыкантов) : https://www.last.fm/ru/tag/rock/artists\nпарсинг ведется по всем страницам сайта с рок-музфкантами(всего 48 стр)\nНа выходе получаем json файл со следующими данными:\n1. Название группы\n2. ссылка на группу - переходишь и наслаждаешься любимой музыкой\n3. описание группы - краткое описание группы'

#Смотрим id админа(юзера, если не с админского аккаунта сообщение)
# @bot.message_handler(commands = ['start'])
# def start(message):
#     bot.send_message(message.chat.id, message.from_user.id)
#Смотрим id нужного стикера
# @bot.message_handler(content_types=['sticker'])
# def id_stiker(message):
#     bot.send_message(message.chat.id, message.sticker.file_id)

#текстовый список названия групп
data = info_for_bot.rock_group_dict()
text = info_for_bot.groups(data)

@bot.message_handler(commands = ['start'])
def start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1, one_time_keyboard=True)
    yes = types.KeyboardButton(text = 'Yes')
    no = types.KeyboardButton(text = 'No')
    kb.add(yes, no)
    bot.send_message(message.chat.id, 'Приветсвую тебя, парсер готов к работе! Стартуем?', reply_markup=kb)

@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id, help_info_text)

@bot.message_handler(commands = ['all'])
def all(message):
    admin_id = 620361026
    if message.from_user.id == admin_id:
        rock_groups = open('rock_groups.json', 'rb')
        bot.send_document(message.chat.id, rock_groups)
    else:
        bot.send_message(message.chat.id, 'Извните, у вас нет прав доступа((')

@bot.message_handler(func = lambda x: x.text == 'Yes' or x.text == 'No')
def start(message):
    if message.text == 'Yes':       
        my_file = open('file.txt', 'w+')
        my_file.write(text)
        my_file.close()
        my_file = open('file.txt', 'rb')
        bot.send_message(message.chat.id, 'Парсер выполнил свою работу. Список групп в файле')
        bot.send_document(message.chat.id, my_file)
        bot.send_message(message.chat.id, 'Чтобы получить информацию о группе, напиши название группы из файла')
    elif message.text == 'No':
        stiker_id = 'CAACAgIAAxkBAAMaYq9XmfJ5tQx9IkaQcD5qXrizOscAAn0TAAKjd6hLwlg7A4hvzeAkBA'
        bot.send_message(message.chat.id, 'Ок, заходи в следующий раз))')
        bot.send_sticker(message.chat.id, stiker_id)

@bot.message_handler(func = lambda x:x.text)
def dannye(message):
    if message.text in text:
        description_of_group, url_of_group = info_for_bot.description_and_url(data, message.text)
        text_send_to_user = f'<a href = "{url_of_group}">Послушать {message.text}</a>'
        bot.send_message(message.chat.id, f'{message.text}: {description_of_group}')
        bot.send_message(message.chat.id, text_send_to_user, parse_mode='HTML')

@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id, help_info_text)

bot.polling()