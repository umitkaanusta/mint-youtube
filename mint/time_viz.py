from mint.time_utils import get_weekdays_score, get_hours_score, label_weekdays
from mint.util import dict_to_list
import plotly.graph_objects as go
from plotly.io import write_image
from plotly.io.orca import config
from time import time

timeviz_filenames = {}


def _create_timeviz_donut(df, lang, filename, width, height, fontsize, metric):
    # Template function for creating donut graphs based on time segments
    # For more info about time segments, check time_utils.py
    config.executable = "mint/orca/orca.exe"
    labels, values = None, None
    if metric not in ["weekdays", "hours"]:
        raise ValueError("weekdays and hours are available time viz metrics")
    if metric == "weekdays" and lang not in ["tr", "en"]:
        raise ValueError("parameter lang should be either en or tr")
    if metric == "weekdays":
        scores = get_weekdays_score(df)
        labels, values = dict_to_list(scores)
        if lang == "tr":
            labels = ["Hafta içi", "Hafta sonu"]
        if lang == "en":
            labels = [label.capitalize() for label in labels]
    if metric == "hours":
        scores = get_hours_score(df)
        labels, values = dict_to_list(scores)
        labels = ["00:00 - 06:59", "07:00 - 12:59", "13:00 - 17:59", "18:00 - 23:59"]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5, textinfo="label+percent+value",
                                 textposition="inside")])
    fig.update_traces(textfont_size=fontsize, showlegend=False)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0, pad=4), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)")
    fname_stamped = filename + "".join(str(time()).split("."))
    timeviz_filenames[filename] = "img/" + fname_stamped + ".svg"
    write_image(fig, file=f"mint/static/img/{fname_stamped}.svg", width=width, height=height)


def create_timeviz_weekdays(df, lang):
    _create_timeviz_donut(df, lang=lang, filename="timeviz_weekdays", width=400, height=400,
                          fontsize=15, metric="weekdays")


def create_timeviz_hours_general(df):
    _create_timeviz_donut(df, lang=None, filename="timeviz_hours_general", width=400, height=400,
                          fontsize=15, metric="hours")


def create_timeviz_hours_weekdays(df):
    # Shows distribution of hourly segments for workdays and weekends
    df = label_weekdays(df)
    workdays = df[df["day"].isin([0])]
    weekend = df[df["day"].isin([1])]
    _create_timeviz_donut(workdays, lang=None, filename="timeviz_hours_workdays", width=400, height=400,
                          fontsize=15, metric="hours")
    _create_timeviz_donut(weekend, lang=None, filename="timeviz_hours_weekend", width=400, height=400,
                          fontsize=15, metric="hours")


def create_timeviz_donuts(df, lang):
    create_timeviz_weekdays(df, lang)
    create_timeviz_hours_general(df)
    create_timeviz_hours_weekdays(df)
