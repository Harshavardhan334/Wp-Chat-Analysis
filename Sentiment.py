from collections import Counter
import pandas as pd
import pickle as pk

tfidf = pk.load(open('tfidf.pkl', 'rb'))
model = pk.load(open('model.pkl', 'rb'))


def Sentiment(df, selected_user):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    df['emotion'] = df['messages'].apply(predict)
    df.drop(['year', 'month', 'day', 'minute', 'users', 'hour'], axis=1, inplace=True)
    return df


def predict(content):
    return model.predict(tfidf.transform([content]))
