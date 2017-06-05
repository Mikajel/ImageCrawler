from os.path import join
from os import getcwd

# search settings
# FIXME: Searching might get slow if list contains too many sites
domain_permissions = ['https://exponea.com']
start_url = 'https://exponea.com'

# local working directory
dir_target = join(getcwd(), 'img')
dir_logging = join(getcwd(), 'logs')
