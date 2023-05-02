import json
import pathlib
from datetime import datetime

import pytz
from googleapiclient.discovery import build

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
        self.output_path = list(pathlib.Path("/app/src").glob("json"))[0]

    def get_youtube_data_to_json(self) -> None:
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            maxResults=50,
            regionCode="JP"
        )
        res = request.execute()

        with open(
            f"{self.output_path}/{self.date_str}_popular.json",
            encoding='utf-8',
            mode='w',
        ) as f:
            json.dump(res, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    youtube = YoutubeApiRequest()
    youtube.get_youtube_data_to_json()
