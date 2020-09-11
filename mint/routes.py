from flask import Flask, render_template, request, redirect, url_for, jsonify
from mint import create_visuals, get_visuals_filenames, get_report
from mint.video_data import (get_comments, create_comments_csv, get_comments_from_csv, get_video_title,
                        get_channel_name, get_channels_videos)
from mint.forms import VideoForm
from mint.util import clean_dir, get_video_id
import mint
import mint._test_utils as test_utils
import os
import shutil
from datetime import datetime

app = Flask(__name__, static_url_path="/static")
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["JSON_AS_ASCII"] = False  # Enables us to see UTF-8 characters in json outputs
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route("/", methods=["GET", "POST"])
def home():
    form = VideoForm()
    if form.validate_on_submit():
        video_link = form.video_link.data
        video_id = get_video_id(video_link)
        lang = form.lang.data
        api_key = form.api_key.data
        return redirect(url_for("report") + f"?video_id={video_id}&lang={lang}&yt_api_key={api_key}")
    return render_template("home.html", form=form)


# sample format: https://www.site.com/report?video_id=325325q1&lang=tr (lang can be en too)
@app.route("/report", methods=["GET"])
def report():
    # Cleaning the static/img directory, deleting old images
    clean_dir("mint/static/img")
    time_dict = {
        "tr": datetime.now().strftime("%d/%m/%Y - %H:%M"),
        "en": datetime.now().strftime("%d %b %Y - %H:%M")
    }
    video_id = request.args.get("video_id")
    lang = request.args.get("lang")
    api_key = request.args.get("yt_api_key")
    mint.API_KEY = api_key
    df = get_comments(video_id, api_key)
    # df = get_comments_from_csv(video_id)
    now = time_dict[lang]
    title = get_video_title(video_id, api_key)
    channel_name = get_channel_name(video_id, api_key)
    create_visuals(df, lang)
    filenames = get_visuals_filenames()
    return render_template(f"report_{lang}.html", video_id=video_id, title=title, time=now,
                           channel_name=channel_name, filenames=filenames)


@app.route("/test", methods=["GET"])
def report_test():
    # Cleaning the static/img directory, deleting old images
    clean_dir("mint/static/img")
    time_dict = {
        "tr": datetime.now().strftime("%d/%m/%Y - %H:%M"),
        "en": datetime.now().strftime("%d %b %Y - %H:%M")
    }
    lang = request.args.get("lang")
    video_id = test_utils.video_ids[lang]
    df = get_comments_from_csv(video_id)
    now = time_dict[lang]
    title = test_utils.video_titles[lang]
    channel_name = test_utils.channel_names[lang]
    create_visuals(df, lang, testmode=True)
    filenames = get_visuals_filenames()
    return render_template(f"report_{lang}.html", video_id=video_id, title=title, time=now,
                           channel_name=channel_name, filenames=filenames)


@app.route("/api/report", methods=["GET"])
def report_json():
    time_dict = {
        "tr": datetime.now().strftime("%d/%m/%Y - %H:%M"),
        "en": datetime.now().strftime("%d %b %Y - %H:%M")
    }
    video_id = request.args.get("video_id")
    lang = request.args.get("lang")
    api_key = request.args.get("yt_api_key")
    mint.API_KEY = api_key
    df = get_comments(video_id, api_key)
    report_ = get_report(video_id, api_key, time_dict, lang, df)
    return jsonify(report_)


@app.route("/api/test-report", methods=["GET"])
def report_json_test():
    time_dict = {
        "tr": datetime.now().strftime("%d/%m/%Y - %H:%M"),
        "en": datetime.now().strftime("%d %b %Y - %H:%M")
    }
    lang = request.args.get("lang")
    video_id = test_utils.video_ids[lang]
    df = get_comments_from_csv(video_id)
    api_key = "test"
    report_ = get_report(video_id, api_key, time_dict, lang, df, testmode=True)
    return jsonify(report_)


@app.route("/api/channel-report", methods=["GET"])
def channel_report_json():
    time_dict = {
        "tr": datetime.now().strftime("%d/%m/%Y - %H:%M"),
        "en": datetime.now().strftime("%d %b %Y - %H:%M")
    }
    channel_id = request.args.get("channel_id")
    lang = request.args.get("lang")
    max_results = int(request.args.get("max_results"))
    order_by = request.args.get("order_by") if request.args.get("order_by") else "relevance"
    api_key = request.args.get("yt_api_key")
    mint.API_KEY = api_key
    videos = get_channels_videos(channel_id, max_results, order_by, api_key)
    reports = []
    for video in videos:
        df = get_comments(video, api_key)
        rep = get_report(video, api_key, time_dict, lang, df)
        reports.append(rep)
    return jsonify(reports)
