"""
API 요청 재시도 데코레이터
"""
import time
from functools import wraps
from utils.logger import get_logger

logger = get_logger("retry")

def retry_request(max_retries=3, delay=2.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Error in {func.__name__} (Attempt {attempt+1}/{max_retries}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                    else:
                        logger.error(f"Failed {func.__name__} after {max_retries} attempts.")
                        raise e
        return wrapper
    return decorator
