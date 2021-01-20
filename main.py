import discord
import os
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

# Vars
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_PREFIX = os.getenv("BOT_PREFIX")
BOT_LOCATION = os.getenv("BOT_LOCATION")
bot = commands.AutoShardedBot(command_prefix=BOT_PREFIX, case_insensitive=True)


# Functions

# Print current time
def current_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


# Bot commands

# Load specific cog
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    print(f"{current_time()} - Loaded extension: {extension}")


# Unload specific cog
@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    print(f"{current_time()} - Unloaded extension: {extension}")


# Reload specific cog
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    print(f"{current_time()} - Reloaded extension: {extension}")


# Update all cogs
@bot.command()
@commands.is_owner()
async def update(ctx, extension):
    for file in os.listdir(f"{BOT_LOCATION}cogs"):
        bot.unload_extension(file[:-3])
        bot.load_extension(file[:-3])
        print(f"{current_time()} - Reloaded extension: {extension}")


# Bot events

# Print message when bot connects to a shard
@bot.event
async def on_ready():
    print(f"{current_time()} - {bot.user.name} connected to a shard.")


# Load cogs
for file in os.listdir(f"{BOT_LOCATION}cogs"):
    if file.endswith(".py"):
        try:
            bot.load_extension(file[:-3])
        except:
            print(f"{current_time()} - Error occured loading: {file[:-3]}")

# Start bot
bot.run(BOT_TOKEN)
