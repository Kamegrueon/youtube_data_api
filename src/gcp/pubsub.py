from google.cloud import pubsub_v1


class PubSubInterface:
    def __init__(
        self,
        project_id: str,
        topic_name: str,
    ) -> None:
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_name)

    def publish(self, data: str):
        encode_data = data.encode("utf-8")
        self.publisher.publish(self.topic_path, data=encode_data)
