from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from bayes import NaiveBayesClassifier
from db import News, session
import string


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


s = session()

num = int(len(s.query(News).filter(News.label != None).all()) * 0.7)

rows = s.query(News).filter(News.label != None).all()
X = [clean(row.title).lower() for row in rows]
y = [row.label for row in rows]

X_train, y_train, X_test, y_test = X[:num], y[:num], X[num:], y[num:]


model = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB(alpha=0.05)),
])

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(model.score(X_test, y_test))
print(accuracy_score(y_test, y_pred))
