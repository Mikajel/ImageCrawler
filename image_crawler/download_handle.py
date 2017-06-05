from os import path, mkdir
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
        if not path.exists(dir_save):
            mkdir(dir_save)

        with open(path.join(dir_save, self._assign_filename(image)), 'wb') as localFile:
            localFile.write(image)

    def _get_image_type(self, data):
        return what('', h=data)