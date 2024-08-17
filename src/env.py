import os

import dotenv

dotenv.load_dotenv()

if os.environ["GOOGLE_PROJECT_ID"]:
    PROJECT_ID = os.environ["GOOGLE_PROJECT_ID"]

if os.environ["CLOUD_STORAGE_BUCKET"]:
    BUCKET_NAME = os.environ["CLOUD_STORAGE_BUCKET"]

if os.environ["PUBSUB_TOPIC"]:
    TOPIC_NAME = os.environ["PUBSUB_TOPIC"]

if os.environ["YOUTUBE_API_SERVICE_NAME"]:
    YOUTUBE_API_SERVICE_NAME = os.environ["YOUTUBE_API_SERVICE_NAME"]

if os.environ["YOUTUBE_API_VERSION"]:
    YOUTUBE_API_VERSION = os.environ["YOUTUBE_API_VERSION"]

if os.environ["SECRET_ID"]:
    SECRET_ID = os.environ["SECRET_ID"]

if os.environ["SECRET_YOUTUBE_API_VERSION"]:
    SECRET_YOUTUBE_API_VERSION = os.environ["SECRET_YOUTUBE_API_VERSION"]

if os.environ["ENVIRONMENT"]:
    ENVIRONMENT = os.environ["ENVIRONMENT"]
