from os import path
import logging
import datetime
from imghdr import what
from urllib import request
from urllib import response
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class DownloadHandle(object):
    """
    Class for manipulation of downloaded files
    Handles exceptions and saving to local disk
    """

    __filename_enum = 0

    def __init__(self):
        self.url_validator = URLValidator()

    def _assign_filename(self, data):

        file_type = self._get_image_type(data)
        if not file_type:
            file_type = ''
        else:
            file_type = '.' + file_type

        DownloadHandle.__filename_enum += 1
        return 'image_' + str(self.__filename_enum).zfill(4) + file_type

    def download_image(self, url: str, dir_save: str, log):

        try:
            self.url_validator(url)
        except ValidationError:
            log.error('Incorrect format of URL: {:40}'.format(url))
            return

        try:
            img_data = request.urlopen(url)
        except UnicodeEncodeError:
            log.error('Unsupported URL encoding at: {:40}'.format(url))
            return

        if img_data:
            self._save_image(img_data, dir_save)

    def _save_image(self, data: response, dir_save: str):

        image = data.read()
        with open(path.join(dir_save, self._assign_filename(image)), 'wb') as localFile:
            localFile.write(image)

    def _get_image_type(self, data):
        return what('', h=data)


class LoggingHandle(object):
    """
    Methods for logging errors and warnings into dedicated local file
    """

    def __init__(self, dir_logging):

        logging.basicConfig(
            filename=path.join(dir_logging, self._get_filename()),
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

    def _get_filename(self):
        return datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+'.log'






