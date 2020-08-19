from mint.sentiment_viz import create_sentiment_donuts, donuts_filenames
from mint.time_viz import create_timeviz_donuts, timeviz_filenames
from mint.wordclouds import create_wordclouds, wordcloud_filenames


def create_visuals(df, lang):
    create_timeviz_donuts(df, lang)
    create_sentiment_donuts(df, lang)
    create_wordclouds(df, lang)


def get_visuals_filenames():
    return {**timeviz_filenames, **donuts_filenames, **wordcloud_filenames}
