from os import sys, environ
from tracker.__main__ import args

# Name of the file to save kernel versions json
DB_FILE_NAME = "data.json"

# By default looks up in env for api and chat id or just put your stuff in here
# directly if you prefer it that way
BOT_API = environ.get("BOT_API")
CHAT_ID = environ.get("CHAT_ID")

if args.notify:
    if (BOT_API and CHAT_ID) is None:
        print("Either BOT_API or CHAT_ID is empty!")
        sys.exit(1)
