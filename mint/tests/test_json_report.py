# Functions to test the JSON Report

from mint._test_utils import video_ids, video_titles, channel_names, time_dict
from mint.video_data import get_comments_from_csv
from mint import get_report
import json


def test_report_created():
    df = get_comments_from_csv(video_id=video_ids["en"])
    assert get_report(
        video_id=video_ids["en"],
        api_key="test",
        time_dict=time_dict,
        lang="en",
        df=df,
        testmode=True
    )


def test_json_report():
    df = get_comments_from_csv(video_id=video_ids["en"])
    report = get_report(video_ids["en"], "test", time_dict, "en", df, True)
    assert report["metadata"]
    assert report["metadata"]["_created_at"]
    assert report["metadata"]["lang"]
    assert report["metadata"]["channel_name"]
    assert report["metadata"]["video_title"]
    assert report["time_dist"]
    assert report["time_dist"]["week_dist"]
    assert report["time_dist"]["hours_dist"]
    assert report["time_dist"]["hours_dist_workdays"]
    assert report["time_dist"]["hours_dist_weekend"]
    assert report["sentiment_dist"]
    assert report["sentiment_dist"]["sentiment_general"]
    assert report["sentiment_dist"]["sentiment_workdays"]
    assert report["sentiment_dist"]["sentiment_weekend"]
    assert report["sentiment_dist"]["sentiment_night"]
    assert report["sentiment_dist"]["sentiment_morning"]
    assert report["sentiment_dist"]["sentiment_afternoon"]
    assert report["sentiment_dist"]["sentiment_evening"]


def test_report_jsonified():
    df = get_comments_from_csv(video_id=video_ids["en"])
    report = get_report(video_ids["en"], "test", time_dict, "en", df, True)
    assert json.dumps(report)
