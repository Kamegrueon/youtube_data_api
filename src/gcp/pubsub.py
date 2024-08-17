from google.cloud import pubsub_v1
from loguru import logger
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
    def publish(self, data: str):
        encoded_data = data.encode("utf-8")
        self.publisher.publish(self.topic_path, data=encoded_data)
        future = self.publisher.publish(self.topic_path, data=encoded_data)
        future.add_done_callback(self._publish_callback)

    def _publish_callback(self, future):
        try:
            message_id = future.result()
            logger.info(f"Message published with ID: {message_id}")
        except Exception as e:
            logger.error(f"Publishing message failed: {str(e)}")
