from flask import Flask, render_template, request, url_for, jsonify
from mint import create_visuals, get_visuals_filenames, get_report
from mint.video_data import get_comments, create_comments_csv, get_comments_from_csv, get_video_title, get_channel_name
import mint
import os
import shutil
from datetime import datetime

app = Flask(__name__, static_url_path="/static")
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY


# sample format: https://www.site.com/report?video_id=325325q1&lang=tr (lang can be en too)
@app.route("/report", methods=["GET"])
def report():
    # Cleaning the static/img directory, deleting old images
    shutil.rmtree("mint/static/img")
    os.mkdir("mint/static/img")
    time_dict = {
        "tr": datetime.now().strftime("%d/%m/%Y - %H:%M"),
        "en": datetime.now().strftime("%d %b %Y - %H:%M (UTC+3)")
    }
    video_id = request.args.get("video_id")
    lang = request.args.get("lang")
    api_key = request.args.get("api_key")
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
    shutil.rmtree("mint/static/img")
    os.mkdir("mint/static/img")
    time_dict = {
        "tr": datetime.now().strftime("%d/%m/%Y - %H:%M"),
        "en": datetime.now().strftime("%d %b %Y - %H:%M (UTC+3)")
    }
    lang = request.args.get("lang")
    api_key = request.args.get("api_key")
    mint.API_KEY = api_key
    # df = get_comments(video_id)
    video_id = "gk5DaBYtu-E" if lang == "tr" else "ng2o98k983k"
    df = get_comments_from_csv(video_id)
    now = time_dict[lang]
    title = get_video_title(video_id, api_key)
    channel_name = get_channel_name(video_id, api_key)
    create_visuals(df, lang)
    filenames = get_visuals_filenames()
    return render_template(f"report_{lang}.html", video_id=video_id, title=title, time=now,
                           channel_name=channel_name, filenames=filenames)


@app.route("/api/report", methods=["GET"])
def report_json():
    time_dict = {
        "tr": datetime.now().strftime("%d/%m/%Y - %H:%M"),
        "en": datetime.now().strftime("%d %b %Y - %H:%M (UTC+3)")
    }
    video_id = request.args.get("video_id")
    lang = request.args.get("lang")
    api_key = request.args.get("api_key")
    mint.API_KEY = api_key
    df = get_comments(video_id, api_key)
    report_ = get_report(video_id, api_key, time_dict, lang, df)
    return jsonify(report_)


@app.route("/api/test-report", methods=["GET"])
def report_json_test():
    time_dict = {
        "tr": datetime.now().strftime("%d/%m/%Y - %H:%M"),
        "en": datetime.now().strftime("%d %b %Y - %H:%M (UTC+3)")
    }
    lang = request.args.get("lang")
    api_key = request.args.get("api_key")
    mint.API_KEY = api_key
    video_id = "gk5DaBYtu-E" if lang == "tr" else "ng2o98k983k"
    df = get_comments_from_csv(video_id)
    report_ = get_report(video_id, api_key, time_dict, lang, df)
    return jsonify(report_)
