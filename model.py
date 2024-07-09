from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

df = pd.read_csv("tweet_emotions.csv")
df = df[['sentiment', 'content']]


def update(text):
    if text == 'hate' or text == 'anger': return 'angry'
    if text == 'sadness' or text == 'worry': return 'sad'
    if text == 'empty' or text == 'neutral' or text == 'boredom': return 'neutral'
    if text == 'fun' or text == 'enthusiasm' or text == 'relief': return 'happy'
    if text == 'surprise' or text == 'love' or text == 'happiness': return 'blissful'


df['emotion'] = df['sentiment'].apply(update)
df = df[['emotion', 'content']]

X = df['content']
y = df['emotion']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

tfidf = TfidfVectorizer(max_features=5000, stop_words='english', strip_accents='ascii')

X_train_v = tfidf.fit_transform(X_train)
X_test_v = tfidf.transform(X_test)

dtree_model = DecisionTreeClassifier().fit(X_train_v, y_train)
y_pred_dtree = dtree_model.predict(X_test_v)

