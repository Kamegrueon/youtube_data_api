# requirements update
poetry export -f requirements.txt -o requirements.txt --without-hashes

# memo
- CloudRunを更新した場合、PubSubのSubscriptionを更新する必要あり（307が返ってくる）
- CloudRun側にもPubSubのサービスアカウントのCloudRun起動元の権限がついているかどうか確認

# 不要なイメージの削除
docker rmi $(docker images --filter "reference=gcr.io/youtube-data-api-385206/pubsub:v0.0.*")


# FastAPIへPOSTリクエストを送信
curl -X 'POST' \
  'http://0.0.0.0:8080/invoke/transfer' \
  -H 'Content-Type: application/json' \
  -d '{"message": {"attributes": null, "data": "dHJhbnNmZXIz", "messageId": "10713412108631183", "message_id": "10713412108631183", "orderingKey": null, "publishTime": "2024-03-20T09:49:40.741Z", "publish_time": "2024-03-20T09:49:40.741Z"}, "subscription": "projects/youtube-data-api-385206/subscriptions/CroudRunService", "deliveryAttempt": null}'


curl -X 'POST' \
  'http://0.0.0.0:8080/invoke/load' \
  -H 'Content-Type: application/json' \
  -d '{"message": {"attributes": null, "data": "bW9zdF9wb3B1bGFyLzIwMjQwMzIxMDk1MF9wb3B1bGFyLmpzb24K", "messageId": "10713412108631183", "message_id": "10713412108631183", "orderingKey": null, "publishTime": "2024-03-20T09:49:40.741Z", "publish_time": "2024-03-20T09:49:40.741Z"}, "subscription": "projects/youtube-data-api-385206/subscriptions/CroudRunService", "deliveryAttempt": null}'
