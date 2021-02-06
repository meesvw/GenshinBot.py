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
            title="Guide 📚",
            description="GenshinBot has a lot of commands and different usages. To help you out we've made a wiki. "
                  "Here you can find all the information you need.\n\n"
                  f"To see all the commands: `{BOT_PREFIX}help`",
            color=discord.Colour.purple()
        )

        embed.add_field(
            name="Wiki 📖",
            value="https://github.com/meesvw/GenshinBot.py/wiki",
            inline=False
        )

        embed.add_field(
            name="More questions?",
            value="Visit the official Discord server:\nhttps://discord.gg/8GMKZTT22n"
        )

        embed.set_footer(
            text=f"{self.bot.user.name} by mvw#2203",
            icon_url=self.bot.user.avatar_url
        )

        await ctx.send(embed=embed)


# Setup cog
def setup(bot):
    bot.add_cog(Magazine(bot))
