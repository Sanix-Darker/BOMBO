# First, install configparser using "pip install configparser"
import configparser as ConfigParser

# Configs parameters
configParser = ConfigParser.RawConfigParser()
configFilePath = r"config.txt"
configParser.read(configFilePath)

# Filling parameters
# The ip address of the module
BOMBO_IP = configParser.get("config-box", "BOMBO_IP")
# The telegram token
TOKEN = configParser.get("config-box", "TOKEN")
# The BEFORE_AFTER...
BEFORE, AFTER = "before.jpeg", "after.jpeg"
# The chat id of the person you want the bot to contact
CHAT_ID = configParser.get("config-box", "CHAT_ID")
