from os import getenv, path

try:
    import simplejson as json
except ImportError:
    import json

##################
# Default values #
##################

# All of these values can be overridden in your config.json, which you pass as
# the first argument to the runserver entrypoint (or `sd-proxy` if installed as
# an egg).

# TCP/IP port to bind to
port = 80

# Whether to check subdomains in Host header again allowed_accounts
allow_all_accounts = False

# Account names / subdomains to check Host against
# you can provide either the account name or full domain here,
# e.g.: foobar or foorbar.serverdensity.com, but don't use full URI or
# include port numbers
allowed_accounts = []

# Only forward to serverdensity.com over HTTPS
use_outbound_ssl = True

# Verify the MD5 hash of the payload provided by the agent
check_hashes = False

# Whether to use JSON schema verification
use_schema = False

# Location of the payload JSON (draft3) schema to check payloads against
payload_schema = path.join(path.dirname(__file__),
                           'payload_schema.json')

# List of regular expressions to blacklist a payload if matched
blacklist_regexes = []

# Verify the serverdensity.com postback IP address being used against
# ip_addresses
check_ip_address = True

# Postback IP addresses to verify against if check_ip_address is enabled see
# ping your account URL to get the primary IP and contact hello@serverdensity.com
# if you need details of all our backup IPs (we don't recommend hard coding these)
ip_addresses = (
    '108.168.255.180',
    '208.43.117.99',
    '108.168.255.193',
    '108.168.255.195'
)

# Whether to run Flask in debug mode or not (you can mostly ignore this)
debug = False

# Number of processes to spawn if using multirunserver.py
# Any False value, e.g. 0, None, '', [] will spawn a process per CPU core
processes = None


#######################
# JSON file overloads #
#######################

config_path = getenv('SD_PROXY_CONFIG', None)

if config_path is None:
    raise AttributeError('Please set SD_PROXY_CONFIG')

locals().update(json.load(open(config_path)))
