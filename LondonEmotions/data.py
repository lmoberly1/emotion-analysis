# -*- coding: UTF-8 -*-
""" Main lib for london-emotions Project
"""
from LondonEmotions.params import BUCKET_NAME, BUCKET_TRAIN_DATA_PATH
from gensim import utils
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords
from os.path import split
import pandas as pd
import datetime
import string
import re
import nltk
# to download nltk data: https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

pd.set_option('display.width', 200)


def retrieve_data(local=True, optimize=False, **kwargs):
    """method to get the training data (or a portion of it) from google cloud bucket"""
    # Add Client() here
    # client = storage.Client()
    if local:
        # path = "raw_data/emotion_data.csv"
        path = 'raw_data/data_train.csv'
    else:
        path = "gs://{}/{}".format(BUCKET_NAME, BUCKET_TRAIN_DATA_PATH)
    df = pd.read_csv(path)
    return df


def clean_data(data):
    """
    clean and preprocess data
    """
    # Process number reviews as strings
    data['Text'] = data['Text'].astype(str)

    # Remove numbers
    data['clean_text'] = data['Text'].apply(
        lambda x: ''.join(let for let in x if not let.isdigit())
    )
    # Lowercase text
    data['clean_text'] = data['clean_text'].apply(
        lambda x: x.lower()
    )
    # Strip whitespace
    data['clean_text'] = data['clean_text'].apply(
        lambda x: x.strip()
    )
    # Remove hashtags and usernames
    data['clean_text'] = data['clean_text'].apply(
        lambda x: re.sub(r"(#[\d\w\.]+)", '', x)
    )
    data['clean_text'] = data['clean_text'].apply(
        lambda x: re.sub(r"(@[\d\w\.]+)", '', x)
    )
    # Remove punctuation
    data['clean_text'] = data['clean_text'].apply(
        lambda x: ''.join(let for let in x if not let in string.punctuation)
    )
    # Tokenization with nltk
    data['clean_text'] = data['clean_text'].apply(
        lambda x: word_tokenize(x)
    )
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    data['clean_text'] = data['clean_text'].apply(
        lambda x: [word for word in x if word not in stop_words]
    )
    # Lemmatizing with nltk
    lemmatizer = WordNetLemmatizer()
    data['clean_text'] = data['clean_text'].apply(
        lambda x: ' '.join(lemmatizer.lemmatize(word) for word in x)
    )

    # Tokenizing text
    data['tokenized_text'] = [utils.simple_preprocess(
        line, deacc=True) for line in data['clean_text']]
    # Return data
    return data


if __name__ == '__main__':
    # For introspections purpose to quickly get this functions on ipython
    # import london-emotions
    # folder_source, _ = split(london-emotions.__file__)
    df = retrieve_data()
    clean_data = clean_data(df)
    print(' dataframe cleaned')
