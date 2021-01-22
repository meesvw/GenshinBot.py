import discord
import os
from discord.ext import commands


# Vars


# Functions


# Creates class
class Kitchen(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Create Traveler profile.
    @commands.command()
    async def cook(self, ctx):
        await ctx.send("Pong!")


def setup(bot):
    bot.add_cog(Kitchen(bot))
