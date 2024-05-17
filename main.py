import telebot
import requests
from bs4 import BeautifulSoup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import time
import hashlib
# pip install lxml

import os
# pip install python-dotenv
from dotenv import load_dotenv  # Для безопасного хранения переменных окружения
load_dotenv()  # Теперь переменные окружения из файла .env доступны


TOKEN_TG_BOT = os.getenv('TOKEN_TG_BOT')
"""Токен для работы с API Telegram"""
bot = telebot.TeleBot(TOKEN_TG_BOT)


ANECDOTICA_API_PID = os.getenv('ANECDOTICA_API_PID')
"""Имя профиля anecdotica"""
ANECDOTICA_API_TOKEN = os.getenv('ANECDOTICA_API_TOKEN')
"""Cекретный токен для работы с API сайта anecdotica.ru"""
ANECDOTICA_API_KEY = os.getenv('ANECDOTICA_API_KEY')
"""Cекретный ключ для работы с API сайта anecdotica.ru"""

query = 'pid=' + ANECDOTICA_API_PID + '&method=getRandItem&uts'
signature = hashlib.md5((query + ANECDOTICA_API_KEY).encode())  # получаем цифровую подпись
url = 'http://anecdotica.ru/api?' + query + '&hash=' + signature.hexdigest()



def parse_anekdot() -> str :
    """Парсит анекдот с сайта и возвращает его"""
    response = requests.get(url=url)
    print(response.status_code)
    print(response.text)
    soup = BeautifulSoup(response.text, 'xml')
    anekdot = soup.find('item').text
    return anekdot


# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handler_messages(message):

    if message.text == '/start':
        # Набор кнопок
        markup = ReplyKeyboardMarkup(row_width=1)
        btn1 = KeyboardButton('Пришли анекдот')
        btn2 = KeyboardButton('Хватит с меня шуточек..')
        markup.add(btn1, btn2)
        bot.send_message(chat_id=message.chat.id,
                         text='Здраствуйте, для анекдотика нажми кнопочку)',
                         reply_markup= markup)
    elif message.text == 'Пришли анекдот':
        text_anekdot = parse_anekdot()
        if text_anekdot:
            bot.send_message(chat_id=message.chat.id, text=text_anekdot)
        else:
            print('ошибочка, шутки нету(')
    elif message.text == 'Хватит с меня шуточек..':
        bot.send_message(chat_id=message.chat.id, text='Ладно, приходите ещё!')




bot.polling(non_stop=True, interval=5)