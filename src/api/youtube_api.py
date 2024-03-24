# Standard Library
# import json
# import pathlib
from datetime import datetime

# Third Party Library
import pytz
from googleapiclient.discovery import build


class YoutubeApiRequest:
    def __init__(
        self,
        youtube_api_service_name: str,
        youtube_api_version: str,
        developer_key: str
    ) -> None:
        self.youtube = build(
            youtube_api_service_name,
            youtube_api_version,
            developerKey=developer_key
        )
        dt = datetime.now(pytz.timezone('Asia/Tokyo'))
        self.date_str = dt.strftime('%Y%m%d%H%M')
        # self.local_path = list(pathlib.Path("src").glob("json"))[0]

    # def get_youtube_data_to_json(self) -> None:
    #     request = self.youtube.videos().list(
    #         part="snippet, contentDetails, statistics",
    #         chart="mostPopular",
    #         maxResults=50,
    #         regionCode="JP"
    #     )
    #     res = request.execute()

    #     with open(
    #         f"{self.local_path}/{self.date_str}_popular.json",
    #         encoding='utf-8',
    #         mode='w',
    #     ) as f:
    #         json.dump(res, f, ensure_ascii=False, indent=2)

    def get_youtube_data(self) -> dict:
        request = self.youtube.videos().list(
            part="snippet, contentDetails, statistics",
            chart="mostPopular",
            maxResults=50,
            regionCode="JP"
        )

        res = request.execute()
        return res


if __name__ == "__main__":
    from gcp.secretmanager import SecretManagerInterface
    from env import (
        PROJECT_ID,
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        SECRET_ID,
        SECRET_YOUTUBE_API_VERSION
    )

    sc = SecretManagerInterface()
    developer_key = sc.get_secret(
        project_id=PROJECT_ID,
        secret_id=SECRET_ID,
        version_id=SECRET_YOUTUBE_API_VERSION
    )

    youtube = YoutubeApiRequest(
        youtube_api_service_name=YOUTUBE_API_SERVICE_NAME,
        youtube_api_version=YOUTUBE_API_VERSION,
        developer_key=developer_key
    )
    print(youtube.get_youtube_data())
    # print(youtube.date_str)
    # youtube.get_youtube_data_to_json()
