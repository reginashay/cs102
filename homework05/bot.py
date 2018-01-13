import datetime
import requests
import config
import telebot
from bs4 import BeautifulSoup


bot = telebot.TeleBot(config.access_token)


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    if week == '0/':
        week = ''
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на день недели
    if day == '/monday' or day == '/sunday':
        schedule_table = soup.find("table", attrs={"id": "1day"})
    elif day == '/tuesday':
        schedule_table = soup.find("table", attrs={"id": "2day"})
    elif day == '/wednesday':
        schedule_table = soup.find("table", attrs={"id": "3day"})
    elif day == '/thursday':
        schedule_table = soup.find("table", attrs={"id": "4day"})
    elif day == '/friday':
        schedule_table = soup.find("table", attrs={"id": "5day"})
    elif day == '/saturday':
        schedule_table = soup.find("table", attrs={"id": "6day"})

    # Проверяем, есть ли занятия в указанный день
    if schedule_table is not None:

        # Время проведения занятий
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]

        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]
        # Удаление управляющих конструкций из списка дисциплин
        for i in range(len(lessons_list)):
            lessons_list[i] = lessons_list[i].replace('\n', '')
            lessons_list[i] = lessons_list[i].replace('\t', '')

        # Номер аудитории
        aud_list = schedule_table.find_all("td", attrs={"class": "room"})
        aud_list = [aud.dd.text for aud in aud_list]

        return times_list, locations_list, lessons_list, aud_list

    # В указанный день занятий нет
    else:
        return 0


def get_first_near(group):
    """ Получить первое занятие следующего дня """
    today = datetime.datetime.now().isoweekday()
    if today == 1:
        day = '/tuesday'
    elif today == 2:
        day = '/wednesday'
    elif today == 3:
        day = '/thursday'
    elif today == 4:
        day = '/friday'
    elif today == 5:
        day = '/saturday'
    elif today == 6:
        day = '/monday'
    if day == '/monday':
        if int(datetime.datetime.today().strftime('%U')) % 2 == 1:
            week = 1
        else:
            week = 2
    else:
        if int(datetime.datetime.today().strftime('%U')) % 2 == 1:
            week = 2
        else:
            week = 1
    web_page = get_page(group, week)
    return parse_schedule(web_page, day)


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    day, group, week = message.text.split()

    if 65 <= ord(group[0]) <= 90:
        web_page = get_page(group, week)
        test = parse_schedule(web_page, day)
        if test == 0:
            resp = '<b>Занятий нет.</b>'
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
        else:
            times_lst, locations_lst, lessons_lst, aud_lst = test
            resp = ''
            for time, location, lesson, aud in zip(times_lst, locations_lst, lessons_lst, aud_lst):
                resp += '<b>{}</b>, {}, {}. {}\n'.format(time, location, lesson, aud)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
    else:
        r = 'Ошибка: номер группы должен начинаться с заглавной буквы.'
        bot.send_message(message.chat.id, r, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    _, group = message.text.split()

    if 65 <= ord(group[0]) <= 90:
        today = datetime.datetime.now().isoweekday()
        if today == 7:
            day = '/monday'
        else:
            if today == 1:
                day = '/monday'
            elif today == 2:
                day = '/tuesday'
            elif today == 3:
                day = '/wednesday'
            elif today == 4:
                day = '/thursday'
            elif today == 5:
                day = '/friday'
            elif today == 6:
                day = '/saturday'

            if int(datetime.datetime.today().strftime('%U')) % 2 == 1:
                week = 2
            else:
                week = 1
            web_page = get_page(group, week)

            test = parse_schedule(web_page, day)
            if test == 0:
                result = get_first_near(group)
                times_lst, locations_lst, lessons_lst, aud_lst = result
                resp = '<b>Ближайшее занятие:</b>\n'
                resp += '<b>{}</b>, {}, {}. {}\n'.format(times_lst[0], locations_lst[0], lessons_lst[0], aud_lst[0])
                bot.send_message(message.chat.id, resp, parse_mode='HTML')
            else:
                times_lst, locations_lst, lessons_lst, aud_lst = test
                num = 0
                i = 0
                for i in range(len(times_lst)):
                    _, time = times_lst[i].split('-')
                    time_h, time_m = time.split(':')
                    time = int(time_h + time_m)
                    now = int(str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute))
                    if now < time:
                        resp = '<b>Ближайшее занятие:</b>\n'
                        resp += '<b>{}</b>, {}, {}. {}\n'.format(times_lst[num], locations_lst[num], lessons_lst[num], aud_lst[num])
                        bot.send_message(message.chat.id, resp, parse_mode='HTML')
                        i = 1
                        break
                    num += 1
                    if i == 0:
                        if now < time:
                            resp = '<b>Ближайшее занятие:</b>\n'
                            resp += '<b>{}</b>, {}, {}. {}\n'.format(times_lst[num], locations_lst[num], lessons_lst[num], aud_lst[num])
                            bot.send_message(message.chat.id, resp, parse_mode='HTML')
                            break
                        else:
                            result = get_first_near(group)
                            times_lst, locations_lst, lessons_lst, aud_lst = result
                            resp = '<b>Ближайшее занятие:</b>\n'
                            resp += '<b>{}</b>, {}, {}. {}\n'.format(times_lst[0], locations_lst[0], lessons_lst[0], aud_lst[0])
                            bot.send_message(message.chat.id, resp, parse_mode='HTML')
    else:
        r = 'Ошибка: номер группы должен начинаться с заглавной буквы.'
        bot.send_message(message.chat.id, r, parse_mode='HTML')


