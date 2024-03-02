# Standard Library
import json
import pathlib
from datetime import datetime

# Third Party Library
import pytz
from googleapiclient.discovery import build

# First Party Library
from api.youtube_api_config import (
    YOUTUBE_API_KEY,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
)


class YoutubeApiRequest:
    def __init__(self) -> None:
        self.youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=YOUTUBE_API_KEY
        )
        dt = datetime.now(pytz.timezone('Asia/Tokyo'))
        self.date_str = dt.strftime('%Y%m%d%H%M')
        self.local_path = list(pathlib.Path("src").glob("json"))[0]

    def get_youtube_data_to_json(self) -> None:
        request = self.youtube.videos().list(
            part="snippet, contentDetails, statistics",
            chart="mostPopular",
            maxResults=50,
            regionCode="JP"
        )
        res = request.execute()

        with open(
            f"{self.local_path}/{self.date_str}_popular.json",
            encoding='utf-8',
            mode='w',
        ) as f:
            json.dump(res, f, ensure_ascii=False, indent=2)

    def get_youtube_data(self) -> dict:
        request = self.youtube.videos().list(
            part="snippet, contentDetails, statistics",
            chart="mostPopular",
            maxResults=50,
            regionCode="JP"
        )
        return request.execute()


if __name__ == "__main__":
    youtube = YoutubeApiRequest()
    print(youtube.date_str)
    # youtube.get_youtube_data_to_json()
