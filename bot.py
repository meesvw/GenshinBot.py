import interactions
import os
from datetime import datetime
from dotenv import load_dotenv

# console variables
env_not_configured = 'Please configure the .env file'

# check if .env exists
if not os.path.exists('.env'):
    with open('.env', 'w') as env:
        env.write('BOT_TOKEN=token\nMONGO_URL=url')
    quit(env_not_configured)

# load and check .env
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
MONGO_URL = os.getenv('MONGO_URL')

if BOT_TOKEN == 'token':
    quit(env_not_configured + ': BOT_TOKEN is default')

if MONGO_URL == 'url':
    quit(env_not_configured + ': MONGO_URL is default')


# print current time
def ct():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# define and start bot
bot = interactions.Client(token=BOT_TOKEN)


@bot.event
async def on_ready():
    print(f'{ct()} - {bot.me.name} connected to a shard')


bot.start()
