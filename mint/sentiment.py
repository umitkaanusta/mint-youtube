from textblob import TextBlob
import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from mint.util import text_preprocess_tr, text_preprocess_en


def get_sentiment_en(text):
    # Returns a polarity score between -100 and 100
    score = int(TextBlob(text_preprocess_en(text)).sentiment.polarity * 100)
    if -10 <= score <= 10:
        return 0  # Neutral
    if -100 <= score < -10:
        return -1  # Negative
    if 10 < score <= 100:
        return 1  # Positive


def get_sentiment_tr(text, model):
    score = int(model.predict_proba(pd.Series(text_preprocess_tr(text)))[0][1] * 100)
    if 45 <= score <= 55:
        return 0  # Neutral
    if 0 <= score < 45:
        return -1  # Negative
    if 55 < score <= 100:
        return 1  # Positive


def label_sentiment(df, lang):
    # Labels the df with sentiments based on language
    # Returns the df with sentiments being labeled
    if lang == "tr":
        model_path = "mint/models/sentiment_model_tr.pkl"
        model = pickle.load(open(model_path, "rb"))
        df["sentiment"] = df["text"].apply(get_sentiment_tr, model=model)
    if lang == "en":
        df["sentiment"] = df["text"].apply(get_sentiment_en)
    if lang not in ["tr", "en"]:
        raise ValueError("parameter lang should be either en or tr")
    return df


def get_sentiment(df, lang):
    # Returns the number of positive, negative and neutral comments for a video's comment section
    df = label_sentiment(df, lang)
    value_counts = df["sentiment"].value_counts()
    positive = value_counts[1] if 1 in value_counts.keys() else 0
    negative = value_counts[-1] if -1 in value_counts.keys() else 0
    neutral = value_counts[0] if 0 in value_counts.keys() else 0
    sentiment = {"positive": int(positive), "neutral": int(neutral), "negative": int(negative)}
    return sentiment
