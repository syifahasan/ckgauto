from functools import wraps
from time import sleep


def retry(max_attempts: int = 3, delay_seconds: float = 1.0):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    last_error = exc
                    if attempt == max_attempts:
                        raise
                    sleep(delay_seconds)
            raise last_error
        return wrapper
    return decorator
