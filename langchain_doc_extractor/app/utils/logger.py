import logging
import time
import inspect
from functools import wraps
import sys

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)  

# Formatter 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# console handler: above INFO level
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# file handler: above DEBUG level
file_handler = logging.FileHandler("debug.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def log_call(fn=None):
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            # async function
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                cls_name = args[0].__class__.__name__ if args else ""
                start = time.perf_counter()
                result = await func(*args, **kwargs)
                duration = time.perf_counter() - start
                logger.info(f"[{cls_name}] {func.__name__}() called - took {duration:.2f}s")
                return result
            return async_wrapper
        else:
            # sync function
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                cls_name = args[0].__class__.__name__ if args else ""
                start = time.perf_counter()
                result = func(*args, **kwargs)
                duration = time.perf_counter() - start
                logger.info(f"[{cls_name}] {func.__name__}() called - took {duration:.2f}s")
                return result
            return sync_wrapper

    return decorator if fn is None else decorator(fn)


def log_all_methods(cls=None):
    def decorator(inner_cls):
        for attr_name, attr in inner_cls.__dict__.items():
            if callable(attr) and not attr_name.startswith("__"):
                decorated = log_call(attr)
                setattr(inner_cls, attr_name, decorated)
        return inner_cls

    return decorator if cls is None else decorator(cls)
