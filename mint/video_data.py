import os
import pandas as pd
from youtube_api import YouTubeDataAPI


API_KEY = "api-key"
yt = YouTubeDataAPI(API_KEY)


def get_comments(video_id):
    # Returns a dataframe of comments in given video id
    return pd.DataFrame(yt.get_video_comments(video_id, get_replies=True))


# Debug function
def create_comments_csv(df, video_id):
    path = f"videos/{video_id}.csv"
    # Creates a csv file inside videos folder
    if os.path.isfile(path):
        os.remove(path)
    df.to_csv(path)


# Debug function
def get_comments_from_csv(video_id):
    # Using a CSV file in debug to avoid using our requests again and again
    path = f"mint/videos/{video_id}.csv"
    return pd.read_csv(path)


def get_video_title(video_id):
    # Returns the title of video from video id
    return yt.get_video_metadata(video_id)["video_title"]


def get_channel_name(video_id):
    return yt.get_video_metadata(video_id)["channel_title"]
