import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from mint.util import text_preprocess_tr
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
import pickle


df = pd.read_csv("datasets/turkish_sentiment_data.csv")

# Removing biased words (the dataset we used is composed of film reviews, those are normally neutral words)
biased_words = ["film", "video", "kamera", "senarist", "öpüşme", "sevişme"]
for word in biased_words:
    df["comment"] = df["comment"].apply(lambda x: x.replace(word, ""))
df["point"] = df["point"].apply(lambda x: x.replace(",", "."))
df["sentiment"] = df["point"].apply(lambda x: 0 if float(x) <= 3.5 else 1)

X = df["comment"].copy()
y = df["sentiment"]

X = X.apply(text_preprocess_tr)

sentiment_model_tr = Pipeline([('vectorizer', CountVectorizer()), ('classifier', LogisticRegression())])
sentiment_model_tr.fit(X, y)

pickle.dump(sentiment_model_tr, open("sentiment_model_tr.pkl", "wb"))
