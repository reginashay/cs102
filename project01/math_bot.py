import requests
import config
import functio
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
    key.row('Тригонометрия', 'Стереометрия')
    key.row('Неравенства', 'Планиметрия')
    key.row('Оптимизация', 'Задачи с параметром')
    key.row('Числа и их свойства')

    r1 = 'Добрый день! Здесь для вас собраны разные задачи для подготовки '
    r2 = 'к ЕГЭ по математике и просто для поддержания мозга в тонусе.'
    r = '\n\n'
    r3 = 'Для перехода в следующее меню выберите тему ниже.'

    msg = bot.send_message(message.chat.id, r1 + r2 + r + r3, reply_markup=key)
    bot.register_next_step_handler(msg, first_action)


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
        number = random.randint(3897, 3910)
    if message.text == 'Случайная задача только с ответом':
        number = random.randint(4051, 4055)
        bot.send_photo(message.chat.id, photo='')
    if message.text == 'В главное меню':
        startBot(message)


# 14
def ster(message):
    if message.text == 'Случайная задача с полным решением':
        number = random.randint(3911, 3948)
    if message.text == 'Случайная задача только с ответом':
        number = random.randint(4056, 4060)
    if message.text == 'В главное меню':
        startBot(message)


# 15
def uneq(message):
    if message.text == 'Случайная задача с полным решением':
        number = random.randint(3949, 3964)
    if message.text == 'Случайная задача только с ответом':
        number = random.randint(4061, 4065)
    if message.text == 'В главное меню':
        startBot(message)


# 16
def plan(message):
    if message.text == 'Случайная задача с полным решением':
        number = random.randint(3965, 3995)
    if message.text == 'Случайная задача только с ответом':
        number = random.randint(4066, 4070)
    if message.text == 'В главное меню':
        startBot(message)


# 17
def opt(message):
    if message.text == 'Случайная задача с полным решением':
        number = random.randint(3996, 4011)
    if message.text == 'Случайная задача только с ответом':
        number = random.randint(4071, 4075)
    if message.text == 'В главное меню':
        startBot(message)


# 18
def param(message):
    if message.text == 'Случайная задача с полным решением':
        number = random.randint(4012, 4037)
    if message.text == 'Случайная задача только с ответом':
        number = random.randint(4076, 4080)
    if message.text == 'В главное меню':
        startBot(message)


# 19
def num_theo(message):
    if message.text == 'Случайная задача с полным решением':
        number = random.randint(4038, 4050)
    if message.text == 'Случайная задача только с ответом':
        number = random.randint(4081, 4085)
    if message.text == 'В главное меню':
        startBot(message)


# more?


if __name__ == '__main__':
    bot.polling(none_stop=True)
