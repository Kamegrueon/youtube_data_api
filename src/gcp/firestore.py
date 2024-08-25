from datetime import datetime, timedelta

from google.cloud import firestore
from google.cloud.firestore_v1.collection import CollectionReference

from utils import date_trunc_from_minutes


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
        # 取得してから35日経過したVIDEO IDはFirestoreのTTLにて削除する
        deletion_date = date_trunc_from_minutes(processed_at + timedelta(days=35))
        collection_ref = self._get_collection(collection_name)
        self._get_existing_video_ids(collection_ref)
        for video_id in video_ids:
            if video_id not in self.existing_video_ids:
                doc_ref = collection_ref.document(f"video_{video_id}")
                doc_ref.set(  # type: ignore
                    {
                        "id": video_id,
                        "processed_at": date_trunc_from_minutes(processed_at),
                        "deletion_date": deletion_date,
                    }
                )

    def get_process_video_ids(self, collection_name: str, processed_at: datetime) -> list[str]:
        collection_ref = self._get_collection(collection_name)
        target_date = date_trunc_from_minutes(processed_at + timedelta(days=-7))

        # 初回取得日が一週間以内のVIDEO IDを取得するクエリ
        query = collection_ref.where("processed_at", ">=", target_date)  # type: ignore
        docs = query.stream()
        video_ids: list[str] = [doc.to_dict()["id"] for doc in docs]  # type: ignore
        return video_ids
