import signal
import sys
from functools import wraps

from loguru import logger as log


def gracefully_exit(app_name: str = None):
    """装饰器: 接收 Ctrl + C 信号后正常退出，或docker stop后快速退出"""

    def handle_sigterm():
        raise KeyboardInterrupt()

    def decorate(func):

        @wraps(func)
        def handler(*args, **kwargs):
            try:
                signal.signal(signal.SIGTERM, handle_sigterm)
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                _app_name = app_name or str(func.__name__)
                log.warning(f'App {_app_name} has been stopped, exit now!')
                sys.exit(0)

        return handler

    return decorate
