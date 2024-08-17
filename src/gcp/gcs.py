from typing import Optional

from google.cloud import storage  # type: ignore
from utils import gcp_error_handler


class GcsInterface:
    def __init__(
        self,
        project_id: str,
        bucket_name: str,
    ) -> None:
        self.client = storage.Client(project=project_id)
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(bucket_name)  # type: ignore

    @gcp_error_handler
    def upload_json(self, gcs_path: str, contents: str) -> None:
        blob = self.bucket.blob(gcs_path)  # type: ignore
        blob.upload_from_string(contents, content_type="application/json")  # type: ignore

    @gcp_error_handler
    def get_file(self, blob_path: str) -> Optional[storage.Blob]:
        blob = self.bucket.get_blob(blob_path)  # type: ignore
        return blob  # type: ignore
