from bottle import route, run, template, request, redirect
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
import string


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


@route("/add_label_recs/")
def add_label_recs():
    # 1. Получить значения параметров label и id из GET-запроса
    label = request.query.label
    id = request.query.id
    s = session()

    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    # 3. Изменить значение метки записи на значение label
    s.query(News).filter(News.id == id).update({'label': label})

    # 4. Сохранить результат в БД
    s.commit()

    redirect("/recommendations")

@route("/update")
def update_news():
    # 1. Получить данные с новостного сайта
    news = get_news('https://news.ycombinator.com', n_pages=1)
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


@route('/recommendations')
def recommendations():
	# 1. Получить список неразмеченных новостей из БД
	rows = s.query(News).filter(News.label == None).all()

	# 2. Получить прогнозы для каждой новости
	good, maybe, never = [], [], []
	for row in rows:
		[prediction] = model.predict([clean(row.title).lower()])
		if prediction == 'good':
			good.append(row)
	for row in rows:
		[prediction] = model.predict([clean(row.title).lower()])
		if prediction == 'maybe':
			maybe.append(row)
	for row in rows:
		[prediction] = model.predict([clean(row.title).lower()])
		if prediction == 'never':
			never.append(row)

	# 3. Вывести ранжированную таблицу с новостями
	return template('news_recommendations', good=good, maybe=maybe, never=never)

def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


if __name__ == "__main__":
    s = session()
    rows = s.query(News).filter(News.label != None).all()
    X_train = [clean(row.title).lower() for row in rows]
    y_train = [row.label for row in rows]
    model = NaiveBayesClassifier()
    model.fit(X_train, y_train)

    run(host="localhost", port=8080)
