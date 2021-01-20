import discord
import os
import sqlite3
from discord.ext import commands

# vars
BOT_LOCATION = f"{os.path.dirname(os.path.abspath(__file__))}/"
USERS_DATABASE = f"{BOT_LOCATION[:-5]}data/genshin.db"

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
    try:
        connection = sqlite3.connect(USERS_DATABASE)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES (:user_id)", {"user_id": user_id})
        connection.commit()
        connection.close()
        return "You're now a Traveler!"
    except sqlite3.IntegrityError:
        return "You're already a Traveler!"


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
