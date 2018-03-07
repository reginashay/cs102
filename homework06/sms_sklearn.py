from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import string


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


f = open("data/SMSSpamCollection", 'rb')
data = []
for line in f:
    data.append([line.decode('utf8')])

for i in data:
    i[0] = i[0].replace('\n', '')
    i[0] = i[0].split('\t')

X, y = [], []

for sms in data:
    for target, msg in sms:
        X.append(msg)
        y.append(target)

X = [clean(x).lower() for x in X]

X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

model = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB(alpha=0.05)),
])

model.fit(X_train, y_train)
print(model.score(X_test, y_test))
# 0.982078853046595
