from google.cloud.exceptions import GoogleCloudError
from loguru import logger


def gcp_error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except GoogleCloudError as e:
            logger.error(e.code)
            for error in e.errors:
                for k, v in error.items():
                    logger.error(f"{k}: {v}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            raise

    return wrapper
