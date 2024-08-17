# Third Party Library
from google.cloud import pubsub_v1  # type: ignore
from loguru import logger

# First Party Library
from utils import gcp_error_handler


class PubSubInterface:
    def __init__(
        self,
        project_id: str,
        topic_name: str,
    ) -> None:
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_name)

    @gcp_error_handler
    def publish(self, data: str) -> None:
        encoded_data = data.encode("utf-8")
        future = self.publisher.publish(self.topic_path, data=encoded_data)  # type: ignore
        future.add_done_callback(self._publish_callback)  # type: ignore

    def _publish_callback(self, future) -> None:  # type: ignore
        try:
            message_id = future.result()  # type: ignore
            logger.info(f"Message published with ID: {message_id}")
        except Exception as e:
            logger.error(f"Publishing message failed: {str(e)}")
