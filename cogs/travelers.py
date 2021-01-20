import discord
import os
import sqlite3
from datetime import datetime
from discord.ext import commands

# vars
BOT_LOCATION = f"{os.path.dirname(os.path.abspath(__file__))}/"
USERS_DATABASE = f"{BOT_LOCATION[:-5]}data/genshin.db"


# Functions

# Print current time
def current_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


# Create user dict
def create_user(user_id):
    try:
        connection = sqlite3.connect(USERS_DATABASE)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES (:user_id)", {"user_id": user_id})
        connection.commit()
        connection.close()
        return "You're now a Traveler!"
    except sqlite3.IntegrityError:
        return "You're already a Traveler!"


# Check if database exists
try:
    connection = sqlite3.connect(USERS_DATABASE)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    location text
    )""")
    print(f"{current_time()} - No table found creating.")
    connection.commit()
    connection.close()
    print(f"{current_time()} - Table has been created.")
except sqlite3.OperationalError:
    print(f"{current_time()} - Table already exists skipping creation.")


# Create Travelers class
class Travelers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Create Traveler profile.
    @commands.command()
    async def appear(self, ctx):

        # Create user in database
        output = create_user(ctx.author.id)
        await ctx.send(output)


# Setup cog
def setup(bot):
    bot.add_cog(Travelers(bot))
