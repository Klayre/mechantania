"""
Evennia settings file.

The available options are found in the default settings file found
here:

c:\users\scyfr\mechantania\evennia\evennia\settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Mechantania"

# open to the internet: 4000, 4001, 4002
# closed to the internet (internal use): 5000, 5001
TELNET_PORTS = [4000]
WEBSOCKET_CLIENT_PORT = 4001
WEBSERVER_PORTS = [(80, 5001)]
AMP_PORT = 5000

ipaddress = '73.71.243.41' 
#WEBSOCKET_CLIENT_INTERFACE = ipaddress
#TELNET_INTERFACES = [ipaddress]

SSH_PORTS = [8022]
#SSH_INTERFACES = [ipaddress]


# security measures (optional)
#TELNET_INTERFACES = ['203.0.113.0']
#WEBSOCKET_CLIENT_INTERFACE = '203.0.113.0'
#ALLOWED_HOSTS = [".mymudgame.com"]

# uncomment to take server offline
# LOCKDOWN_MODE = True

# Register with game index (see games.evennia.com for first setup)
#GAME_DIRECTORY_LISTING = {
#    'game_status': 'pre-alpha',
#    'game_website': 'http://mymudgame.com:4002',
#    'listing_contact': 'me@mymudgame.com',
#    'telnet_hostname': 'mymudgame.com',
#    'telnet_port': 4000,
#    'short_description': "The official Mygame.",
#    'long_description':'Mygame is ...'
#}

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print "secret_settings.py file not found or failed to import."