@bot.message_handler(commands=['tomorrow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    _, group = message.text.split()

    if 65 <= ord(group[0]) <= 90:
        if int(datetime.datetime.today().strftime('%U')) % 2 == 1:
            week = 2
        else:
            week = 1

        today = datetime.datetime.now()
        tom = today
        if today.isoweekday() == 6:
            tom += datetime.timedelta(days=2)
        else:
            tom += datetime.timedelta(days=1)
        if tom.isoweekday() == 1:
            tom = '/monday'
        elif tom.isoweekday() == 2:
            tom = '/tuesday'
        elif tom.isoweekday() == 3:
            tom = '/wednesday'
        elif tom.isoweekday() == 4:
            tom = '/thursday'
        elif tom.isoweekday() == 5:
            tom = '/friday'
        elif tom.isoweekday() == 6:
            tom = '/saturday'

        web_page = get_page(group, week)
        test = parse_schedule(web_page, tom)
        if test == 0:
            bot.send_message(message.chat.id, '<b>Занятий нет.</b>', parse_mode='HTML')
        else:
            times_lst, locations_lst, lessons_lst, aud_lst = test
            resp = '<b>Расписание на завтра:</b>\n'
            for time, location, lesson, aud in zip(times_lst, locations_lst, lessons_lst, aud_lst):
                resp += '<b>{}</b>, {}, {}. {}\n'.format(time, location, lesson, aud)

            bot.send_message(message.chat.id, resp, parse_mode='HTML')

    else:
        r = 'Ошибка: номер группы должен начинаться с заглавной буквы.'
        bot.send_message(message.chat.id, r, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    _, group, week = message.text.split()

    if 65 <= ord(group[0]) <= 90:
        if int(week) == 1:
            resp = '<b>Четная неделя:</b>\n\n'
        elif int(week) == 2:
            resp = '<b>Нечетная неделя:</b>\n\n'
        elif int(week) == 0:
            resp = '<b>Обе недели:</b>\n\n'

        web_page = get_page(group, week)
        days = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday']
        rus_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

        for i in range(len(days)):
            st = '<b>' + rus_days[i] + '</b>' + ':\n'
            resp += st
            test = parse_schedule(web_page, days[i])
            if test == 0:
                resp += '<b>Занятий нет.\n</b>'
            else:
                times_lst, locations_lst, lessons_lst, aud_lst = test
                for time, location, lesson, aud in zip(times_lst, locations_lst, lessons_lst, aud_lst):
                    resp += '<b>{}</b>, {}, {}. {}\n'.format(time, location, lesson, aud)
            resp += '\n'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')

    else:
        r = 'Ошибка: номер группы должен начинаться с заглавной буквы.'
        bot.send_message(message.chat.id, r, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
