# import sys
from google.cloud import pubsub_v1
from loguru import logger
# from google.cloud.pubsub_v1.subscriber.message import Message


class PubSubInterface:
    def __init__(
        self,
        project_id: str,
        topic_name: str,
    ) -> None:
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_name)

    def publish(self, data: str):
        logger.info(data)
        encode_data = data.encode("utf-8")
        self.publisher.publish(self.topic_path, data=encode_data)


# project_id, name = sys.argv[1], sys.argv[2]

# publisher = pubsub_v1.PublisherClient()
# topic_path = publisher.topic_path(project_id, name)

# cnt = 0
# while cnt < 5:
#     data = "gs://test/test2/test3"
#     data = data.encode("utf-8")
#     print("Publish: " + data.decode("utf-8", "ignore"))
#     future = publisher.publish(topic_path, data=data)
#     print("return ", future.result())
#     time.sleep(1)
#     cnt = cnt + 1


# def callback(message):
#     # now = datetime.datetime.now()
#     # print(message, type(message), dir(message))
#     if not isinstance(message, Message):
#         print("invalid")
#     else:
#         print("not invalid")

#     pubsub_message = message.data.decode("utf-8")
#     print(pubsub_message, type(pubsub_message), dir(pubsub_message))

#     # print("msg = \"" + message.data.decode("utf-8") +
#     #       "\"" + "  [" + now.isoformat(" ") + "]")
#     message.ack()


# subscriber = pubsub_v1.SubscriberClient()
# subpath = subscriber.subscription_path(project_id, name)
# flow_control = pubsub_v1.types.FlowControl(max_messages=2)

# subscriber.subscribe(subpath, callback=callback, flow_control=flow_control)
# input()
