from bottle import (
    route, run, template, request, redirect
)
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # 1. Получить значения параметров label и id из GET-запроса
    label = request.query.label
    id = request.query.id
    s = session()

    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    # 3. Изменить значение метки записи на значение label
    s.query(News).filter(News.id == id).update({'label': label})
    
    # 4. Сохранить результат в БД
    s.commit()

    redirect("/news")


@route("/update")
def update_news():
    # 1. Получить данные с новостного сайта
    news = get_news('https://news.ycombinator.com/', n_pages=30)
    s = session()

    # 2. Проверить, каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора
    for post in news:
        if s.query(News).filter(News.title == post['title'],
                                News.author == post['author']).first():
            break
        else:
            s.add(News(**post))

    # 3. Сохранить в БД те новости, которых там нет
    s.commit()

    redirect("/news")

"""
@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
"""

if __name__ == "__main__":
    run(host="localhost", port=8080)
