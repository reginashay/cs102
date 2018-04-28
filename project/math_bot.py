import requests
import config
import telebot
from telebot import types
import random


bot = telebot.TeleBot(config.access_token)


@bot.message_handler(commands=['start'])
def startBot(message):
    """ Запускаем бота """
    key = types.ReplyKeyboardMarkup()
    key.row('Список тем')
    key.row('📖 Почитать')

    r1 = 'Добрый день! Здесь для вас собраны разные задачи для подготовки '
    r2 = 'к ЕГЭ по математике и просто для поддержания мозга в тонусе.'
    r = '\n\n'
    r3 = 'Для перехода в следующее меню выберите тему ниже.'

    msg = bot.send_message(message.chat.id, r1 + r2 + r + r3, reply_markup=key)
    bot.register_next_step_handler(msg, list_of_themes)


def list_of_themes(message):
    """Выбираем тему из предложенных, либо решаем почитать"""
    if message.text == 'Список тем':
        key = types.ReplyKeyboardMarkup()
        key.row('Тригонометрия', 'Стереометрия')
        key.row('Неравенства', 'Планиметрия')
        key.row('Числа и их свойства')

        r = '📚 Выберите тему, чтобы продолжить:'
        msg = bot.send_message(message.chat.id, r, reply_markup=key)
        bot.register_next_step_handler(msg, first_action)

    if message.text == '📖 Почитать':
        key = types.ReplyKeyboardMarkup()
        key.row('Начать чтение')
        key.row('Вернуться в главное меню')

        resp = '📖 Здесь вы можете отвлечься и почитать классическую литературу.'
        msg = bot.send_message(message.chat.id, resp, reply_markup=key)
        bot.register_next_step_handler(msg, handle_book)


def handle_book(message):
    if message.text == 'Начать чтение':

        def open_book():
            """ Открываем книгу и записываем её в BOOK """
            with open('the_orient_express.txt', 'r') as file:
                BOOK = file.read()
            return BOOK

        def pages_keyboard(start, stop):
            """ Создаем Inline-кнопки для перехода по страницам """
            BOOK = open_book()
            keyboard = types.InlineKeyboardMarkup()
            btns = []
            if start > 0:
                btns.append(types.InlineKeyboardButton(
                    text='back', callback_data='to_{}'.format(start - 700)))
            btns.append(types.InlineKeyboardButton(
                text='"/start" to exit',
                url='https://olymp.mipt.ru/'))
            if stop < len(BOOK):
                btns.append(types.InlineKeyboardButton(
                    text='forward', callback_data='to_{}'.format(stop)))
            keyboard.add(*btns)
            return keyboard

        def start_reading(message):
            """ Начинаем с первой страницы """
            BOOK = open_book()
            bot.send_message(message.chat.id, BOOK[:700],
                             parse_mode='Markdown',
                             reply_markup=pages_keyboard(0, 700))

        start_reading(message)  # Запускаем сам режим чтения

        @bot.callback_query_handler(func=lambda c: c.data)
        def pages(c):
            """ Редактируем сообщение каждый раз,
                когда пользователь переходит по страницам """
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
    """ Выбираем тип задачи """
    key = types.ReplyKeyboardMarkup()
    key.row('Случайная задача с полным решением')
    key.row('Случайная задача только с ответом')
    key.row('В главное меню')
    resp = '📚 Выберите следующее действие:'
    msg = bot.send_message(message.chat.id, resp, reply_markup=key)
    return msg


def handle_randnums(message):
    key = types.ReplyKeyboardMarkup()
    key.row('Случайная задача')
    key.row('В главное меню')
    resp = '📚 Выберите следующее действие:'
    msg = bot.send_message(message.chat.id, resp, reply_markup=key)
    return msg


def first_action(message):
    """ Действия в зависимости от выбранной темы задания """
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
    if message.text == 'Числа и их свойства':
        msg = handle_randnums(message)
        bot.register_next_step_handler(msg, num_theo)


def listing(message, domain, a, b, c, d, e):
    """ Отправка картинки с заданием пользователю """
    L = [a, b, c, d, e]
    pic = domain + random.choice(L)
    bot.send_photo(message.chat.id, photo=pic)
    r = 'Наберите или нажмите /start, чтобы вернуться в главное меню и выбрать другое действие.'
    bot.send_message(message.chat.id, r, parse_mode='HTML')


"""
THEMES
Картинки с задачками недоступны, требуется модификация этой части.
"""


