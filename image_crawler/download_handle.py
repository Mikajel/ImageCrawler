import logging
from os import path, mkdir

from imghdr import what
from urllib import response, request
from django.core.validators import URLValidator, ValidationError


class DownloadHandle(object):
    """
    Class for manipulation of downloaded files
    Handles exceptions and saving to local disk
    """

    def __init__(self):
        self._filename_enum = 0
        self.url_validator = URLValidator()

    def _assign_filename(self, data):

        file_type = self._get_image_type(data)
        if not file_type:
            file_type = ''
        else:
            file_type = '.' + file_type

        self._filename_enum += 1
        return 'image_{:04d}{}'.format(self._filename_enum, file_type)

    def download_image(self, url: str, dir_save: str):

        try:
            self.url_validator(url)
        except ValidationError:
            logging.error('Incorrect format of URL: {:40}'.format(url))
            return

        try:
            img_data = request.urlopen(url)
        except UnicodeEncodeError:
            logging.error('Unsupported URL encoding at: {:40}'.format(url))
            return

        if img_data:
            self._save_image(img_data, dir_save)

    def _save_image(self, data: response, dir_save: str):

        image = data.read()
        if not path.exists(dir_save):
            mkdir(dir_save)

        filename = path.join(dir_save, self._assign_filename(image))
        try:
            with open(filename, 'wb') as localFile:
                localFile.write(image)
        except IOError:
            logging.error('Cannot write to file: {}'.format(filename))

    @staticmethod
    def _get_image_type(data):
        return what('', h=data)
