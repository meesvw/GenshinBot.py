import discord
from discord.ext import commands


# Create Magazine class
class Warehouse(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Create Traveler profile.
    @commands.command()
    async def craft(self, ctx, *, item):
        return item


# Setup cog
def setup(bot):
    bot.add_cog(Warehouse(bot))
