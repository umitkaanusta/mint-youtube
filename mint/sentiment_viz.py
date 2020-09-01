from mint.sentiment import get_sentiment
from mint.time_utils import label_hours, label_weekdays
from mint.util import dict_to_list
import plotly.graph_objects as go
from kaleido.scopes.plotly import PlotlyScope
from time import time

donuts_filenames = {}


def _create_donut(df, lang, filename, width, height, fontsize):
    scope = PlotlyScope()
    sentiment = get_sentiment(df, lang)
    labels, values = dict_to_list(sentiment)
    if lang == "tr":
        labels = ["Pozitif", "Nötr", "Negatif"]
    if lang == "en":
        labels = [label.capitalize() for label in labels]
    colors = ["darkgreen", "lightgreen", "red"]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5, textinfo="label+percent+value",
                                 textposition="inside")])
    fig.update_traces(marker=dict(colors=colors), textfont_size=fontsize, showlegend=False)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0, pad=4), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", width=width, height=height)
    fname_stamped = filename + "".join(str(time()).split("."))
    donuts_filenames[filename] = "img/" + fname_stamped + ".svg"
    with open(f"mint/static/img/{fname_stamped}.svg", "wb") as f:
        f.write(scope.transform(fig, format="svg"))
    # fig.write_image(file=f"mint/static/img/{fname_stamped}.svg")


def create_donut_general(df, lang):
    # Creates a donut graph of all comments
    _create_donut(df, lang=lang, filename="donut_general", width=400, height=400, fontsize=16)


def create_donut_weekdays(df, lang):
    # Creates 2 donut graphs where one is for workdays, the other is for weekends
    df = label_weekdays(df)
    workdays = df[df["day"].isin([0])]
    weekend = df[df["day"].isin([1])]
    _create_donut(workdays, lang=lang, filename="donut_workdays", width=400, height=400, fontsize=16)
    _create_donut(weekend, lang=lang, filename="donut_weekend", width=400, height=400, fontsize=16)


def create_donut_hours(df, lang):
    # Creates donut graphs for each segment based on hours
    df = label_hours(df)
    night = df[df["hour"].isin([1])]
    morning = df[df["hour"].isin([2])]
    afternoon = df[df["hour"].isin([3])]
    evening = df[df["hour"].isin([4])]
    _create_donut(night, lang=lang, filename="donut_night", width=320, height=320, fontsize=14)
    _create_donut(morning, lang=lang, filename="donut_morning", width=320, height=320, fontsize=14)
    _create_donut(afternoon, lang=lang, filename="donut_afternoon", width=320, height=320, fontsize=14)
    _create_donut(evening, lang=lang, filename="donut_evening", width=320, height=320, fontsize=14)


def create_sentiment_donuts(df, lang):
    create_donut_general(df, lang)
    create_donut_weekdays(df, lang)
    create_donut_hours(df, lang)
