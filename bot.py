import os
from datetime import datetime
from dotenv import load_dotenv


# console variables
env_not_configured = 'Please configure the .env file'


# # Functions
# print current time
def current_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# Check if .env exists
if not os.path.exists('.env'):
    with open('.env', 'w') as env:
        env.write('BOT_TOKEN=token\nMONGO_URL=url')
    quit(env_not_configured)

# Load and check .env
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

if BOT_TOKEN == 'token':
    quit(env_not_configured + ': BOT_TOKEN is default')
