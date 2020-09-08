import os
import pandas as pd
from youtube_api import YouTubeDataAPI


def get_comments(video_id, api_key):
    yt = YouTubeDataAPI(api_key)
    return pd.DataFrame(yt.get_video_comments(video_id, get_replies=True))


# Debug function
def create_comments_csv(df, video_id):
    path = f"videos/{video_id}.csv"
    if os.path.isfile(path):
        os.remove(path)
    df.to_csv(path)


# Debug function
def get_comments_from_csv(video_id):
    # Using a CSV file in debug to avoid using our requests again and again
    path = f"mint/videos/{video_id}.csv"
    return pd.read_csv(path)


def get_video_title(video_id, api_key):
    yt = YouTubeDataAPI(api_key)
    return yt.get_video_metadata(video_id)["video_title"]


def get_channel_name(video_id, api_key):
    yt = YouTubeDataAPI(api_key)
    return yt.get_video_metadata(video_id)["channel_title"]


def get_channels_videos(channel_id, max_results, api_key):
    yt = YouTubeDataAPI(api_key)
    videos = yt.search(channel_id=channel_id, max_results=max_results, api_key=api_key)
    return [video["video_id"] for video in videos]
