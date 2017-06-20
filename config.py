import datetime
import logging
from os import getcwd, mkdir
from os.path import join, exists

# search settings
domain_permissions = {'https://winfreetoiletpaper.com'}
start_url = 'https://winfreetoiletpaper.com'

# local working directory
dir_target = join(getcwd(), 'img')
dir_logging = join(getcwd(), 'logs')


def log_init():
    if not exists(dir_logging):
        mkdir(dir_logging)

    logging.basicConfig(
        filename=join(
            dir_logging,
            datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'),
        filemode='w',
        level=logging.DEBUG)

    logging.info('Logging initialized')
