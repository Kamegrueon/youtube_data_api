from google.cloud import secretmanager  # type: ignore
from utils import gcp_error_handler


class SecretManagerInterface:
    def __init__(self) -> None:
        self.client = secretmanager.SecretManagerServiceClient()

    @gcp_error_handler
    def get_secret(self, project_id: str, secret_id: str, version_id: str) -> str:
        path = self.client.secret_version_path(project_id, secret_id, version_id)

        response = self.client.access_secret_version(request={"name": path})  # type: ignore

        secret_value = response.payload.data.decode("UTF-8")

        return secret_value


if __name__ == "__main__":
    project_id = "youtube-data-api-385206"
    secret_id = "YOUTUBE_API_KEY"
    version_id = "1"

    sm = SecretManagerInterface()
    youtube_api_key = sm.get_secret(project_id, secret_id, version_id)
