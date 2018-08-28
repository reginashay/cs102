import requests
from requests import exceptions
import time
import datetime
from collections import Counter
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import networkx as nx
import community
import matplotlib.pyplot as plt
#import numpy


config = {
    'VK_ACCESS_TOKEN': '',
    'PLOTLY_USERNAME': 'reginashay',
    'PLOTLY_API_KEY': 'B6iSZ7YBb3JguRIxbxL0'
}


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for n in range(max_retries + 1):
        try:
            r = requests.get(url, params=params, timeout=timeout)
            return r
        except requests.exceptions.RequestException:
            if n == max_retries:
                raise
            backoff_delay = backoff_factor * (2 ** (n - 1))
            time.sleep(backoff_delay)


def get_friends(user_id, fields):
    """ Вернуть данные о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
        'domain': 'https://api.vk.com/method',
        'access_token': config.get('VK_ACCESS_TOKEN'),
        'user_id': user_id,
        'fields': fields
    }
    query = '{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53'.format(**query_params)
    response = requests.get(query)
    return response.json()


def age_predict(user_id):
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    response = get_friends(user_id, 'bdate')
    dates = [q.get('bdate') for q in response['response']['items']]
    b = [dates[i] for i in range(len(dates)) if dates[i] is not None]
    c = [b[j] for j in range(len(b)) if len(b[j]) > 5]
    digits = [c[k].split('.') for k in range(len(c))]
    g = 0
    m = 60*60*24*365
    tday = datetime.date.today()
    for cell in digits:
        bdate = datetime.date(int(cell[2]), int(cell[1]), int(cell[0]))
        dif = tday - bdate
        g += dif.total_seconds() // m
    return g // len(digits)


def messages_get_history(user_id, offset=0, count=20):
    """ Получить историю переписки с указанным пользователем
    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "offset must be positive integer"
    assert count >= 0, "count must be positive integer"

    lim_count = 200
    query_params = {
        'domain': 'https://api.vk.com/method',
        'access_token': config.get('VK_ACCESS_TOKEN'),
        'user_id': user_id,
        'offset': offset,
        'count': min(count, lim_count)
    }
    history = []
    while count != 0:
        query = '{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}&v=5.53'.format(**query_params)
        response = requests.get(query)
        count -= min(count, lim_count)
        query_params['offset'] += 200
        query_params['count'] = min(count, lim_count)
        history += response.json()['response']['items']
        time.sleep(0.3)
    return history


def count_dates_from_messages(messages):
    """ Получить список дат и их частот
    :param messages: список сообщений
    """
    dates_rep = [datetime.datetime.fromtimestamp(n['date']).strftime("%Y-%m-%d")
                 for n in messages]
    unique = Counter(dates_rep)
    dates_list = [f for f in unique]
    freq = [unique[f] for f in unique]
    return dates_list, freq


def plotly_messages_freq(freq_list):
    """ Построение графика с помощью Plot.ly
    :param freq_list: список дат и их частот
    """
    x, y = freq_list
    data = [go.Scatter(x=x, y=y)]
    py.iplot(data)


def get_network(users_ids, as_edgelist=True):
    edges = []
    matrix = [[0 for j in range(len(users_ids))]
              for i in range(len(users_ids))]
    for i, us_id in enumerate(users_ids):
        user_id = us_id.get('id')
        response = get_friends(user_id, fields='bdate')
        if response.get('error'):
            continue
        friends_list = response['response']['items']
        for j in range(i + 1, len(users_ids)):
            if users_ids[j] in friends_list:
                if as_edgelist is True:
                    edges.append((i, j))
                else:
                    matrix[i][j] = matrix[j][i] = 1
    if as_edgelist is True:
        return edges
    else:
        return matrix


def plot_graph(graph):
    nodes = set([n for n, m in graph] + [m for n, m in graph])
    g = nx.Graph()
    for node in nodes:
        g.add_node(node)
    for edge in graph:
        g.add_edge(edge[0], edge[1])
    pos = nx.shell_layout(g)
    part = community.best_partition(g)
    values = [part.get(node) for node in g.nodes()]
    nx.draw_spring(g, cmap=plt.get_cmap('jet'), node_color=values,
                   node_size=30, with_labels=False)
    plt.show()


if __name__ == '__main__':
    user_id = 120828165
    other_id = 468524897
    r = get_friends(user_id, fields='bdate')
    b = age_predict(user_id)
    print('Predicted age:', int(b))

    c = messages_get_history(other_id, count=300)
    d = count_dates_from_messages(c)
    plotly_messages_freq(d)

    friends_list = r.get('response').get('items')
    edges = get_network(friends_list)
    plot_graph(edges)
