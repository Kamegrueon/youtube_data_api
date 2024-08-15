import os
import dotenv

dotenv.load_dotenv()

PROJECT_ID = ""
if os.getenv("GOOGLE_PROJECT_ID"):
    PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")

BUCKET_NAME = ""
if os.getenv("CLOUD_STORAGE_BUCKET"):
    BUCKET_NAME = os.getenv("CLOUD_STORAGE_BUCKET")

TOPIC_NAME = ""
if os.getenv("PUBSUB_TOPIC"):
    TOPIC_NAME = os.getenv("PUBSUB_TOPIC")

YOUTUBE_API_SERVICE_NAME = ""
if os.getenv("YOUTUBE_API_SERVICE_NAME"):
    YOUTUBE_API_SERVICE_NAME = os.getenv("YOUTUBE_API_SERVICE_NAME")

YOUTUBE_API_VERSION = ""
if os.getenv("YOUTUBE_API_VERSION"):
    YOUTUBE_API_VERSION = os.getenv("YOUTUBE_API_VERSION")

SECRET_ID = ""
if os.getenv("SECRET_ID"):
    SECRET_ID = os.getenv("SECRET_ID")

SECRET_YOUTUBE_API_VERSION = ""
if os.getenv("SECRET_YOUTUBE_API_VERSION"):
    SECRET_YOUTUBE_API_VERSION = os.getenv("SECRET_YOUTUBE_API_VERSION")

ENVIRONMENT = ""
if os.getenv("ENVIRONMENT"):
    ENVIRONMENT = os.getenv("ENVIRONMENT")
