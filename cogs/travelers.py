import discord
import os
import sqlite3
from discord.ext import commands

# vars
BOT_LOCATION = f"{os.path.dirname(os.path.abspath(__file__))}/"
USERS_DATABASE = f"{BOT_LOCATION[:-5]}data/users.db"

# Check if database exists
connection = sqlite3.connect(USERS_DATABASE)
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
user_id INTEGER PRIMARY KEY
)""")
connection.commit()
connection.close()


# Functions

# Create user dict
def create_user(user_id):
    user_dict = {}
    return user_dict


# Create Travelers class
class Travelers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Create Traveler profile.
    @commands.command()
    async def appear(self, ctx):

        # Connect to database
        await ctx.send("pong!")


# Setup cog
def setup(bot):
    bot.add_cog(Travelers(bot))
