import psycopg2
import psycopg2.extras
from pprint import pprint as pp
from tabulate import tabulate

conn = psycopg2.connect("host=localhost port=5432 dbname=odscourse user=postgres password=secret")
cursor = conn.cursor() # cursor_factory=psycopg2.extras.DictCursor)

def fetch_all(cursor):
    colnames = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    return [{colname:value for colname, value in zip(colnames, record)} for record in records]


"""
cursor.execute("")
records = cursor.fetchall()
print(records)
"""


""" ЗАДАНИЕ 1. Сколько мужчин и женщин представлено в этом наборе данных? """

cursor.execute(
    """
    SELECT gender, AVG(height), COUNT(gender) AS num
    FROM mlboot
    GROUP BY gender
    """
)
print('TASK 1')
print(tabulate(fetch_all(cursor), "keys", "psql"))


""" ЗАДАНИЕ 2. Кто в среднем реже указывает, что употребляет алкоголь – мужчины или женщины? """

cursor.execute(
    """
    SELECT gender, AVG(alco::int) AS alco
    FROM mlboot
    GROUP BY gender
    """
)
print('TASK 2')
print(tabulate(fetch_all(cursor), "keys", "psql"))


""" ЗАДАНИЕ 3. Во сколько раз (округленно, round) процент курящих среди мужчин больше, чем процент    # FIX IT
    курящих среди женщин (по крайней мере, по этим анкетным данным)? """

cursor.execute(
    """
    SELECT (SELECT ROUND(AVG(smoke::int) * 100, 2) FROM mlboot WHERE gender=2) /
           (SELECT ROUND(AVG(smoke::int) * 100, 2) FROM mlboot WHERE gender=1) AS div
    FROM mlboot
    LIMIT '1'
    """
)
print('TASK 3')
print(tabulate(fetch_all(cursor), "keys", "psql"))


""" ЗАДАНИЕ 4. В чём здесь измеряется возраст? На сколько месяцев (примерно) отличаются медианные значения
    возраста курящих и некурящих? """

cursor.execute(
    """
    SELECT ABS((SELECT median(age) / 30 FROM mlboot WHERE smoke='1') - \
           (SELECT median(age) / 30 FROM mlboot WHERE smoke='0'))::int AS diff
    FROM mlboot
    LIMIT '1'
    """
)
print('TASK 4')
print(tabulate(fetch_all(cursor), "keys", "psql"))


""" ЗАДАНИЕ 5.
    Уточнения:
        1. Создайте новый признак age_years – возраст в годах, округлив до целых (round).
           Для данного примера отберите курящих мужчин от 60 до 64 лет включительно.
        2. Категории уровня холестрина на рисунке и в наших данных отличаются. Отображение значений на картинке
           в значения признака cholesterol следующее: 4 ммоль/л -> 1, 5-7 ммоль/л -> 2, 8 ммоль/л -> 3.
        3. Интересуют 2 подвыборки курящих мужчин возраста от 60 до 64 лет включительно:
           первая с верхним артериальным давлением строго меньше 120 мм рт.ст. и концентрацией холестерина – 4 ммоль/л,
           а вторая – с верхним артериальным давлением от 160 (включительно) до 180 мм рт.ст. (не включительно)
           и концентрацией холестерина – 8 ммоль/л.

    Во сколько раз (округленно, round) отличаются доли больных людей (согласно целевому признаку, cardio)
    в этих двух подвыборках?
"""

cursor.execute(
    """
    SELECT (ROUND(
        ((SELECT AVG(cardio::int)
            FROM (SELECT * FROM mlboot WHERE 60 <= round(age/365.25)::int AND round(age/365.25)::int <= 64 AND gender=2 AND smoke::int=1) AS w
            WHERE cholesterol = 3 AND ap_hi >= 160 AND ap_lo < 180 AND gender=2 AND smoke::int=1)
        /
        (SELECT AVG(cardio::int)
            FROM (SELECT * FROM mlboot WHERE 60 <= round(age/365.25)::int AND round(age/365.25)::int <= 64 AND gender=2 AND smoke::int=1) AS r
            WHERE cholesterol = 1 AND ap_hi < 120 AND gender=2 AND smoke::int=1)
        )
    )) AS avg_div
    FROM mlboot
    LIMIT '1'
    """
)
print('TASK 5')
print(tabulate(fetch_all(cursor), "keys", "psql"))


""" ЗАДАНИЕ 6. Постройте новый признак – BMI (Body Mass Index). Для этого надо вес в килограммах
    поделить на квадрат роста в метрах. Нормальными считаются значения BMI от 18.5 до 25.

    Выбрать верные утверждения:

    1. Медианный BMI по выборке превышает норму.
    2. У женщин в среднем BMI ниже, чем у мужчин.
    3. У здоровых в среднем BMI выше, чем у больных.
    4. В сегменте здоровых и непьющих мужчин в среднем BMI ближе к норме,
       чем в сегменте здоровых и непьющих женщин.
"""

cursor.execute(
    """
    SELECT height / 100 AS bmi FROM mlboot LIMIT '10'
    """
)
print('TASK 6.1')
print(tabulate(fetch_all(cursor), "keys", "psql"))
