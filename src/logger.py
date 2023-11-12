import os.path
import sys

from loguru import logger

_LOG_FORMAT = (
    '<green>{time:MM-DD HH:mm:ss.SSS}</green> '
    '| <level>{level: <7}</level> '
    '| <cyan>{file: <15}<red>:</red> {line: <3}</cyan> '
    '| <magenta><bold>{extra[prefix]}</bold></magenta><level>{message}</level>'
)


def add_log_to_console(log_level: str = 'INFO'):
    logger.add(
        sink=sys.stdout,
        level=log_level,
        format=_LOG_FORMAT
    )


def add_log_to_file(log_dir: str, log_filename: str, log_level: str = 'DEBUG'):
    log_filepath = os.path.join(log_dir, log_filename + '_{time:YYYYMMDD-HHmmss}.log')
    logger.add(
        sink=log_filepath,
        level=log_level,
        format=_LOG_FORMAT,
        rotation='50 MB',  # create a new log file when log file size > 5 MB
        retention='6 months',  # keep log file time: "1 week, 3 days"、"2 months"
        encoding="utf-8",
    )


def show_log_msgs():
    logger.warning('*' * 50)
    logger.trace('This is a test TRACE message.')
    logger.debug('This is a test DEBUG message.')
    logger.info('This is a test INFO message.')
    logger.success('This is a test SUCCESS message.')
    logger.warning('This is a test WARNING message.')
    logger.error('This is a test ERROR message.')
    logger.critical('This is a test CRITICAL message.')
    logger.warning('*' * 50)


def init_logger(log_dir: str = None,
                log_filename: str = 'log',
                console_log_level: str = "INFO",
                file_log_level: str = "DEBUG",
                show_demo_logger: bool = False):
    """loguru全局初始化，不需要再次导入"""
    # first remove default logger sink
    logger.remove()

    # to console
    add_log_to_console(console_log_level)

    # to file
    if log_dir is not None:
        add_log_to_file(log_dir, log_filename, file_log_level)

    # enable log prefix
    logger.configure(extra={'prefix': ''})

    # simple test log output
    if show_demo_logger:
        show_log_msgs()
