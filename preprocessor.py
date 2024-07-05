import re
import pandas as pd


def starts_with_u200e(text):
    pattern = r'^\u200e'
    return bool(re.match(pattern, text))


def remove_leading_u200e(text):
    return re.sub(r'^\u200e', '', text)


def remove_trailing_u200e(text):
    if text.endswith('\u200e'):
        return text[:-1]
    return text


def preprocess(data):
    pattern = r'\[\d{2}\/\d{2}\/\d{2}, \d{2}:\d{2}:\d{2}\]\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({
        'user_messages': messages,
        'message_date': dates
    })
    df['message_date'] = pd.to_datetime(df['message_date'], format='[%d/%m/%y, %H:%M:%S] ')
    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split(r'([\w\W]+?):\s', message)
        entry[2] = remove_trailing_u200e(entry[2])
        entry[2] = remove_leading_u200e(entry[2])
        users.append(entry[1])
        messages.append(entry[2])
    df['messages'] = messages
    df['users'] = users
    df.drop(columns=['user_messages'], inplace=True)
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    return df

