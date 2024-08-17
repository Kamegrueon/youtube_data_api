from typing import Any, Callable

from google.cloud.exceptions import GoogleCloudError
from loguru import logger


def gcp_error_handler(func: Callable[..., Any]) -> Any:
    def wrapper(*args: Any, **kwargs: Any) -> None:
        try:
            return func(*args, **kwargs)
        except GoogleCloudError as e:
            logger.error(e.code)
            for error in e.errors:  # type: ignore
                for k, v in error.items():  # type: ignore
                    logger.error(f"{k}: {v}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            raise

    return wrapper
