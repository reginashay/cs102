from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from db import News, session
import string


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


def get_data():
    rows = s.query(News).filter(News.label != None).all()
    X = [clean(row.title).lower() for row in rows]
    y = [row.label for row in rows]
    return X, y


s = session()
cnt = int(len(s.query(News).filter(News.label != None).all()) * 0.7)
X, y = get_data()
X_train, y_train, X_test, y_test = X[:cnt], y[:cnt], X[cnt:], y[cnt:]

model = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB(alpha=0.05)),
])

model.fit(X_train, y_train)
print(model.score(X_test, y_test))
# 0.3546325878594249
