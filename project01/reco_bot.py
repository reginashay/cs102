import requests
import config
import telebot
from bs4 import BeautifulSoup

"""
This bot gives you recommendations on books (basically)
Or maybe this bot gives rec-s on anything somehow related to the specified theme
(e.g. detective/sci-fi/etc. books, movies, series etc.)
"""


bot = telebot.TeleBot(config.access_token)


def get_page():
    pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
