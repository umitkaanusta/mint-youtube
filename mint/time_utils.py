# Utility functions to seperate comments into time segments
#
# Segments based on hour:
# 00:00 - 06:00: Night owls
# 07:00 - 12:00: Early birds & people at work
# 13:00 - 17:00: Those people have time to watch youtube during those hours
# 18:00 - 23:00: They're watching youtube to get away from work/school stress or watching YT on a weekend night
#
# Segments based on weekdays:
# Mon - Fri
# Sat - Sun

from datetime import datetime


def get_weekday(timestamp):
    # Converts a unix timestamp to weekdays
    # Returns 0 for workdays, 1 for weekend
    day = int(datetime.fromtimestamp(timestamp).strftime("%w"))
    if day in [1, 2, 3, 4, 5]:
        return 0
    if day in [0, 6]:
        return 1


def get_hour(timestamp):
    # Gets the hour from a unix timestamp
    # Returns:
    #   1 for 00:00 - 06:00
    #   2 for 07:00 - 12:00
    #   3 for 13:00 - 17:00
    #   4 for 18:00 - 23:00
    hour = int(datetime.fromtimestamp(timestamp).strftime("%H"))
    if 0 <= hour <= 6:
        return 1
    if 7 <= hour <= 12:
        return 2
    if 13 <= hour <= 17:
        return 3
    if 18 <= hour <= 23:
        return 4


def label_weekdays(df):
    # Returns df with weekdays labeled based on column comment_publish_date
    df["day"] = df["comment_publish_date"].apply(get_weekday)
    return df


def label_hours(df):
    df["hour"] = df["comment_publish_date"].apply(get_hour)
    return df


def get_weekdays_score(df):
    # Returns the number of comments on workdays and weekends
    df = label_weekdays(df)
    value_counts = df["day"].value_counts()
    # Value counts does not show weekend (e.g) data if there isn't any, so we need to check if they exist first
    workdays = value_counts[0] if 0 in value_counts.keys() else 0
    weekend = value_counts[1] if 1 in value_counts.keys() else 0
    return {"workdays": int(workdays), "weekend": int(weekend)}


def get_hours_score(df):
    # Returns the number of comments on four hour-based time segments
    df = label_hours(df)
    value_counts = df["hour"].value_counts()
    night = value_counts[1] if 1 in value_counts.keys() else 0
    morning = value_counts[2] if 2 in value_counts.keys() else 0
    afternoon = value_counts[3] if 3 in value_counts.keys() else 0
    evening = value_counts[4] if 4 in value_counts.keys() else 0
    return {"night": int(night), "morning": int(morning), "afternoon": int(afternoon), "evening": int(evening)}
