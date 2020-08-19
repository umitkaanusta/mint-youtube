from wordcloud import WordCloud, get_single_color_func
from mint.sentiment import label_sentiment
from mint.util import text_preprocess_en, text_preprocess_tr, txt_to_list, comments_to_string
from mint.time_utils import label_weekdays, label_hours
from mint.video_data import get_channel_name
from time import time

wordcloud_filenames = {}


def _create_wordcloud(df, lang, filename, width, height):
    # Template function to create wordclouds
    stopwords = ""
    title = get_channel_name(df["video_id"].iloc[0]).lower()
    comments = comments_to_string(df).lower()
    comments = comments.replace("video", "")
    for word in title.split():
        comments = comments.replace(word, "")
    if lang == "tr":
        stopwords = txt_to_list("mint/models/datasets/stopwords-tr.txt")
        comments = text_preprocess_tr(comments)
        # Common words people use to refer youtubers in Turkish
        comments = comments.replace("abi", "")
        comments = comments.replace("abla", "")
    if lang == "en":
        stopwords = txt_to_list("mint/models/datasets/stopwords-en.txt")
        comments = text_preprocess_en(comments)
    if lang not in ["tr", "en"]:
        raise ValueError("parameter lang should be either tr or en")
    # Stopwords are already removed by text_preprocess functions but if stopwords is None in WordCloud,
    # it uses its own stopwords. So we're putting our own stopwords lists to prevent unexpected problems
    cloud = WordCloud(width=width, height=height, stopwords=stopwords, max_words=400).generate(comments)
    fname_stamped = filename + "".join(str(time()).split("."))
    wordcloud_filenames[filename] = "img/" + fname_stamped + ".png"
    cloud.to_file(filename=f"mint/static/img/{fname_stamped}.png")


def create_wordcloud_general(df, lang):
    # Creates a wordcloud of all comments
    _create_wordcloud(df, lang=lang, width=500, height=250, filename="wordcloud_general")


def create_wordcloud_sentiment(df, lang):
    # Creates 3 wordclouds of positive, negative and neutral comments
    df = label_sentiment(df, lang=lang)
    positive = df[df["sentiment"].isin([1])]
    neutral = df[df["sentiment"].isin([0])]
    negative = df[df["sentiment"].isin([-1])]
    _create_wordcloud(positive, lang=lang, width=500, height=250, filename="wordcloud_positive")
    _create_wordcloud(neutral, lang=lang, width=500, height=250, filename="wordcloud_neutral")
    _create_wordcloud(negative, lang=lang, width=500, height=250, filename="wordcloud_negative")


def create_wordcloud_weekdays(df, lang):
    # Creates 2 wordclouds, one for workdays and one for weekends.
    df = label_weekdays(df)
    workdays = df[df["day"].isin([0])]
    weekend = df[df["day"].isin([1])]
    _create_wordcloud(workdays, lang=lang, width=500, height=250, filename="wordcloud_workdays")
    _create_wordcloud(weekend, lang=lang, width=500, height=250, filename="wordcloud_weekend")


def create_wordcloud_hours(df, lang):
    # Creates wordclouds for each segment based on hours
    df = label_hours(df)
    night = df[df["hour"].isin([1])]
    morning = df[df["hour"].isin([2])]
    afternoon = df[df["hour"].isin([3])]
    evening = df[df["hour"].isin([4])]
    _create_wordcloud(night, lang=lang, width=400, height=200, filename="wordcloud_night")
    _create_wordcloud(morning, lang=lang, width=400, height=200, filename="wordcloud_morning")
    _create_wordcloud(afternoon, lang=lang, width=400, height=200, filename="wordcloud_afternoon")
    _create_wordcloud(evening, lang=lang, width=400, height=200, filename="wordcloud_evening")


def create_wordclouds(df, lang):
    create_wordcloud_general(df, lang)
    create_wordcloud_sentiment(df, lang)
    create_wordcloud_weekdays(df, lang)
    create_wordcloud_hours(df, lang)
