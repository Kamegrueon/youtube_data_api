import os
import dotenv

dotenv.load_dotenv()

PROJECT_ID = ""
if os.getenv("PROJECT_ID"):
    PROJECT_ID = os.getenv("PROJECT_ID")

BUCKET_NAME = ""
if os.getenv("BUCKET_NAME"):
    BUCKET_NAME = os.getenv("BUCKET_NAME")

TOPIC_NAME = ""
if os.getenv("TOPIC_NAME"):
    TOPIC_NAME = os.getenv("TOPIC_NAME")

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
