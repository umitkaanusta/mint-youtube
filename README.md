# mint-youtube: Self-hosted YouTube comment analytics tool
![Python version](https://img.shields.io/badge/python-v3.7-blue)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)


Mint is a self-hosted comment analytics tool for YouTube videos.


## Demo video (click on the image to watch)
[![Demo video](https://img.youtube.com/vi/pTSNcMOUd-s/0.jpg)](https://www.youtube.com/watch?v=pTSNcMOUd-s)


## Upcoming features / Features in development
- A simple log to see the results of your past requests to the JSON API


## Installation

### Pulling from Docker Hub and running
- Run `docker pull umitkaanusta/mint-youtube`
- Run `docker run -p 5000:5000 -d umitkaanusta/mint-youtube`

### Creating your own Docker Image and running it
- Clone the repository
- `cd` to the repo's directory
- Run `docker build -t mint-youtube .`
- Run `docker run -p 5000:5000 -d mint-youtube`

### Installing & running without Docker
- Clone the repository
- Run `pip install -r requirements.txt`
- Run the script run.py 


## Usage
- Available languages: Turkish (tr), English (en)
- You need a YouTube Data API key before using Mint
- Check here if you don't have it: https://developers.google.com/youtube/v3/getting-started

### Getting visual report
- Open the home page, paste the link of the video, your YT Data API key and select the language of the comments.
- Alternatively, send a GET request to
    - `/report?video_id=<video_id>&lang=<language>&yt_api_key=<api_key>`
- Test endpoint:
    - `/test?lang=<language>`
    
### Getting JSON reports
- Mint has a small JSON API in it

#### Report for a video
- Send a GET request to
-   `/api/report?video_id=<video_id>&lang=<language>&yt_api_key=<api_key>`
- Test endpoint:
-   `/api/test-report?lang=<language>`

#### Report for a channel
- Send a GET request to
-   `/api/channel-report?channel_id=<channel_id>&lang=<language>&max_results=<max_results>&order_by=<order_by>&yt_api_key=<api_key>`
-   Query parameter `order_by` accepts the following: `date, rating, title, viewCount`
-   `order_by` is set to `relevance` by default



## Known bugs - not related to Mint

### Bug 001
Mint uses youtube-data-api as a Python wrapper of the YouTube Data API v3.
The package gives the following error on some cases:
```
"commenter_channel_id" : item['snippet'].get('authorChannelId').get('value', None),
AttributeError: 'NoneType' object has no attribute 'get'
```
Our suggested band-aid solution:
- Go to your local virtual env, find youtube_api under site-packages folder
- Modify line 233 of parsers.py as the following:
```
"commenter_channel_id" : None,
```
- **This change won't affect Mint in the slightest**


## Citations

```
@misc{leon_yin_2018_1414418,
  author       = {Leon Yin and
                  Megan Brown},
  title        = {SMAPPNYU/youtube-data-api},
  month        = sep,
  year         = 2018,
  doi          = {10.5281/zenodo.1414418},
  url          = {https://doi.org/10.5281/zenodo.1414418}
}
```
