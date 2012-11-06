from os import getenv, path

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
check_hashes = False
debug = False
payload_schema = path.join(path.dirname(path.dirname(__file__)),
                           'payload_schema.json')


#######################
# JSON file overloads #
#######################

config_path = getenv('SD_PROXY_CONFIG', None)

if config_path is None:
    raise AttributeError('Please set SD_PROXY_CONFIG')

locals().update(json.load(open(config_path)))
