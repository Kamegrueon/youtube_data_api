from datetime import datetime, timedelta

from google.cloud import firestore


class FirestoreInterface:
    def __init__(self, project_id: str) -> None:
        self.client = firestore.Client(project=project_id)

    def _get_existing_video_ids(self, collection_name: str) -> None:
        self.existing_video_ids: set[str] = set()
        docs = self.client.collection(collection_name).stream()
        for doc in docs:  # type: ignore
            self.existing_video_ids.add(doc.id.split("_")[1])  # type: ignore

    def update_video_ids(self, collection_name: str, processed_at: datetime, video_ids: list[str]):
        self._get_existing_video_ids(collection_name)
        for video_id in video_ids:
            if video_id not in self.existing_video_ids:
                doc_ref = self.client.collection(collection_name).document(f"video_{video_id}")
                doc_ref.set({"id": video_id, "processedAt": processed_at.isoformat()})  # type: ignore

    def get_process_video_ids(self, collection_name: str, days_ago: int, processed_at: datetime) -> list[str]:
        start_date = processed_at - timedelta(days=days_ago)
        query = self.client.collection(collection_name).where("processedAt", ">=", start_date.isoformat())  # type: ignore
        docs = query.stream()
        video_ids: list[str] = [doc.to_dict()["id"] for doc in docs]  # type: ignore
        return video_ids
