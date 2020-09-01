# Functions to test the visual report

from plotly.io.orca import config
from mint._test_utils import video_ids
from mint.video_data import get_comments_from_csv
from mint.util import clean_dir
from mint import create_visuals, get_visuals_filenames
import os


def test_visuals_created():
    df = get_comments_from_csv(video_id=video_ids["en"])
    clean_dir("mint/static/img")
    config.executable = "mint/orca/orca.exe"
    create_visuals(df, "en", True)
    images = set(os.listdir("mint/static/img"))
    filenames = set(get_visuals_filenames().values())
    assert images == filenames




