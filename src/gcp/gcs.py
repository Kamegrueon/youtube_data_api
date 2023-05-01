# import json
import os
import shutil
from typing import Optional

from google.auth.credentials import AnonymousCredentials
from google.cloud.storage import Client
from google.cloud.storage.blob import Blob

from gcp.config.gcp_config import PROJECT_ID

# GCSのオブジェクトを取得する
# curl http://host.docker.internal:4443/storage/v1/b/youtube/o


class GCS:
    def __init__(self, bucket_name: str) -> None:
        self.client = Client(
            credentials=AnonymousCredentials(),
            project=PROJECT_ID,
        )
        self.bucket_name = bucket_name

    def __local_copy_process(self, target_path: str, dest_path: str) -> None:
        shutil.copy(target_path, dest_path)

    def __local_delete_process(self, blob: Blob) -> None:
        local_full_path = f"/app/tmp/cloud-storage/data/{blob.name}"
        os.remove(local_full_path)

    def upload_file(self, gcs_path: str, local_path: str) -> None:
        # local_path = "src/json/json_file.json"
        bucket = self.client.get_bucket(self.bucket_name)
        blob_gcs = bucket.blob(gcs_path)

        blob_gcs.upload_from_filename(local_path)

        gcp_full_path = f"/app/tmp/cloud-storage/data/{gcs_path}"
        self.__local_copy_process(local_path, gcp_full_path)

    def download_file(self, gcs_path: str, local_path: str) -> None:
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob(gcs_path)
        blob.download_to_filename(local_path)

        gcp_full_path = f"/app/tmp/cloud-storage/data/{gcs_path}"
        self.__local_copy_process(gcp_full_path, local_path)

    def get_file(self, blob_path: str) -> Optional[Blob]:
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.get_blob(blob_path)
        return blob

    def delete_file(self, blob: Blob) -> None:
        blob.delete()
        self.__local_delete_process(blob)

    def delete_all_files(self) -> None:
        bucket = self.client.bucket(self.bucket_name)
        blobs = bucket.list_blobs()
        list(map(self.delete_file, blobs))


if __name__ == "__main__":
    # from api.youtube_api import YoutubeApiRequest
    BUCKET_NAME = "youtube"

    # youtube = YoutubeApiRequest()
    gcs = GCS(bucket_name=BUCKET_NAME)

    # youtube.get_youtube_data_to_json()
    # LOCAL_FILE_PATH =
    # f"{youtube.output_path}/{youtube.date_str}_popular.json"
    # GCS_FILE_PATH = f"{gcs.bucket_name}/{youtube.date_str}_popular.json"

    gcs.delete_all_files()

    # gcs.upload_file(
    #     gcs_path=GCS_FILE_PATH,
    #     local_path=LOCAL_FILE_PATH
    # )

    # blob = gcs.get_file(GCS_FILE_PATH)
    # if blob is not None:
    #     with blob.open(mode="r", encoding='utf-8') as f:
    #         j = json.load(f)
    #         print(j)


# blob = bucket.blob("test")

# [print(bucket.name) for bucket in client.list_buckets()]

# with blob.open("w") as f:
#     f.write("Hello World")
