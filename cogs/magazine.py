import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# Vars
load_dotenv()
BOT_PREFIX = os.getenv("BOT_PREFIX")


# Create Magazine class
class Magazine(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Create Traveler profile.
    @commands.command()
    async def guide(self, ctx):
        embed = discord.Embed(
            color=discord.Colour.purple()
        )

        embed.add_field(
            name="Summary",
            value="GenshinBot has a lot of commands. So much that I can't list them all in one Embed. "
                  "Please visit the wiki for the full documentation. "
                  "Almost all cooking and crafting recipes are the same as in game.\n\n"
                  f"Basic command list: `{BOT_PREFIX}help`",
            inline=False
        )

        embed.set_author(
            name=self.bot.user.name,
            icon_url=self.bot.user.avatar_url,
            url="https://github.com/meesvw/GenshinBot.py/"
        )

        embed.add_field(
            name="Wiki 📖",
            value="https://github.com/meesvw/GenshinBot.py/wiki"
        )

        embed.set_footer(
            text=f"{self.bot.user.name} by mvw#2203",
            icon_url=self.bot.user.avatar_url
        )

        await ctx.send(embed=embed)


# Setup cog
def setup(bot):
    bot.add_cog(Magazine(bot))
