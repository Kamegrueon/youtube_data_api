# requirements update
poetry export -f requirements.txt -o requirements.txt --without-hashes

# build
docker compose build --no-cache
docker build . -t youtube_data_api

# tag
docker tag youtube_data_api gcr.io/youtube-data-api-385206/pubsub:v0.0.12

# push
docker push gcr.io/youtube-data-api-385206/pubsub:v0.0.12

# deploy
gcloud run deploy pubsub-tutorial --image gcr.io/youtube-data-api-385206/pubsub:v0.0.12  --service-account=youtube-data-api@youtube-data-api-385206.iam.gserviceaccount.com --set-env-vars=PROJECT_ID=youtube-data-api-385206,BUCKET_NAME=youtube-data-api-bucket4346542,YOUTUBE_API_SERVICE_NAME=youtube,YOUTUBE_API_VERSION=v3,SECRET_ID=YOUTUBE_API_KEY,SECRET_YOUTUBE_API_VERSION=1 --no-allow-unauthenticated

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
