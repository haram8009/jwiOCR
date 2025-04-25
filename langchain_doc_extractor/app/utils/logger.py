import logging
import time
import inspect
from functools import wraps

logger = logging.getLogger("main")
logging.basicConfig(level=logging.INFO)

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
                logger.info(f"[{cls_name}] {func.__name__}() called — took {duration:.2f}s")
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
                logger.info(f"[{cls_name}] {func.__name__}() called — took {duration:.2f}s")
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
