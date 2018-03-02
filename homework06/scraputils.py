import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    rows = parser.findAll('table')[2].findAll('tr')

    for n in range(0, len(rows) - 3, 3):

        try:
            comments = rows[n + 1].findAll('a')
            if comments:
                if 'comment' in comments[3].text:
                    comment = int(comments[3].text.split()[0]) 
                else: 
                    comment = 0
            else:
                comment = 0
        except (IndexError):
            comment = 0

        author = rows[n + 1].a.text
        if 'ago' in author:
            author = None

        points = rows[n + 1].findAll('span')[0].text.split()[0]

        title = rows[n].findAll('a')[1].text

        url = rows[n].findAll('a')[1]['href']

        if ' ' not in title:
            title = rows[n].findAll('a')[0].text
            url = rows[n].findAll('a')[1].text

        news_list.append({
            'author': author if author else None,
            'comments': comment,
            'points': int(points) if points else 0,
            'title': title,
            'url': url if 'http' in url else None
            })

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.findAll('table')[2].findAll('tr')[-1].a['href']


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
