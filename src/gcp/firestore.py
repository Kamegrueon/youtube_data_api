from datetime import datetime, timedelta

from google.cloud import firestore
from google.cloud.firestore_v1.collection import CollectionReference


class FirestoreInterface:
    def __init__(self, project_id: str, database: str) -> None:
        self.client = firestore.Client(project=project_id, database=database)

    def _get_collection(self, collection_name: str) -> CollectionReference:
        return self.client.collection(collection_name)

    def _get_existing_video_ids(self, collection_ref: CollectionReference) -> None:
        self.existing_video_ids: set[str] = set()
        docs = collection_ref.stream()
        for doc in docs:  # type: ignore
            self.existing_video_ids.add(doc.id.split("_")[1])  # type: ignore

    def update_video_ids(self, collection_name: str, processed_at: datetime, video_ids: list[str]):
        end_date = processed_at + timedelta(days=7)
        collection_ref = self._get_collection(collection_name)
        self._get_existing_video_ids(collection_ref)
        for video_id in video_ids:
            if video_id not in self.existing_video_ids:
                doc_ref = collection_ref.document(f"video_{video_id}")
                doc_ref.set({"id": video_id, "processed_at": processed_at, "end_date": end_date.isoformat()})  # type: ignore

    def get_process_video_ids(self, collection_name: str, processed_at: datetime) -> list[str]:
        collection_ref = self._get_collection(collection_name)
        query = collection_ref.where("end_date", ">=", processed_at.isoformat())  # type: ignore
        docs = query.stream()
        video_ids: list[str] = [doc.to_dict()["id"] for doc in docs]  # type: ignore
        return video_ids
