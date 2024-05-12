# pip install requests
# pip install beautifulsoup4
import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import time
import hashlib
# pip install lxml


bot = telebot.TeleBot(TOKEN)




# формируем строку параметров
query = 'pid=' + PID + '&method=getRandItem&uts=' + str(int(time.time()))

signature = hashlib.md5((query + KEY).encode())  # получаем цифровую подпись
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
        btn2 = KeyboardButton('Хватит')
        markup.add(btn1, btn2)
        bot.send_message(chat_id=message.chat.id,
                         text='Здравствуйте! Для получения анекдота нажмите кнопку',
                         reply_markup = markup
                         )
    
    elif message.text == 'Пришли анекдот':
        text_anekdot = parse_anekdot()
        if text_anekdot:
            bot.send_message(chat_id=message.chat.id, text=text_anekdot)
        else:
            print('ОШИБКА! АНЕДКОТ НЕ ПОЛУЧЕН!')
    
    elif message.text == 'Хватит':
        bot.send_message(chat_id=message.chat.id, text='Ок! Приходите еще!')


bot.polling()



