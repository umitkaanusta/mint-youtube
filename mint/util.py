import string
import pandas as pd
import os
import glob
import urllib.parse as urlparse
from urllib.parse import parse_qs


def txt_to_list(path):
    # Reads a txt file's each line, puts it in a list
    f = open(path, "r", encoding="utf-8")
    txt_list = f.read().split()
    return txt_list


def comments_to_string(df):
    # Reads a video's csv file, converts the comments into a single string
    return " ".join(df["text"].tolist())


def dict_to_list(dictionary):
    # Returns keys and values of a dict
    return list(dictionary.keys()), list(dictionary.values())


def clean_dir(path):
    files = glob.glob(path + "/*")
    for f in files:
        os.remove(f)


def get_video_id(url):
    # Gets YouTube video id from url
    if "youtu.be" in url:
        return url.split("/")[-1]
    parsed = urlparse.urlparse(url)
    return parse_qs(parsed.query)["v"][0]


def text_preprocess_tr(text):
    try:
        stopwords = txt_to_list("mint/models/datasets/stopwords-tr.txt")
    except FileNotFoundError:
        # When retraining a model through a script in models folder, the above usage fails
        stopwords = txt_to_list("datasets/stopwords-tr.txt")
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = [word for word in text.split() if word.lower() not in stopwords]
    return " ".join(text)


def text_preprocess_en(text):
    try:
        stopwords = txt_to_list("mint/models/datasets/stopwords-en.txt")
    except FileNotFoundError:
        # When retraining a model through a script in models folder, the above usage fails
        stopwords = txt_to_list("datasets/stopwords-en.txt")
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = [word for word in text.split() if word.lower() not in stopwords]
    return " ".join(text)
