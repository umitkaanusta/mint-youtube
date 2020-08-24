from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class VideoForm(FlaskForm):
    video_link = StringField("",
                           validators=[DataRequired(message="This field must be filled")],
                           render_kw={"placeholder": "Paste the link of the YouTube video"})
    api_key = StringField("",
                          validators=[DataRequired(message="This field must be filled")],
                          render_kw={"placeholder": "Paste the YouTube Data API key"})
    lang = SelectField("Language of the video",
                    choices=[("en", "English"), ("tr", "Turkish")],
                    validators=[DataRequired(message="This field must be filled")])
    submit = SubmitField("Analyze")
