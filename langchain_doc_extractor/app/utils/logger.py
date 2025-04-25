import logging
from functools import wraps
from inspect import isfunction

# logger = logging.getLogger(__name__)
logger = logging.getLogger("main")
logging.basicConfig(level=logging.INFO)

def log_call(fn=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cls_name = args[0].__class__.__name__ if args else ""
            logger.info(f"[{cls_name}] {func.__name__}() called")
            return func(*args, **kwargs)
        return wrapper

    # 사용자가 @log_call()처럼 호출했을 경우
    if fn is None:
        return decorator

    # 사용자가 @log_call 처럼 바로 데코레이터로 사용했을 경우
    if isfunction(fn):
        return decorator(fn)

    raise TypeError("Invalid usage of log_call")


def log_all_methods(cls=None):
    def decorator(inner_cls):
        for attr_name, attr in inner_cls.__dict__.items():
            if callable(attr) and not attr_name.startswith("__"):
                setattr(inner_cls, attr_name, log_call(attr))
        return inner_cls

    # 사용자가 @log_all_methods()처럼 호출했을 경우
    if cls is None:
        return decorator
    # 사용자가 @log_all_methods처럼 바로 썼을 경우
    return decorator(cls)
