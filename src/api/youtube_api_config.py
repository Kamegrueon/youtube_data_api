# Standard Library
import os

# Third Party Library
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
