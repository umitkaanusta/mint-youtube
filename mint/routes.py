from flask import Flask, render_template, request, url_for
from mint import create_visuals, get_visuals_filenames
from mint.video_data import get_comments, create_comments_csv, get_comments_from_csv, get_video_title, get_channel_name
import os
from datetime import datetime

app = Flask(__name__, static_url_path="/static")
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY


# sample format: https://www.site.com/report?video_id=325325q1&lang=tr (lang can be en too)
@app.route("/report", methods=["GET"])
def report():
    time_dict = {
        "tr": datetime.now().strftime("%d/%m/%Y - %H:%M"),
        "en": datetime.now().strftime("%d %b %Y - %H:%M")
    }
    video_id = request.args.get("video_id")
    lang = request.args.get("lang")
    df = get_comments(video_id)
    # df = get_comments_from_csv(video_id)
    now = time_dict[lang]
    title = get_video_title(video_id)
    channel_name = get_channel_name(video_id)
    create_visuals(df, lang)
    filenames = get_visuals_filenames()
    return render_template(f"report_{lang}.html", video_id=video_id, title=title, time=now,
                           channel_name=channel_name, filenames=filenames)


@app.route("/test", methods=["GET"])
def test_report():
    time_dict = {
        "tr": datetime.now().strftime("%d/%m/%Y - %H:%M"),
        "en": datetime.now().strftime("%d %b %Y - %H:%M")
    }
    lang = request.args.get("lang")
    # df = get_comments(video_id)
    video_id = "gk5DaBYtu-E" if lang == "tr" else "ng2o98k983k"
    df = get_comments_from_csv(video_id)
    now = time_dict[lang]
    title = get_video_title(video_id)
    channel_name = get_channel_name(video_id)
    create_visuals(df, lang)
    filenames = get_visuals_filenames()
    print(filenames)
    return render_template(f"report_{lang}.html", video_id=video_id, title=title, time=now,
                           channel_name=channel_name, filenames=filenames)
