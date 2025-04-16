import time
import functools
import logging

def timer(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        duration = time.time() - start
        logging.info(f"{fn.__name__} took {duration:.4f} seconds")
        return result
    return wrapper