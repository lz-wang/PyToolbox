import os.path
import sys

from loguru import logger


def add_log_to_console(log_level: str = 'INFO'):
    logger.add(
        sink=sys.stderr,
        level=log_level,
        format='<green>{time:MM-DD HH:mm:ss.SSS}</green> '
               '| <level>{level: <8}</level> '
               '| <cyan>{name:}</cyan>: <cyan>{function:} '
               '</cyan>: <cyan>line.{line:}</cyan> | '
               '<level>{message}</level> '
    )


def add_log_to_file(log_dir: str, log_level: str = 'DEBUG'):
    logger.add(
        sink=os.path.join(log_dir, 'log_{time:YYYY_MM_DD-HH_mm_ss}.log'),
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} "
               "| {level: <8} | {name:}:{function:}:line.{line} | {message}",
        rotation='10 MB',  # create a new log file when log file size > 5 MB
        retention='1 months',  # keep log file time: "1 week, 3 days"、"2 months"
        # backtrace=True,
        encoding="utf-8",
        # compression='zip'  # zip、tar、gz、tar.gz
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
        add_log_to_file(log_dir, file_log_level)

    # simple test log output
    if show_demo_logger:
        show_log_msgs()
