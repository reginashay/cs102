import requests
import config
import telebot
from telebot import types
from bs4 import BeautifulSoup
import random


bot = telebot.TeleBot(config.access_token)


def get_page(num):
    #num = str(num)
    #url = config.domain,
    #response = requests.get(url)
    #web_page = response.text
    #return web_page
    pass


def parse_page(web_page):
    #soup = BeautifulSoup(web_page, "html5lib")
    #soup.find()
    pass


@bot.message_handler(commands=['start'])
def startBot(message):

    key = types.ReplyKeyboardMarkup()
    key.row('Список тем')
    key.row('Почитать')

    r1 = 'Добрый день! Здесь для вас собраны разные задачи для подготовки '
    r2 = 'к ЕГЭ по математике и просто для поддержания мозга в тонусе.'
    r = '\n\n'
    r3 = 'Для перехода в следующее меню выберите тему ниже.'

    msg = bot.send_message(message.chat.id, r1 + r2 + r + r3, reply_markup=key)
    bot.register_next_step_handler(msg, list_of_themes)


def list_of_themes(message):

    if message.text == 'Список тем':
        key = types.ReplyKeyboardMarkup()
        key.row('Тригонометрия', 'Стереометрия')
        key.row('Неравенства', 'Планиметрия')
        key.row('Оптимизация', 'Задачи с параметром')
        key.row('Числа и их свойства')

        r = 'Выберите тему, чтобы продолжить:'
        msg = bot.send_message(message.chat.id, r, reply_markup=key)
        bot.register_next_step_handler(msg, first_action)

    if message.text == 'Почитать':
        key = types.ReplyKeyboardMarkup()
        key.row('Начать чтение')
        key.row('Вернуться в главное меню')

        resp = 'Здесь вы можете почитать рассказ '
        msg = bot.send_message(message.chat.id, resp, reply_markup=key)
        bot.register_next_step_handler(msg, handle_book)


def handle_book(message):
    if message.text == 'Начать чтение':

        def open_book():
            with open('the_orient_express.txt', 'r') as file:
                BOOK = file.read() # открываем книгу и записываем её в BOOK
            return BOOK

        def pages_keyboard(start, stop):
            # Формируем Inline-кнопки для перехода по страницам.
            BOOK = open_book()
            keyboard = types.InlineKeyboardMarkup()
            btns = []
            if start > 0: btns.append(types.InlineKeyboardButton(
                text='back', callback_data='to_{}'.format(start - 700)))

            btns.append(types.InlineKeyboardButton(
                text='Type "/start" if you want to exit',
                callback_data='to_{}'.format()))

            if stop < len(BOOK): btns.append(types.InlineKeyboardButton(
                text='forward', callback_data='to_{}'.format(stop)))
            keyboard.add(*btns)
            return keyboard # возвращаем объект клавиатуры

        def start_reading(message):
            # Начинаем
            BOOK = open_book()
            bot.send_message(message.chat.id, BOOK[:700], parse_mode='Markdown',
                reply_markup=pages_keyboard(0, 700))

        start_reading(message)

        @bot.callback_query_handler(func=lambda c: c.data)
        def pages(c):
            # Редактируем сообщение каждый раз, когда пользователь переходит по страницам.
            BOOK = open_book()
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=BOOK[int(c.data[3:]):int(c.data[3:]) + 700],
                parse_mode='Markdown',
                reply_markup=pages_keyboard(int(c.data[3:]), 
                    int(c.data[3:]) + 700))

    if message.text == 'Вернуться в главное меню':
        startBot(message)


def handle_randomness(message):
    key = types.ReplyKeyboardMarkup()
    key.row('Случайная задача с полным решением')
    key.row('Случайная задача только с ответом')
    key.row('В главное меню')
    resp = 'Выберите следующее действие:'
    msg = bot.send_message(message.chat.id, resp, reply_markup=key)
    return msg


def first_action(message):
    if message.text == 'Тригонометрия':
        msg = handle_randomness(message)
        bot.register_next_step_handler(msg, trigo)
    if message.text == 'Стереометрия':
        msg = handle_randomness(message)
        bot.register_next_step_handler(msg, ster)
    if message.text == 'Неравенства':
        msg = handle_randomness(message)
        bot.register_next_step_handler(msg, uneq)
    if message.text == 'Планиметрия':
        msg = handle_randomness(message)
        bot.register_next_step_handler(msg, plan)
    if message.text == 'Оптимизация':
        msg = handle_randomness(message)
        bot.register_next_step_handler(msg, opt)
    if message.text == 'Задачи с параметром':
        msg = handle_randomness(message)
        bot.register_next_step_handler(msg, param)
    if message.text == 'Числа и их свойства':
        msg = handle_randomness(message)
        bot.register_next_step_handler(msg, num_theo)


# 13
def trigo(message):
    if message.text == 'Случайная задача с полным решением':
        domain = 'https://pp.userapi.com/c824501/v824501235/867'
        a = '55/bx1HklCnvBY.jpg'
        b = '5e/es7WwiUZlPA.jpg'
        c = '67/gcz9TN29W98.jpg'
        d = '70/IOJPUU1ufrY.jpg'
        e = 'b8/nWO5N-dgRYU.jpg'
        L = [a, b, c, d, e]
        pic = domain + random.choice(L)
        bot.send_photo(message.chat.id, photo=pic)
        
    if message.text == 'Случайная задача только с ответом':
        bot.send_message(message.chat.id, 'hi', parse_mode='HTML')
        
    if message.text == 'В главное меню':
        startBot(message)


# 14
def ster(message):
    if message.text == 'Случайная задача с полным решением':
        pass
    if message.text == 'Случайная задача только с ответом':
        pass
    if message.text == 'В главное меню':
        startBot(message)


# 15
def uneq(message):
    if message.text == 'Случайная задача с полным решением':
        pass
    if message.text == 'Случайная задача только с ответом':
        pass
    if message.text == 'В главное меню':
        startBot(message)


# 16
def plan(message):
    if message.text == 'Случайная задача с полным решением':
        pass
    if message.text == 'Случайная задача только с ответом':
        pass
    if message.text == 'В главное меню':
        startBot(message)


# 17
def opt(message):
    if message.text == 'Случайная задача с полным решением':
        pass
    if message.text == 'Случайная задача только с ответом':
        pass
    if message.text == 'В главное меню':
        startBot(message)


# 18
def param(message):
    if message.text == 'Случайная задача с полным решением':
        pass
    if message.text == 'Случайная задача только с ответом':
        pass
    if message.text == 'В главное меню':
        startBot(message)


# 19
def num_theo(message):
    if message.text == 'Случайная задача с полным решением':
        pass
    if message.text == 'Случайная задача только с ответом':
        pass
    if message.text == 'В главное меню':
        startBot(message)


# more?


if __name__ == '__main__':
    bot.polling(none_stop=True)
