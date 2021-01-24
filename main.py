import discord
import os
import sqlite3
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv


# Vars
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_PREFIX = os.getenv("BOT_PREFIX")
BOT_LOCATION = f"{os.path.dirname(os.path.abspath(__file__))}/"
USERS_DATABASE = f"{BOT_LOCATION}data/genshin.db"
DBL_ENABLED = os.getenv("DBL_ENABLED")
DBL_TOKEN = os.getenv("DBL_TOKEN")
bot = commands.AutoShardedBot(command_prefix=BOT_PREFIX, case_insensitive=True)


# Functions

# Print current time
def current_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


# Set Bot status
async def set_status():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=f"Teyvat | {BOT_PREFIX}help"))


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
async def update(ctx):
    for file in os.listdir(f"{BOT_LOCATION}cogs"):
        if file.endswith(".py"):
            try:
                bot.unload_extension(f"cogs.{file[:-3]}")
                bot.load_extension(f"cogs.{file[:-3]}")
                print(f"{current_time()} - Updated extension: {file[:-3]}")
            except:
                print(f"{current_time()} - Error updating extension: {file[:-3]}")


# Bot events

# Print message when bot connects to a shard
@bot.event
async def on_ready():
    await set_status()
    print(f"{current_time()} - {bot.user.name} connected to a shard.")


# Bot error handler
@bot.event
async def on_command_error(ctx, error):
    # Error handler command not found
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        return False

    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        return await ctx.send(error)


# Startup

# Print logo
print("=========================================")
print("GGGGG EEEEE N   N SSSSS H   H IIIII N   N")
print("G     E     NN  N S     H   H   I   NN  N")
print("G GGG EEEEE N N N SSSSS HHHHH   I   N N N")
print("G   G E     N  NN     S H   H   I   N  NN")
print("GGGGG EEEEE N   N SSSSS H   H IIIII N   N")
print("==== github.com/meesvw/GenshinBot.py ====\n")

# Check if .env exists
if os.path.exists(f"{BOT_LOCATION}.env"):
    if BOT_TOKEN == "YourBotToken":
        print(f"{current_time()} - Please configure the .env file before starting.")
        quit()
    if DBL_TOKEN == "YourDBLToken" and DBL_ENABLED == "True":
        print(f"{current_time()} - Warning TopGG has not been configured.")
else:
    with open(f"{BOT_LOCATION}.env", "w") as file:
        file.write("BOT_TOKEN=YourBotToken\nBOT_PREFIX=gi!\nDBL_ENABLED=False\nDBL_TOKEN=YourDBLToken")
        print(f"{current_time()} - Created .env file.")
    print(f"{current_time()} - Please configure the .env file before starting.")
    quit()

# Check if database exists
try:
    connection = sqlite3.connect(USERS_DATABASE)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    user_dict text,
    status text
    )""")
    connection.commit()
    connection.close()
    print(f"{current_time()} - Database has been created.")
except sqlite3.OperationalError:
    print(f"{current_time()} - Database found skipping creation.")

# Load cogs
for file in os.listdir(f"{BOT_LOCATION}cogs"):
    if file == "topgg.py" and DBL_ENABLED == "False":
        pass
    elif file.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{file[:-3]}")
            print(f"{current_time()} - Loaded extension: {file[:-3]}")
        except:
            print(f"{current_time()} - Error occured loading: {file[:-3]}")

# Start bot
bot.run(BOT_TOKEN)
