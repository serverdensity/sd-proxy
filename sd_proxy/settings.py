from os import getenv

try:
    import simplejson as json
except ImportError:
    import json

##################
# Default values #
##################


port = 8889
allow_all_accounts = False
allowed_accounts = []
use_outbound_ssl = True


#######################
# JSON file overloads #
#######################

config_path = getenv('SD_PROXY_CONFIG', None)

if config_path is None:
    raise AttributeError('Please set SD_PROXY_CONFIG')

locals().update(json.load(open(config_path)))
