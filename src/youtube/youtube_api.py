# Standard Library
from datetime import datetime
from typing import cast

# Third Party Library
import pytz
from googleapiclient.discovery import build

from api.schemas.youtube_response import YouTubeVideoResponse
from api.schemas.job_request import InvokeRequest

class YoutubeApiRequest:
    def __init__(
        self,
        youtube_api_service_name: str,
        youtube_api_version: str,
        developer_key: str
    ) -> None:
        self.youtube: object = build(
            youtube_api_service_name,
            youtube_api_version,
            developerKey=developer_key
        )
        dt = datetime.now(pytz.timezone('Asia/Tokyo'))
        self.date_str = dt.strftime('%Y%m%d%H%M')

    def get_data(self, params: InvokeRequest) -> YouTubeVideoResponse:
        print(params)
        request = self.youtube.videos().list( # type: ignore
            part=params.part, #"snippet, contentDetails, statistics"
            chart=params.chart, #"mostPopular"
            maxResults=params.maxResults, #50
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
    if PROJECT_ID and SECRET_ID and SECRET_YOUTUBE_API_VERSION:
        developer_key = sc.get_secret(
            project_id=PROJECT_ID,
            secret_id=SECRET_ID,
            version_id=SECRET_YOUTUBE_API_VERSION
        )

    if YOUTUBE_API_SERVICE_NAME and YOUTUBE_API_VERSION:
        youtube = YoutubeApiRequest(
            youtube_api_service_name=YOUTUBE_API_SERVICE_NAME,
            youtube_api_version=YOUTUBE_API_VERSION,
            developer_key=developer_key
        )
    params = InvokeRequest(
        prefix= "most_popular",
        part= "snippet, contentDetails, statistics",
        chart= "mostPopular",
        maxResults= 50
    )
    print(youtube.get_data(params))
