import discord
import os
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

# # vars
# dotenv setup
load_dotenv()
prefix = os.getenv('prefix')
# bot setup

bot_dir = f'{os.path.dirname(os.path.abspath(__file__))}/'
bot = commands.AutoShardedBot(
    command_prefix=prefix,
    case_insensitive=True
)


# # functions
# return current time
def current_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


# set bot status
async def set_status():
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.competing,
        name=f"Teyvat | {prefix}guide")
    )


# # bot events
# bot on_ready event
@bot.event
async def on_ready():
    print(f'{current_time()} - {bot.user.name} instance is running')
    await set_status()


# # bot on_command_error event
# @bot.event
# async def on_command_error(ctx, error):
#     # command not found
#     if isinstance(error, commands.CommandNotFound):
#         return
#     # command missing argument
#     if isinstance(error, commands.MissingRequiredArgument):
#         return await ctx.send(error)
#     # command on cooldown
#     if isinstance(error, commands.CommandOnCooldown):
#         return await ctx.send(error)
#     # member not found
#     if isinstance(error, commands.MemberNotFound):
#         return await ctx.send(error)
#     # user not found
#     if isinstance(error, commands.UserNotFound):
#         return await ctx.send(error)


# # startup
# check .env
if not os.path.exists(f'{bot_dir}.env'):
    with open(f'{bot_dir}.env', 'w') as file:
        file.write('token=BotToken\nmongo_url=MongoDBurl\nprefix=g!')
    quit(f'{current_time()} - configure .env file')
elif os.getenv('token') == 'BotToken' or os.getenv('mongo_url') == 'MongoDBurl':
    quit(f'{current_time()} - configure .env file')

# load cogs
for file in os.listdir(f'{bot_dir}cogs'):
    if file.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{file[:-3]}')
        except Exception:
            print(f'{current_time()} - error loading: {file[:-3]}')

# start bot
print('https://github.com/meesvw')
print(f'{current_time()} - starting bot')
bot.run(os.getenv('token'))
