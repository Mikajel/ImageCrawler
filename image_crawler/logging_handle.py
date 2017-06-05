from os import path, mkdir
import logging
import datetime


class LoggingHandle(object):
    """
    Methods for logging errors and warnings into dedicated local file
    """

    def __init__(self, dir_logging):

        if not path.exists(dir_logging):
            mkdir(dir_logging)

        logging.basicConfig(
            filename=path.join(dir_logging, self._assign_filename()),
            filemode='w',
            level=logging.DEBUG)

        self.info('Logging initialized')

    def info(self, msg: str):
        time_str = datetime.datetime.now().strftime('  %Y-%m-%d %H:%M:%S')
        logging.info(time_str + ' - ' + msg)

    def warning(self, msg: str):
        time_str = datetime.datetime.now().strftime('  %Y-%m-%d %H:%M:%S')
        logging.warning(time_str + ' - ' + msg)

    def error(self, msg: str):
        time_str = datetime.datetime.now().strftime('  %Y-%m-%d %H:%M:%S')
        logging.error(time_str + ' - ' + msg)

    def _assign_filename(self):
        return datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+'.log'
