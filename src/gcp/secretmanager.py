from google.cloud import secretmanager


class SecretManagerInterface:
    def __init__(self) -> None:
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret(
        self,
        project_id: str,
        secret_id: str,
        version_id: str
    ) -> str:
        path = self.client.secret_version_path(
            project_id,
            secret_id,
            version_id
        )
        print(path)

        response = self.client.access_secret_version(
            request={"name": path}
        )

        secret_value = response.payload.data.decode('UTF-8')

        return secret_value


if __name__ == "__main__":
    project_id = "youtube-data-api-385206"
    secret_id = "YOUTUBE_API_KEY"
    version_id = "1"

    sm = SecretManagerInterface()
    youtube_api_key = sm.get_secret(project_id, secret_id, version_id)

    print(youtube_api_key)
