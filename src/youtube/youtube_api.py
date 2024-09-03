# Standard Library
from datetime import datetime
from typing import cast

# Third Party Library
import pytz
from googleapiclient.discovery import build  # type: ignore
from pytz.tzinfo import BaseTzInfo

from api.schemas import YouTubeVideoResponse


class YoutubeApiRequest:
    def __init__(
        self,
        youtube_api_service_name: str,
        youtube_api_version: str,
        developer_key: str,
    ) -> None:
        self.youtube: object = build(
            serviceName=youtube_api_service_name, version=youtube_api_version, developerKey=developer_key
        )
        jst: BaseTzInfo = pytz.timezone("Asia/Tokyo")
        self.processed_at: datetime = datetime.now(jst)

    def get_most_popular(self, part: str, chart: str, maxResults: int) -> YouTubeVideoResponse:
        request = self.youtube.videos().list(  # type: ignore
            part=part, chart=chart, maxResults=maxResults, regionCode="JP"
        )

        res = request.execute()  # type: ignore
        return cast(YouTubeVideoResponse, res)

    def get_video_details(self, part: str, ids: str, maxResults: int) -> YouTubeVideoResponse:
        request = self.youtube.videos().list(  # type: ignore
            part=part, id=ids, maxResults=maxResults, regionCode="JP"
        )

        res = request.execute()  # type: ignore
        return cast(YouTubeVideoResponse, res)


if __name__ == "__main__":
    from env import (
        PROJECT_ID,
        SECRET_ID,
        SECRET_YOUTUBE_API_VERSION,
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
    )
    from gcp.secretmanager import SecretManagerInterface

    sc = SecretManagerInterface()

    developer_key = sc.get_secret(
        project_id=PROJECT_ID,
        secret_id=SECRET_ID,
        version_id=SECRET_YOUTUBE_API_VERSION,
    )

    youtube = YoutubeApiRequest(
        youtube_api_service_name=YOUTUBE_API_SERVICE_NAME,
        youtube_api_version=YOUTUBE_API_VERSION,
        developer_key=developer_key,
    )

    part = ",".join(["snippet", "contentDetails", "statistics"])
    chart = "mostPopular"
    maxResults = 50
    print(youtube.get_most_popular(part, chart, maxResults))
