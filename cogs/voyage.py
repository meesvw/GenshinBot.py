import discord
import os
from discord.ext import commands


# Vars
BOT_LOCATION = f"{os.path.dirname(os.path.abspath(__file__))}/"
WORLDS_LOCATION = f"{BOT_LOCATION[:-5]}data/worlds/"


# Functions
def change_user_location(location):
    return


# Create Travelers class
class Voyage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Create Traveler profile.
    @commands.command()
    async def travel(self, ctx, location):
        if f"{location.lower()}.txt" in os.listdir(WORLDS_LOCATION):
            await ctx.send(location)


# Setup cog
def setup(bot):
    bot.add_cog(Voyage(bot))
