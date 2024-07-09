from urlextract import URLExtract
from collections import Counter
import pandas as pd
from wordcloud import WordCloud
import emoji

extract = URLExtract()


def countNumOfWords(df):
    words = []
    for message in df['messages']:
        words.extend(message.split())
    return len(words)


def countMedia(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    imageCount = df[df['messages'] == 'image omitted\r\n'].shape[0]
    videoCount = df[df['messages'] == 'video omitted\r\n'].shape[0]
    stickerCount = df[df['messages'] == 'sticker omitted\r\n'].shape[0]
    return imageCount, videoCount, stickerCount


def countUrl(selected_user, df):
    links = []
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    for message in df['messages']:
        links.extend(extract.find_urls(message))
    return len(links)


def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    numOfMessages = df.shape[0]
    numOfWords = countNumOfWords(df)
    return numOfMessages, numOfWords


def fetchMostUsers(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'users': 'name', 'count': 'percent'})
    return x, df


def createWordCloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=" "))
    return df_wc


def mostCommonWords(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    f = open("stop_hinglish.txt", 'r')
    stop_words = f.read()
    words = []
    for message in df['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df


def mostUsedEmojis(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    return_df = pd.DataFrame(Counter(emojis).most_common(20))
    return_df = return_df.rename(columns={'0': 'emoji', '1': 'count'})
    return return_df



