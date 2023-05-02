import json

from api.youtube_api import YoutubeApiRequest
from gcp.gcs import GCS

BUCKET_NAME = "youtube"


def main() -> None:
    youtube = YoutubeApiRequest()
    gcs = GCS(bucket_name=BUCKET_NAME)

    youtube.get_youtube_data_to_json()

    local_file_path = f"{youtube.output_path}/{youtube.date_str}_popular.json"
    gcs_file_path = f"{gcs.bucket_name}/{youtube.date_str}_popular.json"

    gcs.upload_file(
        gcs_path=gcs_file_path,
        local_path=local_file_path,
    )

    blob = gcs.get_file(gcs_file_path)
    if blob is not None:
        with blob.open(mode="r", encoding='utf-8') as f:
            j = json.load(f)
            print(j)


if __name__ == "__main__":
    main()
# print(os.environ.get("STORAGE_EMULATOR_HOST"))
