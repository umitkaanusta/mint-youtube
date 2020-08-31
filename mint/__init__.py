from mint.sentiment_viz import create_sentiment_donuts, donuts_filenames
from mint.time_viz import create_timeviz_donuts, timeviz_filenames
from mint.wordclouds import create_wordclouds, wordcloud_filenames
from mint.time_utils import get_hours_score, get_weekdays_score, label_hours, label_weekdays
from mint.sentiment import get_sentiment
from mint.video_data import get_channel_name, get_video_title
import mint.test_utils

API_KEY = "api-key"


def create_visuals(df, lang, testmode=False):
    create_timeviz_donuts(df, lang)
    create_sentiment_donuts(df, lang)
    create_wordclouds(df, lang, testmode)


def get_visuals_filenames():
    return {**timeviz_filenames, **donuts_filenames, **wordcloud_filenames}


def get_report(video_id, api_key, time_dict, lang, df, testmode=False):
    report_ = {
        "metadata": {
            "_created_at": time_dict[lang],
            "lang": lang,
            "channel_name": test_utils.channel_names[lang] if testmode else get_video_title(video_id, api_key),
            "video_title": test_utils.video_titles[lang] if testmode else get_channel_name(video_id, api_key)
        },
        "time_dist": {
            "week_dist": get_weekdays_score(df),
            "hours_dist": get_hours_score(df),
            "hours_dist_workdays": get_hours_score(label_weekdays(df)[label_weekdays(df)["day"].isin([0])]),
            "hours_dist_weekend": get_hours_score(label_weekdays(df)[label_weekdays(df)["day"].isin([1])])
        },
        "sentiment_dist": {
            "sentiment_general": get_sentiment(df, lang),
            "sentiment_workdays": get_sentiment(label_weekdays(df)[label_weekdays(df)["day"].isin([0])], lang),
            "sentiment_weekend": get_sentiment(label_weekdays(df)[label_weekdays(df)["day"].isin([1])], lang),
            "sentiment_night": get_sentiment(label_hours(df)[label_hours(df)["hour"].isin([1])], lang),
            "sentiment_morning": get_sentiment(label_hours(df)[label_hours(df)["hour"].isin([2])], lang),
            "sentiment_afternoon": get_sentiment(label_hours(df)[label_hours(df)["hour"].isin([3])], lang),
            "sentiment_evening": get_sentiment(label_hours(df)[label_hours(df)["hour"].isin([4])], lang)
        }
    }
    return report_
