# mint-youtube
Comment analytics tool for YouTube videos

## Known bugs
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