def trigo(message):
    """ Тригонометрия """
    if message.text == 'Случайная задача с полным решением':
        domain = 'https://pp.userapi.com/c824501/v824501235/867'
        a = '55/bx1HklCnvBY.jpg'
        b = '5e/es7WwiUZlPA.jpg'
        c = '67/gcz9TN29W98.jpg'
        d = '70/IOJPUU1ufrY.jpg'
        e = 'b8/nWO5N-dgRYU.jpg'
        listing(message, domain, a, b, c, d, e)
    if message.text == 'Случайная задача только с ответом':
        domain = 'https://pp.userapi.com/c8'
        a = '40025/v840025299/37972/sXNZ5OPTEI0.jpg'
        b = '41039/v841039299/5ce60/zErNd8fk1aI.jpg'
        c = '40537/v840537299/45731/kjYL84Lr4go.jpg'
        d = '24409/v824409295/87fd9/NZJXiISmSm4.jpg'
        e = '40133/v840133295/66fb8/hRX_Duac_lY.jpg'
        listing(message, domain, a, b, c, d, e)
    if message.text == 'В главное меню':
        startBot(message)


def ster(message):
    """ Стереометрия """
    if message.text == 'Случайная задача с полным решением':
        domain = 'https://pp.userapi.com/c840721/v840721235/45e'
        a = '30/lOv9xgUjBOc.jpg'
        b = '39/WdmO2IfSdNQ.jpg'
        c = '42/EoaeGb4P-MU.jpg'
        d = '4b/YSOXrpR51DM.jpg'
        e = '54/8Zu5pp9lKJ4.jpg'
        listing(message, domain, a, b, c, d, e)
    if message.text == 'Случайная задача только с ответом':
        domain = 'https://pp.userapi.com/c'
        a = '841626/v841626883/55090/NOiMHkpcGTY.jpg'
        b = '840324/v840324883/46120/Vm8aNmn3Y3c.jpg'
        c = '831109/v831109883/506fb/b9dlQyyGY8I.jpg'
        d = '621702/v621702883/57e3e/BDB3myG5lwQ.jpg'
        e = '841137/v841137883/5ca6b/Yb2gbg6mP0s.jpg'
        listing(message, domain, a, b, c, d, e)
    if message.text == 'В главное меню':
        startBot(message)


def uneq(message):
    """ Неравенства """
    if message.text == 'Случайная задача с полным решением':
        domain = 'https://pp.userapi.com/c824202/v824202235/87c'
        a = '1a/-MA3Ppk-9X8.jpg'
        b = '23/iZ2XR8vOJdg.jpg'
        c = '2c/Bd-rugmuzjQ.jpg'
        d = '35/Yv6aTFS6mNY.jpg'
        e = '3e/Xw2qfXgAcyk.jpg'
        listing(message, domain, a, b, c, d, e)
    if message.text == 'Случайная задача только с ответом':
        domain = 'https://pp.userapi.com/c8'
        a = '41531/v841531883/57088/L3SP1rXq1aE.jpg'
        b = '31209/v831209883/47384/UZmOgIyHpm4.jpg'
        c = '34100/v834100883/8bb46/U5Gvn491FvI.jpg'
        d = '41029/v841029883/5f864/61DEWUPksOQ.jpg'
        e = '40627/v840627883/451a0/WSA_JSYSmP4.jpg'
        listing(message, domain, a, b, c, d, e)
    if message.text == 'В главное меню':
        startBot(message)


def plan(message):
    """ Планиметрия """
    if message.text == 'Случайная задача с полным решением':
        domain = 'https://pp.userapi.com/c834300/v834300235/8c2'
        a = '6f/X4G1dCHG5iE.jpg'
        b = '78/P0ZLzEg3PSk.jpg'
        c = '8a/GwNsgMnsHFo.jpg'
        d = 'a5/7HjkSlQBpaU.jpg'
        e = 'ae/Lim71Yhev2U.jpg'
        listing(message, domain, a, b, c, d, e)
    if message.text == 'Случайная задача только с ответом':
        domain = 'https://pp.userapi.com/c8'
        a = '34301/v834301883/859f2/eRYTJ_bc6rk.jpg'
        b = '34302/v834302883/89640/Rvty3FsQrhQ.jpg'
        c = '40337/v840337883/4275e/VVXAef_LNAE.jpg'
        d = '41138/v841138883/5dccc/g6P295ck6SY.jpg'
        e = '30208/v830208883/51bf1/LjG-ql-akWg.jpg'
        listing(message, domain, a, b, c, d, e)
    if message.text == 'В главное меню':
        startBot(message)


def num_theo(message):
    """ Числа и их свойства """
    if message.text == 'Случайная задача':
        domain = 'https://pp.userapi.com/c824604/v824604235/8b'
        a = '495/_N4wD8U4Evw.jpg'
        b = '49d/-AkWxL2KFos.jpg'
        c = '4a6/lqiui_MKj-Y.jpg'
        d = '4af/LG0VMQIRe9g.jpg'
        e = '501/wWRP0EKaGpo.jpg'
        listing(message, domain, a, b, c, d, e)
    if message.text == 'В главное меню':
        startBot(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
