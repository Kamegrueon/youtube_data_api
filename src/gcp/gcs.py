from typing import Optional
from google.cloud import storage


class GcsInterface:
    def __init__(
        self,
        project_id: str,
        bucket_name: str,
    ) -> None:
        self.client = storage.Client(project=project_id)
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(bucket_name)

    def upload_json(self, gcs_path: str, contents: str) -> None:
        blob = self.bucket.blob(gcs_path)
        try:
            blob.upload_from_string(contents, content_type="application/json")
        except Exception as e:
            raise Exception(e)


    def get_file(self, blob_path: str) -> Optional[storage.Blob]:
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.get_blob(blob_path)
        return blob
